from __future__ import annotations

import csv
import json
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "geo-benchmark" / "config"


class TiDBFactBaseV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads((CONFIG / "tidb_fact_base_v2.json").read_text())
        cls.facts = cls.payload["facts"]
        with (CONFIG / "tidb_fact_coverage_2026-09.csv").open(newline="") as handle:
            cls.coverage = list(csv.DictReader(handle))

    def test_required_fact_fields_and_unique_ids(self):
        required = {
            "fact_id",
            "category",
            "status",
            "owner",
            "canonical_truth",
            "correct_when",
            "incorrect_when",
            "applies_to",
            "source_urls",
            "judge_prompt",
        }
        ids = [fact["fact_id"] for fact in self.facts]
        self.assertEqual(len(ids), len(set(ids)))
        for fact in self.facts:
            self.assertTrue(required.issubset(fact), fact["fact_id"])
            self.assertIn(fact["status"], {"READY_FOR_JUDGE", "REVIEW_REQUIRED"})
            self.assertTrue(fact["source_urls"], fact["fact_id"])
            self.assertTrue(all(url.startswith("https://") for url in fact["source_urls"]))
            if fact["status"] == "READY_FOR_JUDGE":
                self.assertIsNotNone(fact["verified_on"], fact["fact_id"])
                self.assertIsNotNone(fact["review_by"], fact["fact_id"])

    def test_preview_facts_are_reviewed_quarterly(self):
        for fact in self.facts:
            normalized_truth = fact["canonical_truth"].lower().replace("-", " ")
            if "public preview" not in normalized_truth:
                continue
            self.assertEqual(fact["review_cadence"], "quarterly", fact["fact_id"])
            verified = date.fromisoformat(fact["verified_on"])
            review_by = date.fromisoformat(fact["review_by"])
            self.assertLessEqual((review_by - verified).days, 93, fact["fact_id"])

    def test_product_rename_and_review_gates(self):
        by_id = {fact["fact_id"]: fact for fact in self.facts}
        self.assertNotIn("drive9_definition", by_id)
        self.assertNotIn("mem9_definition", by_id)
        filesystem = by_id["tidb_cloud_filesystem_definition"]
        memory = by_id["tidb_cloud_memory_definition"]
        self.assertIn("drive9", filesystem["incorrect_when"])
        self.assertIn("drive9 as the current product name", filesystem["incorrect_when"])
        self.assertIn("mem9 as the current product name", memory["incorrect_when"])
        self.assertEqual(memory["status"], "REVIEW_REQUIRED")
        self.assertEqual(by_id["tidb_vector_search"]["status"], "REVIEW_REQUIRED")
        self.assertEqual(by_id["tidb_cloud_ru_and_rcu"]["status"], "REVIEW_REQUIRED")

    def test_september_prompts_use_current_memory_and_filesystem_names(self):
        prompts = json.loads(
            (ROOT / "geo-benchmark" / "prompts" / "2026-09" / "prompts.json").read_text()
        )
        relevant = [
            row["prompt_text"]
            for row in prompts
            if "memory" in row["prompt_text"].lower()
            or "filesystem" in row["prompt_text"].lower()
            or "mem9" in row["prompt_text"].lower()
            or "drive9" in row["prompt_text"].lower()
        ]
        self.assertTrue(any("TiDB Cloud Memory" in text for text in relevant))
        self.assertTrue(any("TiDB Cloud Filesystem" in text for text in relevant))
        self.assertFalse(any("mem9" in text.lower() or "drive9" in text.lower() for text in relevant))

    def test_specific_ai_sources_replace_hub_links(self):
        by_id = {fact["fact_id"]: fact for fact in self.facts}
        for fact_id in ("tidb_vector_search", "tidb_full_text_search", "pytidb_definition"):
            self.assertNotIn("https://docs.pingcap.com/ai/", by_id[fact_id]["source_urls"])

    def test_general_answers_do_not_require_unasked_qualifiers(self):
        policy = self.payload["judge_scope_policy"]
        self.assertIn("general 'What is X?'", policy["core_answer_rule"])
        self.assertIn("omitting qualifiers is not an error", policy["omission_rule"])
        example = policy["examples"][0]
        self.assertEqual(example["prompt"], "What is TiDB vector search?")
        self.assertIn("without plan or maturity details", example["expected"])

    def test_questions_and_answers_can_activate_qualifier_checks(self):
        policy = self.payload["judge_scope_policy"]
        activators = " ".join(policy["qualifier_check_activates_when"])
        self.assertIn("The prompt asks", activators)
        self.assertIn("The answer makes a specific claim", activators)
        self.assertEqual(
            policy["qualifier_dimensions"],
            ["maturity", "plan", "region", "version", "access"],
        )
        self.assertIn("asked about or asserted", policy["claim_rule"])

    def test_every_fact_judge_prompt_includes_conditional_scope_rule(self):
        for fact in self.facts:
            prompt = fact["judge_prompt"]
            self.assertIn("Scope rule:", prompt, fact["fact_id"])
            self.assertIn("Omission is not an error", prompt, fact["fact_id"])

    def test_review_queue_is_unique(self):
        reviews = self.payload["review_queue"]
        ids = [item["review_id"] for item in reviews]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("tidb_vector_search_production_status", ids)
        self.assertIn("tidb_cloud_memory_launch_and_rename", ids)
        self.assertIn("tidb_ru_rcu_definition", ids)

    def test_all_branded_prompts_have_an_explicit_disposition(self):
        prompts = json.loads(
            (ROOT / "geo-benchmark" / "prompts" / "2026-09" / "prompts.json").read_text()
        )
        branded_ids = {row["prompt_id"] for row in prompts if row.get("brand_class") == "branded"}
        covered_ids = {row["prompt_id"] for row in self.coverage}
        self.assertEqual(covered_ids, branded_ids)
        allowed = {"fact_covered", "review_required", "comparison_metric_only"}
        self.assertTrue(all(row["coverage_disposition"] in allowed for row in self.coverage))
        self.assertFalse(any(not row["fact_or_review_ids"] and row["coverage_disposition"] != "comparison_metric_only" for row in self.coverage))


if __name__ == "__main__":
    unittest.main()
