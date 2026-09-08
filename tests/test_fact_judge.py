from __future__ import annotations

import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from geo_benchmark.fact_judge import (
    COVERAGE_FIELDS,
    CoverageValidationError,
    JudgeSettings,
    SemanticFactJudge,
    activated_qualifier_dimensions,
    detect_conflicts,
    prepare_fact_coverage,
    validate_fact_coverage,
)
from geo_benchmark.cli import main, prepare, collect, score_and_report, fact_judge_cost
from geo_benchmark.scoring import score_answer
from geo_benchmark.reports import branded_accuracy_table
from geo_benchmark.scoring import brand_metrics


REPO = Path(__file__).resolve().parents[1]
CONFIG = REPO / "geo-benchmark" / "config"


class SemanticFactJudgeTests(unittest.TestCase):
    def test_changed_content_invalidates_saved_judgments(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        prompt = {"prompt_id": "stable_agentinfra_007", "prompt_text": "What is agent memory?"}
        judge = SemanticFactJudge(root, "2026-09", JudgeSettings(mode="mock"))
        judge.judge_answer(prompt, "An answer", "hash")
        judge.flush_cache()
        fresh = SemanticFactJudge(root, "2026-09", JudgeSettings(mode="mock"))
        fresh.payload["facts"][0]["canonical_truth"] = "Updated truth"
        fresh.judge_answer(prompt, "An answer", "hash")
        self.assertEqual(fresh.usage.cache_hits, 0)
        changed = SemanticFactJudge(root, "2026-09", JudgeSettings(mode="mock"))
        changed.judge_answer({**prompt, "prompt_text": "Different question"}, "An answer", "hash")
        self.assertEqual(changed.usage.cache_hits, 0)

    def test_unexpected_live_structures_are_unavailable(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        for response in [[], None, {"output_text": "[]"}, {"output_text": "null"},
                         {"output_text": '{"verdict":"correct"}'}, {"usage": None}]:
            with self.subTest(response=response):
                judge = SemanticFactJudge(root, "2026-09", JudgeSettings(mode="live", retries=0))
                with patch.dict("os.environ", {"OPENAI_API_KEY": "dummy"}), patch(
                    "geo_benchmark.fact_judge._post_json", return_value=response
                ):
                    result = judge.judge_answer({"prompt_id": "stable_agentinfra_007"}, "answer", "hash")
                self.assertEqual(result["unavailable_facts"], 1)
                self.assertFalse(judge.cache)

    def test_unknown_pricing_is_not_zero(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        settings = JudgeSettings(mode="live", model="unknown-model")
        judge = SemanticFactJudge(root, "2026-09", settings)
        self.assertIsNone(fact_judge_cost(judge, {}, settings)["estimated_cost_usd"])

    def test_full_mock_scoring_writes_reports(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        shutil.copytree(REPO / "geo-benchmark/prompts/2026-09", root / "prompts/2026-09")
        prepare(root, "2026-09", 216, 0.3, False)
        with patch("geo_benchmark.providers._post_json", side_effect=AssertionError("Network forbidden")), patch(
            "geo_benchmark.fact_judge._post_json", side_effect=AssertionError("Network forbidden")
        ):
            collect(root, "2026-09", ["mock"], 1, 0, False)
            scored, summary, cost = score_and_report(root, "2026-09", judge_settings=JudgeSettings(mode="mock"))
        self.assertEqual(len(scored), 1296)
        self.assertTrue(any(row.get("semantic_checked_facts", 0) for row in scored))
        report = (root / "reports/2026-09/llm-report.md").read_text()
        self.assertIn("Semantic accuracy", report)
        self.assertEqual(cost["combined_total_estimated_cost_usd"], 0)
        csv_paths = list((root / "reports/2026-09").glob("*.csv"))
        self.assertTrue(any("semantic_fact_accuracy" in p.read_text() for p in csv_paths))

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

    def test_mock_judge_cache_survives_a_new_process(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        prompt = {
            "prompt_id": "stable_agentinfra_007",
            "prompt_text": "How does TiDB handle agent memory persistence?",
        }
        first = SemanticFactJudge(root, "2026-09", JudgeSettings(mode="mock"))
        first.judge_answer(prompt, "TiDB can store agent state.", "answer-hash")
        first.flush_cache()

        second = SemanticFactJudge(root, "2026-09", JudgeSettings(mode="mock"))
        result = second.judge_answer(prompt, "TiDB can store agent state.", "answer-hash")
        self.assertTrue(result["results"][0]["cached"])
        self.assertEqual(second.usage.calls, 0)
        self.assertEqual(second.usage.cache_hits, 1)

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


class FactCoverageWorkflowTests(unittest.TestCase):
    def make_root(self) -> tuple[tempfile.TemporaryDirectory, Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name) / "benchmark"
        config = root / "config"
        config.mkdir(parents=True)
        shutil.copyfile(CONFIG / "tidb_fact_base_v2.json", config / "tidb_fact_base_v2.json")
        return temp, root

    @staticmethod
    def write_prompts(root: Path, month: str, prompts: list[dict[str, str]]) -> None:
        path = root / "prompts" / month / "prompts.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(prompts), encoding="utf-8")

    @staticmethod
    def write_coverage(root: Path, month: str, rows: list[dict[str, str]]) -> Path:
        path = root / "config" / f"tidb_fact_coverage_{month}.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=COVERAGE_FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        return path

    def test_prepare_reuses_only_unchanged_branded_prompts(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        old_rows = [
            {
                "prompt_id": "same",
                "prompt_type": "definition",
                "prompt_text": "What is TiDB?",
                "coverage_disposition": "fact_covered",
                "fact_or_review_ids": "tidb_distributed_sql",
                "note": "approved mapping",
                "mapping_status": "approved",
            },
            {
                "prompt_id": "changed",
                "prompt_type": "definition",
                "prompt_text": "Old wording",
                "coverage_disposition": "fact_covered",
                "fact_or_review_ids": "tidb_distributed_sql",
                "note": "approved mapping",
                "mapping_status": "approved",
            },
        ]
        self.write_coverage(root, "2026-09", old_rows)
        self.write_prompts(
            root,
            "2026-10",
            [
                {"prompt_id": "same", "prompt_type": "definition", "prompt_text": "What is TiDB?", "brand_class": "branded"},
                {"prompt_id": "changed", "prompt_type": "definition", "prompt_text": "New wording", "brand_class": "branded"},
                {"prompt_id": "new", "prompt_type": "definition", "prompt_text": "What is TiDB Cloud?", "brand_class": "branded"},
                {"prompt_id": "generic", "prompt_type": "comparison", "prompt_text": "Best database?", "brand_class": "non_branded"},
            ],
        )

        result = prepare_fact_coverage(root, "2026-10")
        with Path(result["path"]).open(newline="", encoding="utf-8") as handle:
            rows = {row["prompt_id"]: row for row in csv.DictReader(handle)}

        self.assertEqual(result["reused"], 1)
        self.assertEqual(result["needs_review"], 2)
        self.assertEqual(set(rows), {"same", "changed", "new"})
        self.assertEqual(rows["same"]["mapping_status"], "approved")
        self.assertEqual(rows["same"]["fact_or_review_ids"], "tidb_distributed_sql")
        self.assertEqual(rows["changed"]["mapping_status"], "needs_review")
        self.assertEqual(rows["changed"]["fact_or_review_ids"], "")
        self.assertEqual(rows["new"]["mapping_status"], "needs_review")

    def test_validation_blocks_pending_mapping_then_accepts_approval(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        prompt = {
            "prompt_id": "new",
            "prompt_type": "definition",
            "prompt_text": "What is TiDB?",
            "brand_class": "branded",
        }
        self.write_prompts(root, "2026-10", [prompt])
        path = self.write_coverage(
            root,
            "2026-10",
            [{
                "prompt_id": "new",
                "prompt_type": "definition",
                "prompt_text": "What is TiDB?",
                "coverage_disposition": "review_required",
                "fact_or_review_ids": "",
                "note": "review this mapping",
                "mapping_status": "needs_review",
            }],
        )
        with self.assertRaisesRegex(CoverageValidationError, "mapping_status is needs_review"):
            validate_fact_coverage(root, "2026-10")

        self.write_coverage(
            root,
            "2026-10",
            [{
                "prompt_id": "new",
                "prompt_type": "definition",
                "prompt_text": "What is TiDB?",
                "coverage_disposition": "fact_covered",
                "fact_or_review_ids": "tidb_distributed_sql",
                "note": "reviewed",
                "mapping_status": "approved",
            }],
        )
        result = validate_fact_coverage(root, "2026-10")
        self.assertEqual(result["approved"], 1)
        self.assertEqual(result["path"], str(path))

    def test_missing_coverage_error_explains_how_to_prepare_it(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        self.write_prompts(root, "2026-10", [])
        with self.assertRaisesRegex(CoverageValidationError, "prepare-fact-coverage --month 2026-10"):
            validate_fact_coverage(root, "2026-10")

    def test_prepare_writes_an_empty_approved_file_when_no_prompts_are_branded(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        self.write_prompts(
            root,
            "2026-10",
            [{
                "prompt_id": "generic",
                "prompt_type": "category",
                "prompt_text": "Which database architecture fits this workload?",
                "brand_class": "non_branded",
            }],
        )
        result = prepare_fact_coverage(root, "2026-10")
        self.assertTrue(Path(result["path"]).exists())
        self.assertEqual(result["total"], 0)
        self.assertEqual(validate_fact_coverage(root, "2026-10")["approved"], 0)

    def test_committed_september_coverage_is_valid(self):
        result = validate_fact_coverage(REPO / "geo-benchmark", "2026-09")
        self.assertEqual(result["total"], 138)

    def test_missing_approval_cannot_be_inherited(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        prompt = {"prompt_id": "p", "prompt_type": "definition", "prompt_text": "What is TiDB?", "brand_class": "branded"}
        self.write_prompts(root, "2026-10", [prompt])
        self.write_coverage(root, "2026-09", [{
            "prompt_id": "p", "prompt_type": "definition", "prompt_text": "What is TiDB?",
            "coverage_disposition": "fact_covered", "fact_or_review_ids": "tidb_distributed_sql"
        }])
        result = prepare_fact_coverage(root, "2026-10")
        self.assertEqual(result["needs_review"], 1)
        with self.assertRaises(CoverageValidationError):
            validate_fact_coverage(root, "2026-10")

    def test_direct_run_applies_coverage_gate_before_provider_collection(self):
        with patch("geo_benchmark.cli.prepare"), patch(
            "geo_benchmark.cli.validate_prompts_or_exit"
        ), patch(
            "geo_benchmark.cli.prepare_and_validate_fact_coverage",
            side_effect=SystemExit("coverage review required"),
        ), patch("geo_benchmark.cli.collect") as collect_answers:
            with self.assertRaisesRegex(SystemExit, "coverage review required"):
                main([
                    "--data-dir",
                    "test-data",
                    "run",
                    "--month",
                    "2026-10",
                    "--providers",
                    "mock",
                    "--fact-judge",
                    "mock",
                ])
        collect_answers.assert_not_called()


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
