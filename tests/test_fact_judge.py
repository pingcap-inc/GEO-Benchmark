from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from geo_benchmark.fact_judge import (
    JudgeSettings,
    SemanticFactJudge,
    activated_qualifier_dimensions,
    detect_conflicts,
)
from geo_benchmark.scoring import score_answer
from geo_benchmark.reports import branded_accuracy_table
from geo_benchmark.scoring import brand_metrics


REPO = Path(__file__).resolve().parents[1]
CONFIG = REPO / "geo-benchmark" / "config"


class SemanticFactJudgeTests(unittest.TestCase):
    def make_root(self) -> tuple[tempfile.TemporaryDirectory, Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name) / "geo-benchmark"
        config = root / "config"
        config.mkdir(parents=True)
        for name in ["tidb_fact_base_v2.json", "tidb_fact_coverage_2026-09.csv"]:
            shutil.copyfile(CONFIG / name, config / name)
        return temp, root

    def test_general_definition_does_not_activate_plan_qualifier(self):
        dimensions = activated_qualifier_dimensions(
            "What is TiDB Cloud Zero?",
            "TiDB Cloud Zero is a temporary TiDB environment for evaluation.",
        )
        self.assertNotIn("plan", dimensions)
        self.assertNotIn("maturity", dimensions)

    def test_question_or_answer_can_activate_only_relevant_qualifiers(self):
        self.assertEqual(
            activated_qualifier_dimensions("Is this generally available?", "It supports SQL."),
            ["maturity"],
        )
        self.assertEqual(
            activated_qualifier_dimensions("What is this?", "It is generally available."),
            ["maturity"],
        )

    def test_review_required_fact_is_excluded(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        judge = SemanticFactJudge(root, "2026-09", JudgeSettings(mode="mock"))
        result = judge.judge_answer(
            {"prompt_id": "stable_agentinfra_008", "prompt_text": "How does the RU model work?"},
            "A mock answer.",
            "answer-hash",
        )
        self.assertEqual(result["coverage_disposition"], "review_required")
        self.assertEqual(result["selected_facts"], 0)
        self.assertEqual(result["checked_facts"], 0)

    def test_retired_name_conflicts_distinguish_current_from_historical_usage(self):
        rules = [
            {"conflict_id": "drive9_current_name"},
            {"conflict_id": "mem9_current_name"},
        ]
        current = detect_conflicts("mem9 is the current memory product.", rules)
        historical = detect_conflicts("mem9 was renamed and is now called TiDB Cloud Memory.", rules)
        self.assertEqual([row["fact_id"] for row in current], ["conflict:mem9_current_name"])
        self.assertEqual(historical, [])

    def test_mock_judge_writes_structured_verdict_and_uses_cache(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        judge = SemanticFactJudge(root, "2026-09", JudgeSettings(mode="mock"))
        prompt = {
            "prompt_id": "stable_agentinfra_007",
            "prompt_text": "How does TiDB handle agent memory persistence?",
        }
        answer = "[[fact:tidb_agent_memory_storage:incorrect]]"
        first = judge.judge_answer(prompt, answer, "answer-hash")
        second = judge.judge_answer(prompt, answer, "answer-hash")
        self.assertEqual(first["results"][0]["verdict"], "incorrect")
        self.assertEqual(first["accuracy"], 0.0)
        self.assertTrue(second["results"][0]["cached"])
        self.assertEqual(judge.usage.calls, 1)
        self.assertEqual(judge.usage.cache_hits, 1)

    def test_live_judge_missing_key_is_unavailable_not_incorrect(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        judge = SemanticFactJudge(root, "2026-09", JudgeSettings(mode="live"))
        with patch.dict("os.environ", {}, clear=True):
            result = judge.judge_answer(
                {
                    "prompt_id": "stable_agentinfra_007",
                    "prompt_text": "How does TiDB handle agent memory persistence?",
                },
                "TiDB can store agent state.",
                "answer-hash",
            )
        self.assertEqual(result["results"][0]["verdict"], "judge_unavailable")
        self.assertIsNone(result["accuracy"])
        self.assertEqual(result["unavailable_facts"], 1)

    def test_live_judge_malformed_responses_retry_then_become_unavailable(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        judge = SemanticFactJudge(
            root,
            "2026-09",
            JudgeSettings(mode="live", retries=1),
        )
        malformed = {"output_text": "not json", "usage": {"input_tokens": 2, "output_tokens": 2}}
        with patch.dict("os.environ", {"OPENAI_API_KEY": "invalid-test-key"}, clear=True), patch(
            "geo_benchmark.fact_judge._post_json", return_value=malformed
        ) as request:
            result = judge.judge_answer(
                {
                    "prompt_id": "stable_agentinfra_007",
                    "prompt_text": "How does TiDB handle agent memory persistence?",
                },
                "TiDB can store agent state.",
                "answer-hash",
            )
        self.assertEqual(request.call_count, 2)
        self.assertEqual(result["results"][0]["verdict"], "judge_unavailable")
        self.assertIsNone(result["accuracy"])
        self.assertFalse(judge.cache)


class LiteralAccuracyScopeTests(unittest.TestCase):
    def test_generic_terms_do_not_activate_facts_for_absent_product(self):
        row = {
            "answer_id": "a1",
            "run_id": "r1",
            "month": "2026-09",
            "prompt_id": "p1",
            "model_surface": "mock",
            "raw_answer": "CockroachDB is a distributed SQL database with vector search.",
        }
        prompt = {"prompt_id": "p1", "prompt_text": "Best database for this workload?"}
        facts = {
            "targets": {
                "TiDB": [
                    {
                        "triggers": ["distributed sql", "vector"],
                        "expected_any": ["distributed sql"],
                        "wrong_any": [],
                    }
                ]
            }
        }
        result = score_answer(row, prompt, {"rules": []}, facts, "TiDB")
        self.assertFalse(result["mentioned_target"])
        self.assertEqual(result["accuracy_checked_facts"], 0)
        self.assertEqual(result["accuracy_correct_facts"], 0)


class SemanticReportingTests(unittest.TestCase):
    def test_brand_metrics_keep_unavailable_separate_from_accuracy(self):
        rows = [
            {
                "prompt_id": "p1",
                "accuracy_checked_facts": 1,
                "accuracy": 1.0,
                "citation_presence": True,
                "recommendation_class": "not_mentioned",
                "semantic_fact_judge": {"selected_facts": 1},
                "semantic_fact_accuracy": 1.0,
                "semantic_unavailable_facts": 0,
                "semantic_not_enough_information_facts": 0,
            },
            {
                "prompt_id": "p2",
                "accuracy_checked_facts": 0,
                "accuracy": 1.0,
                "citation_presence": False,
                "recommendation_class": "not_mentioned",
                "semantic_fact_judge": {"selected_facts": 1},
                "semantic_fact_accuracy": None,
                "semantic_unavailable_facts": 1,
                "semantic_not_enough_information_facts": 0,
            },
        ]
        metrics = brand_metrics(rows)
        self.assertEqual(metrics["semantic_brand_accuracy"], 100.0)
        self.assertEqual(metrics["semantic_brand_accuracy_coverage"], 0.5)
        self.assertEqual(metrics["semantic_brand_unavailable_facts"], 1)

    def test_branded_report_table_exposes_legacy_and_semantic_metrics(self):
        overall = {
            "branded_prompt_count": 2,
            "brand_accuracy": 75.0,
            "brand_accuracy_coverage": 1.0,
            "semantic_brand_accuracy": 100.0,
            "semantic_brand_accuracy_coverage": 0.5,
            "semantic_brand_unavailable_facts": 1,
        }
        lines = branded_accuracy_table(
            {"target_order": ["TiDB"], "targets": {"TiDB": {"overall": overall}}}
        )
        rendered = "\n".join(lines)
        self.assertIn("Semantic accuracy", rendered)
        self.assertIn("| TiDB | 2 | 75.00 | 100.00% | 100.00 | 50.00% | 1 |", rendered)

    def test_guarded_workflow_runs_full_test_discovery(self):
        script = (REPO / "scripts" / "run-benchmark-workflow.sh").read_text(encoding="utf-8")
        self.assertIn("python3 -m unittest discover -s tests", script)


if __name__ == "__main__":
    unittest.main()
