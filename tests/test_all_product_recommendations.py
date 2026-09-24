import csv
import tempfile
import unittest
from pathlib import Path

from geo_benchmark.reports import add_answer_level_recommendations, write_csv
from geo_benchmark.scoring import extract_recommended_products, score_answer
from geo_benchmark.source_report import build_cited_domain_details


class AllProductRecommendationTests(unittest.TestCase):
    def raw(self, answer: str) -> dict:
        return {
            "answer_id": "a1",
            "run_id": "r1",
            "month": "2026-09",
            "prompt_id": "p1",
            "model_surface": "openai",
            "model_name": "test-model",
            "status": "ok",
            "raw_answer": answer,
        }

    def prompt(self) -> dict:
        return {
            "prompt_id": "p1",
            "prompt_text": "Best database for a low-latency cache?",
            "panel": "stable",
            "group": "discovery",
            "prompt_type": "AI Agent Infrastructure",
            "use_case": "agentinfra",
            "intent_weight": 3,
            "qualified_recommendation_opportunity": True,
        }

    def test_non_branded_competitor_recommendation_without_tidb(self):
        scored = score_answer(
            self.raw("For this workload, I recommend Redis."),
            self.prompt(),
            {"rules": [], "default_weight": 0.2},
            {"targets": {}},
            "TiDB",
        )

        self.assertEqual(scored["recommended_products"], ["Redis (1)"])
        self.assertEqual(scored["recommendation_class"], "not_mentioned")
        self.assertEqual(scored["recommendation_score"], 0.0)

    def test_ranked_recommendations_include_favored_and_supporting_products(self):
        answer = (
            "Final recommendation: Redis is the best fit. "
            "TiDB is also a strong alternative."
        )

        self.assertEqual(
            extract_recommended_products(answer),
            ["Redis (1)", "TiDB (2)"],
        )

    def test_neutral_depends_answer_has_no_recommended_products(self):
        answer = (
            "It depends on the use case: choose Redis if caching dominates; "
            "choose TiDB if transactional SQL dominates."
        )

        self.assertEqual(extract_recommended_products(answer), [])

    def test_source_details_extract_competitor_from_raw_answer(self):
        raw = self.raw(
            "For this workload, I recommend Redis. Source: https://redis.io/docs/latest/"
        )
        raw["raw_citations"] = ["https://redis.io/docs/latest/"]
        legacy_tidb_score = {
            "answer_id": "a1",
            "prompt_id": "p1",
            "target": "TiDB",
            "mentioned_target": False,
            "recommendation_class": "not_mentioned",
            "competitive_winner": None,
        }

        details = build_cited_domain_details(
            [raw], [legacy_tidb_score], [self.prompt()]
        )

        self.assertEqual(details[0]["recommended_products"], ["Redis (1)"])

    def test_offline_report_refresh_enriches_old_scored_rows_and_csv(self):
        raw = self.raw("For this workload, I recommend Redis.")
        old_scored = [{"answer_id": "a1", "target": "TiDB"}]

        add_answer_level_recommendations(old_scored, [raw])

        self.assertEqual(old_scored[0]["recommended_products"], ["Redis (1)"])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scored_answers.csv"
            write_csv(path, old_scored)
            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(rows[0]["recommended_products"], "Redis (1)")


if __name__ == "__main__":
    unittest.main()
