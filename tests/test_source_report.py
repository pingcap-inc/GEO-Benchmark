import csv
import tempfile
import unittest
from pathlib import Path

from geo_benchmark.source_report import (
    aggregate_cited_domains,
    build_cited_domain_details,
    normalize_domain,
    source_type_for_url,
    write_cited_domain_report,
)


class CitedDomainReportTests(unittest.TestCase):
    def setUp(self):
        self.prompts = [
            {
                "prompt_id": "p1",
                "prompt_text": "Best database for an AI application?",
                "brand_class": "non_branded",
                "group": "discovery",
                "prompt_type": "AI Agent Infrastructure",
                "use_case": "agentinfra",
                "panel": "stable",
            }
        ]
        self.raw = [
            {
                "answer_id": "a1",
                "status": "ok",
                "prompt_id": "p1",
                "model_surface": "openai",
                "run_index": 1,
                "raw_answer": "TiDB is recommended. See https://www.example.com/answer.",
                "raw_citations": [
                    "https://example.com/answer",
                    "https://www.example.com/another-page",
                    "https://docs.pingcap.com/tidb/stable",
                ],
            },
            {
                "answer_id": "a2",
                "status": "ok",
                "prompt_id": "p1",
                "model_surface": "anthropic",
                "run_index": 2,
                "raw_answer": "CockroachDB is recommended.",
                "raw_citations": ["https://example.com/second-answer"],
            },
            {
                "answer_id": "failed",
                "status": "error",
                "prompt_id": "p1",
                "raw_citations": ["https://ignored.example/failure"],
            },
        ]
        self.scored = [
            {
                "answer_id": "a1",
                "prompt_id": "p1",
                "target": "TiDB",
                "mentioned_target": True,
                "recommendation_class": "best",
                "competitive_winner": None,
            },
            {
                "answer_id": "a1",
                "prompt_id": "p1",
                "target": "CockroachDB",
                "mentioned_target": False,
                "recommendation_class": "not_mentioned",
                "competitive_winner": None,
            },
            {
                "answer_id": "a2",
                "prompt_id": "p1",
                "target": "TiDB",
                "mentioned_target": False,
                "recommendation_class": "not_mentioned",
                "competitive_winner": "CockroachDB",
            },
            {
                "answer_id": "a2",
                "prompt_id": "p1",
                "target": "CockroachDB",
                "mentioned_target": True,
                "recommendation_class": "strong",
                "competitive_winner": "CockroachDB",
            },
        ]

    def test_normalizes_domains_and_rejects_non_http_links(self):
        self.assertEqual(normalize_domain("https://WWW.Example.com/page"), "example.com")
        self.assertEqual(normalize_domain("http://docs.example.com/page"), "docs.example.com")
        self.assertIsNone(normalize_domain("javascript:alert(1)"))

    def test_source_type_uses_three_requested_groups(self):
        self.assertEqual(source_type_for_url("https://docs.pingcap.com/tidb/stable"), "PingCAP")
        self.assertEqual(source_type_for_url("https://cockroachlabs.com/docs/stable"), "Competitor")
        self.assertEqual(source_type_for_url("https://example.com/article"), "Other")

    def test_details_deduplicate_domains_within_each_answer(self):
        details = build_cited_domain_details(self.raw, self.scored, self.prompts)
        example_rows = [row for row in details if row["domain"] == "example.com"]

        self.assertEqual(len(example_rows), 2)
        self.assertEqual(len(example_rows[0]["citation_urls"]), 2)
        self.assertEqual(example_rows[0]["brand_class"], "non_branded")
        self.assertEqual(example_rows[0]["group"], "discovery")
        self.assertTrue(example_rows[0]["tidb_appeared"])
        self.assertEqual(example_rows[0]["recommended_products"], ["TiDB"])
        self.assertEqual(example_rows[1]["recommended_products"], ["CockroachDB"])

    def test_summary_ranks_by_unique_prompts_not_repeated_answers(self):
        details = build_cited_domain_details(self.raw, self.scored, self.prompts)
        summary = aggregate_cited_domains(details)
        example = next(row for row in summary if row["domain"] == "example.com")

        self.assertEqual(example["prompt_count"], 1)
        self.assertEqual(example["cited_answer_count"], 2)
        self.assertEqual(example["tidb_appeared_prompt_count"], 1)
        self.assertEqual(example["recommended_products"], {"CockroachDB": 1, "TiDB": 1})

    def test_writes_filterable_html_and_complete_csv_exports(self):
        self.prompts[0]["prompt_text"] = "Question </script><script>alert(1)</script>"
        with tempfile.TemporaryDirectory() as tmp:
            report_dir = Path(tmp)
            write_cited_domain_report(
                report_dir, "2026-09", self.raw, self.scored, self.prompts
            )

            html = (report_dir / "cited-domains.html").read_text(encoding="utf-8")
            self.assertIn('id="brand_class"', html)
            self.assertIn('id="recommended_product"', html)
            self.assertIn('id="tidb_appeared"', html)
            self.assertNotIn("</script><script>alert(1)</script>", html)
            self.assertIn("\\u003c/script\\u003e", html)

            with (report_dir / "cited-domain-summary.csv").open(
                newline="", encoding="utf-8"
            ) as handle:
                summary_rows = list(csv.DictReader(handle))
            with (report_dir / "cited-domain-details.csv").open(
                newline="", encoding="utf-8"
            ) as handle:
                detail_rows = list(csv.DictReader(handle))

            self.assertEqual(summary_rows[0]["domain"], "example.com")
            self.assertEqual(len(detail_rows), 3)


if __name__ == "__main__":
    unittest.main()
