import tempfile
import unittest
import os
import socket
from pathlib import Path
from typing import Optional
from unittest.mock import patch

from geo_benchmark.cli import (
    collect,
    fallback_error_is_eligible,
    load_env_files,
    load_prompts,
    prepare,
    prompt_validation_errors,
    prompt_source_root,
    retry_configured_errors,
    retry_errors,
    selected_prompt_ids,
)
from geo_benchmark.costs import estimate_actual_cost, estimate_planned_cost
from geo_benchmark.defaults import DEFAULT_MODELS, DEFAULT_PRICING, DEFAULT_TARGETS
from geo_benchmark.io_utils import read_json, read_jsonl, stable_hash, write_json, write_jsonl
from geo_benchmark.providers import AnthropicProvider, OpenAIProvider, ProviderError, _post_json
from geo_benchmark.reports import write_reports
from geo_benchmark.scoring import (
    aggregate_scores,
    aggregate_slice,
    competitive_winner,
    is_product_related_url,
    product_in_prompt,
    product_positions,
    score_answer,
    score_answers,
)
from geo_benchmark.seed import generate_seed_prompts


class GeoBenchmarkTests(unittest.TestCase):
    def _aggregate_row(self, prompt_id="p1", **overrides):
        row = {
            "prompt_id": prompt_id,
            "panel": "stable",
            "intent_weight": 1,
            "presence_score": 1.0,
            "citation_authority_answer": 1.0,
            "recommendation_score": 1.0,
            "recommendation_class": "best",
            "qualified_recommendation_opportunity": True,
            "mention_position": "first",
            "source_authority": 1.0,
            "accuracy": 1.0,
            "accuracy_checked_facts": 1,
            "freshness": 1.0,
            "citation_presence": True,
            "target_in_prompt": False,
        }
        row.update(overrides)
        return row

    def test_prepare_keeps_stable_prompts_across_months(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prepare(root, "2026-08", 20, 0.3, False)
            prepare(root, "2026-09", 20, 0.3, False)
            aug = read_json(root / "prompts" / "2026-08" / "prompts.json")
            sep = read_json(root / "prompts" / "2026-09" / "prompts.json")
            aug_stable = [row for row in aug if row["panel"] == "stable"]
            sep_stable = [row for row in sep if row["panel"] == "stable"]
            self.assertEqual(aug_stable, sep_stable)
            self.assertEqual(len([row for row in sep if row["panel"] == "dynamic"]), 6)

    def test_provider_data_dir_uses_canonical_prompt_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            canonical = base / "geo-benchmark"
            provider_root = base / "geo-benchmark-openai"

            prepare(provider_root, "2026-08", 20, 0.3, False)

            self.assertEqual(prompt_source_root(provider_root), canonical)
            self.assertTrue((canonical / "prompts" / "2026-08" / "prompts.json").exists())
            self.assertFalse((provider_root / "prompts" / "2026-08" / "prompts.json").exists())
            self.assertEqual(
                load_prompts(provider_root, "2026-08"),
                read_json(canonical / "prompts" / "2026-08" / "prompts.json"),
            )

    def test_score_answer_detects_tidb_recommendation_and_citation(self):
        prompt = {
            "prompt_id": "p1",
            "panel": "stable",
            "prompt_type": "category",
            "intent_weight": 3,
            "qualified_recommendation_opportunity": True,
        }
        row = {
            "answer_id": "a1",
            "run_id": "r1",
            "month": "2026-08",
            "prompt_id": "p1",
            "model_surface": "mock",
            "model_name": "mock",
            "raw_answer": (
                "Best choice: TiDB. TiDB is a distributed SQL database with MySQL "
                "compatibility and vector search. Source: https://docs.pingcap.com/tidb/stable"
            ),
        }
        source_authority = {
            "rules": [{"contains": "docs.pingcap.com", "weight": 1.0, "label": "official_docs"}],
            "default_weight": 0.2,
        }
        facts = {
            "facts": [
                {
                    "triggers": ["distributed sql"],
                    "expected_any": ["distributed sql"],
                    "wrong_any": ["single-node only"],
                }
            ]
        }
        scored = score_answer(row, prompt, source_authority, facts)
        self.assertEqual(scored["mention_position"], "first")
        self.assertEqual(scored["recommendation_class"], "best")
        self.assertGreater(scored["citation_authority_answer"], 0.8)

    def test_score_answer_uses_raw_citations_when_answer_has_no_url(self):
        prompt = {
            "prompt_id": "p1",
            "panel": "stable",
            "prompt_type": "category",
            "intent_weight": 3,
            "qualified_recommendation_opportunity": True,
        }
        row = {
            "answer_id": "a1",
            "run_id": "r1",
            "month": "2026-08",
            "prompt_id": "p1",
            "model_surface": "anthropic",
            "model_name": "claude-sonnet-5",
            "raw_answer": "Best choice: TiDB for scale-out distributed SQL.",
            "raw_citations": ["https://docs.pingcap.com/tidb/stable"],
        }
        source_authority = {
            "rules": [{"contains": "docs.pingcap.com", "weight": 1.0, "label": "official_docs"}],
            "default_weight": 0.2,
        }

        scored = score_answer(row, prompt, source_authority, {"targets": {}}, "TiDB")

        self.assertTrue(scored["citation_presence"])
        self.assertGreater(scored["citation_authority_answer"], 0)

    def test_score_answers_supports_multiple_targets(self):
        prompts = [
            {
                "prompt_id": "p1",
                "prompt_text": "What is TiDB Cloud Zero?",
                "panel": "stable",
                "prompt_type": "category",
                "intent_weight": 3,
                "qualified_recommendation_opportunity": True,
            }
        ]
        raw = [
            {
                "answer_id": "a1",
                "run_id": "r1",
                "status": "ok",
                "month": "2026-08",
                "prompt_id": "p1",
                "model_surface": "mock",
                "model_name": "mock",
                "raw_answer": "1. CockroachDB\n2. TiDB\nSources: https://www.cockroachlabs.com/docs/stable https://docs.pingcap.com/tidb/stable",
            }
        ]
        source_authority = {
            "rules": [
                {"contains": "docs.pingcap.com", "weight": 1.0, "label": "official_docs"},
                {"contains": "cockroachlabs.com/docs", "weight": 1.0, "label": "official_docs"},
            ],
            "default_weight": 0.2,
        }
        scored = score_answers(raw, prompts, source_authority, {"targets": {}}, ["TiDB", "CockroachDB"])
        self.assertEqual({row["target"] for row in scored}, {"TiDB", "CockroachDB"})
        by_target = {row["target"]: row for row in scored}
        self.assertEqual(by_target["CockroachDB"]["mention_position"], "first")
        self.assertEqual(by_target["TiDB"]["mention_position"], "top3")
        self.assertEqual(by_target["TiDB"]["brand_class"], "branded")
        self.assertEqual(by_target["CockroachDB"]["brand_class"], "non_branded")

    def test_aggregate_scores_splits_overall_and_unchanged(self):
        rows = [
            {
                "prompt_id": "stable_1",
                "panel": "stable",
                "intent_weight": 1,
                "presence_score": 1.0,
                "citation_authority_answer": 1.0,
                "recommendation_score": 1.0,
                "recommendation_class": "best",
                "qualified_recommendation_opportunity": True,
                "mention_position": "first",
                "source_authority": 1.0,
                "accuracy": 1.0,
                "freshness": 1.0,
            },
            {
                "prompt_id": "dynamic_1",
                "panel": "dynamic",
                "intent_weight": 1,
                "presence_score": 0.0,
                "citation_authority_answer": 0.0,
                "recommendation_score": 0.0,
                "recommendation_class": "not_mentioned",
                "qualified_recommendation_opportunity": True,
                "mention_position": "none",
                "source_authority": 0.0,
                "accuracy": 1.0,
                "freshness": 0.0,
            },
        ]
        summary = aggregate_scores(rows)
        self.assertEqual(summary["overall"]["answer_share"], 50.0)
        self.assertEqual(summary["unchanged"]["answer_share"], 100.0)

    def test_branded_rows_excluded_from_visibility(self):
        prompt = {
            "prompt_id": "branded_1",
            "prompt_text": "What is TiDB Cloud Zero?",
            "panel": "stable",
            "prompt_type": "brand_fact",
            "intent_weight": 1,
            "qualified_recommendation_opportunity": False,
        }
        row = {
            "answer_id": "answer_1",
            "run_id": "run_1",
            "month": "2026-09",
            "prompt_id": "branded_1",
            "model_surface": "mock",
            "model_name": "mock",
            "raw_answer": "TiDB Cloud Zero is a TiDB product.",
        }

        scored = score_answer(row, prompt, {}, {"targets": {}}, "TiDB")
        metrics = aggregate_slice([scored])

        self.assertTrue(scored["target_in_prompt"])
        self.assertEqual(scored["brand_class"], "branded")
        self.assertEqual(scored["mention_position"], "first")
        self.assertEqual(metrics["answer_share"], 0.0)
        self.assertEqual(metrics["prompt_count"], 0)
        self.assertEqual(metrics["answer_count"], 1)

    def test_non_branded_rows_still_scored(self):
        row = self._aggregate_row(
            presence_score=0.6,
            citation_authority_answer=0.5,
            recommendation_score=0.75,
            recommendation_class="strong",
        )

        metrics = aggregate_slice([row])

        self.assertEqual(metrics["answer_share"], 60.0)
        self.assertEqual(metrics["citation_authority"], 50.0)
        self.assertEqual(metrics["qualified_recommendation_rate"], 100.0)

    def test_brand_metrics_populated_for_branded_rows(self):
        row = self._aggregate_row(
            target_in_prompt=True,
            accuracy=0.5,
            accuracy_checked_facts=2,
            citation_presence=True,
            recommendation_class="negative",
        )

        metrics = aggregate_slice([row])

        self.assertEqual(metrics["branded_prompt_count"], 1)
        self.assertEqual(metrics["brand_citation_rate"], 100.0)
        self.assertEqual(metrics["brand_accuracy"], 50.0)

    def test_avg_accuracy_excludes_unchecked_rows(self):
        rows = [
            self._aggregate_row("checked", accuracy=0.5, accuracy_checked_facts=1),
            self._aggregate_row("unchecked", accuracy=1.0, accuracy_checked_facts=0),
        ]

        metrics = aggregate_slice(rows)

        self.assertEqual(metrics["avg_accuracy"], 0.5)
        self.assertEqual(metrics["accuracy_coverage"], 0.5)

    def test_new_competitor_aliases_match(self):
        aliases = {
            "Aurora": "Aurora MySQL",
            "AuroraDSQL": "Amazon Aurora DSQL",
            "RDS": "AWS RDS",
            "MariaDB": "Maria DB",
            "Percona": "Percona Server",
            "SingleStore": "Single Store",
            "Weaviate": "Weaviate",
            "Qdrant": "Qdrant",
            "Milvus": "Zilliz",
            "Pinecone": "Pinecone",
            "Chroma": "ChromaDB",
            "Vespa": "Vespa",
            "Redis": "RediSearch",
            "pgvector": "pgvector",
            "Elasticsearch": "Elastic Search",
            "OpenSearch": "OpenSearch",
            "Vitess": "Vitess",
            "Databricks": "Databricks",
            "OceanBase": "Ocean Base",
            "PlanetScale": "Planet Scale",
            "ClickHouse": "Click House",
            "Druid": "Apache Druid",
            "Pinot": "Apache Pinot",
            "TimescaleDB": "Timescale",
            "StarRocks": "Star Rocks",
            "MongoDB": "MongoDB Atlas",
            "MySQL": "My SQL",
            "PostgreSQL": "pgsql",
        }
        for target, text in aliases.items():
            with self.subTest(target=target):
                self.assertIn(target, product_positions(text))

        urls = {
            "Weaviate": "https://weaviate.io/developers/weaviate",
            "Qdrant": "https://qdrant.tech/documentation/",
            "Milvus": "https://github.com/milvus-io/milvus",
            "Pinecone": "https://www.pinecone.io/learn/",
            "Chroma": "https://www.trychroma.com/",
            "Vespa": "https://vespa.ai/",
            "Redis": "https://redis.io/docs/",
            "pgvector": "https://github.com/pgvector/pgvector",
            "Elasticsearch": "https://www.elastic.co/elasticsearch",
            "OpenSearch": "https://opensearch.org/docs/",
            "Vitess": "https://vitess.io/docs/",
            "Databricks": "https://www.databricks.com/product",
            "OceanBase": "https://en.oceanbase.com/docs/",
        }
        for target, url in urls.items():
            with self.subTest(target=target, url=url):
                self.assertTrue(is_product_related_url(target, url))
        self.assertFalse(is_product_related_url("Neon", "https://neonscience.org/"))

    def test_product_in_prompt_uses_alias_boundaries(self):
        prompt = {"prompt_text": "How is chromatography data stored?"}

        self.assertFalse(product_in_prompt(prompt, "Chroma"))
        self.assertTrue(product_in_prompt({"prompt_text": "How does ChromaDB work?"}, "Chroma"))

    def test_aurora_dsql_does_not_double_count_as_aurora(self):
        positions = product_positions("Amazon Aurora DSQL is a distributed SQL service.")

        self.assertIn("AuroraDSQL", positions)
        self.assertNotIn("Aurora", positions)

    def test_aurora_general_product_url_matches(self):
        self.assertTrue(
            is_product_related_url("Aurora", "https://aws.amazon.com/rds/aurora/features/")
        )

    def test_incumbents_do_not_win_competitive_prompts(self):
        prompt = {"prompt_type": "competitive"}

        self.assertEqual(
            competitive_winner("MySQL compatible, but TiDB is the best choice.", prompt),
            "TiDB",
        )

    def test_tidb_family_aliases_match(self):
        for alias in ["PyTiDB", "TiKV", "TiFlash", "mem9", "TiDB Cloud Filesystem"]:
            with self.subTest(alias=alias):
                self.assertIn("TiDB", product_positions(alias))

    def test_august_figures_unchanged(self):
        data_path = (
            Path(__file__).resolve().parents[1]
            / "geo-benchmark"
            / "runs"
            / "2026-08"
            / "scored_answers.jsonl"
        )
        rows = read_jsonl(data_path)
        expected = {
            "CockroachDB": (24.84, 15.46, 21.67),
            "TiDB": (21.31, 8.24, 11.67),
            "YugabyteDB": (14.97, 12.26, 8.33),
            "Neon": (14.44, 10.53, 8.33),
            "Supabase": (19.28, 14.65, 15.00),
            "PlanetScale": (3.99, 3.12, 3.33),
        }

        for target, published in expected.items():
            with self.subTest(target=target):
                metrics = aggregate_slice([row for row in rows if row["target"] == target])
                actual = (
                    metrics["answer_share"],
                    metrics["citation_authority"],
                    metrics["qualified_recommendation_rate"],
                )
                self.assertEqual(actual, published)

    def test_cost_estimate_counts_requests(self):
        prompts = [{"prompt_text": "best distributed SQL database"} for _ in range(10)]
        estimate = estimate_planned_cost(prompts, ["openai"], 3, DEFAULT_MODELS, DEFAULT_PRICING, 700)
        self.assertEqual(estimate["providers"][0]["requests"], 30)
        self.assertGreater(estimate["total_estimated_cost_usd"], 0)

    def test_cost_estimate_adds_web_search_fee_when_enabled(self):
        prompts = [{"prompt_text": "best distributed SQL database"} for _ in range(10)]

        estimate = estimate_planned_cost(prompts, ["openai"], 3, DEFAULT_MODELS, DEFAULT_PRICING, 700, "on")

        self.assertEqual(estimate["providers"][0]["web_search_requests"], 30)
        self.assertGreater(estimate["providers"][0]["estimated_cost_usd"], 0.3)

    def test_actual_cost_matches_versioned_model_name(self):
        raw = [
            {
                "status": "ok",
                "model_surface": "openai",
                "model_name": "gpt-5-mini-2025-08-07",
                "input_tokens": 1000,
                "output_tokens": 1000,
            }
        ]
        estimate = estimate_actual_cost(raw, DEFAULT_PRICING)
        self.assertGreater(estimate["total_estimated_cost_usd"], 0)

    def test_openai_web_search_on_uses_responses_api_low_mode(self):
        prompt = {"prompt_id": "p1", "prompt_text": "Which database category fits fresh operational analytics?"}
        config = {"model": "gpt-5-mini", "env_var": "OPENAI_API_KEY", "web_search": "on", "max_output_tokens": 100}
        captured = {}

        def fake_post(endpoint, payload, headers):
            captured["endpoint"] = endpoint
            captured["payload"] = payload
            return {
                "model": "gpt-5-mini-2026-08-01",
                "output_text": "TiDB is one option.",
                "output": [
                    {"type": "web_search_call"},
                    {"type": "message", "content": [{"type": "output_text", "text": "TiDB is one option."}]},
                ],
                "usage": {"input_tokens": 10, "output_tokens": 5},
                "sources": [{"url": "https://docs.pingcap.com/tidb/stable"}],
            }

        old_key = os.environ.get("OPENAI_API_KEY")
        try:
            os.environ["OPENAI_API_KEY"] = "test-key"
            with patch("geo_benchmark.providers._post_json", fake_post):
                result = OpenAIProvider("openai", config).generate(prompt, 1)
        finally:
            restore_env("OPENAI_API_KEY", old_key)

        self.assertTrue(captured["endpoint"].endswith("/v1/responses"))
        self.assertEqual(captured["payload"]["tools"], [{"type": "web_search", "search_context_size": "low"}])
        self.assertEqual(captured["payload"]["max_tool_calls"], 1)
        self.assertGreaterEqual(captured["payload"]["max_output_tokens"], 4000)
        self.assertEqual(result.web_search_requests, 1)
        self.assertIn("https://docs.pingcap.com/tidb/stable", result.citations)

    def test_post_json_wraps_socket_timeout_as_retryable_provider_error(self):
        with patch("urllib.request.urlopen", side_effect=socket.timeout("read timed out")):
            with self.assertRaises(ProviderError) as ctx:
                _post_json("https://api.example.test", {"ok": True}, {})

        self.assertTrue(ctx.exception.retryable)
        self.assertIn("request timed out", str(ctx.exception))

    def test_openai_web_search_off_uses_responses_api_without_tools(self):
        prompt = {"prompt_id": "p1", "prompt_text": "Which database category fits fresh operational analytics?"}
        config = {"model": "gpt-5-mini", "env_var": "OPENAI_API_KEY", "web_search": "off", "max_output_tokens": 100}
        captured = {}

        def fake_post(endpoint, payload, headers):
            captured["endpoint"] = endpoint
            captured["payload"] = payload
            return {
                "model": "gpt-5-mini-2026-08-01",
                "output_text": "TiDB is one option.",
                "output": [
                    {"type": "message", "content": [{"type": "output_text", "text": "TiDB is one option."}]},
                ],
                "usage": {"input_tokens": 10, "output_tokens": 5},
            }

        old_key = os.environ.get("OPENAI_API_KEY")
        try:
            os.environ["OPENAI_API_KEY"] = "test-key"
            with patch("geo_benchmark.providers._post_json", fake_post):
                result = OpenAIProvider("openai", config).generate(prompt, 1)
        finally:
            restore_env("OPENAI_API_KEY", old_key)

        self.assertTrue(captured["endpoint"].endswith("/v1/responses"))
        self.assertNotIn("tools", captured["payload"])
        self.assertNotIn("max_tool_calls", captured["payload"])
        self.assertGreaterEqual(captured["payload"]["max_output_tokens"], 4000)
        self.assertEqual(result.web_search_requests, 0)

    def test_anthropic_web_search_on_adds_server_tool(self):
        prompt = {"prompt_id": "p1", "prompt_text": "Which database category fits fresh operational analytics?"}
        config = {"model": "claude-sonnet-5", "env_var": "ANTHROPIC_API_KEY", "web_search": "on", "max_output_tokens": 100}
        captured = {}

        def fake_post(endpoint, payload, headers):
            captured["payload"] = payload
            return {
                "model": "claude-sonnet-5",
                "content": [
                    {"type": "server_tool_use", "name": "web_search"},
                    {
                        "type": "text",
                        "text": "TiDB is one option.",
                        "citations": [{"type": "web_search_result_location", "url": "https://docs.pingcap.com/tidb/stable"}],
                    },
                ],
                "usage": {"input_tokens": 10, "output_tokens": 5},
            }

        old_key = os.environ.get("ANTHROPIC_API_KEY")
        try:
            os.environ["ANTHROPIC_API_KEY"] = "test-key"
            with patch("geo_benchmark.providers._post_json", fake_post):
                result = AnthropicProvider("anthropic", config).generate(prompt, 1)
        finally:
            restore_env("ANTHROPIC_API_KEY", old_key)

        self.assertEqual(
            captured["payload"]["tools"],
            [{"type": "web_search_20250305", "name": "web_search", "max_uses": 1}],
        )
        self.assertEqual(result.web_search_requests, 1)
        self.assertIn("https://docs.pingcap.com/tidb/stable", result.citations)

    def test_seed_prompts_are_neutral_and_evidence_backed(self):
        prompts = generate_seed_prompts("2026-08", total=120, update_ratio=0.3)
        prompt_texts = [prompt["prompt_text"] for prompt in prompts]
        measured_brand_terms = [
            "tidb",
            "cockroachdb",
            "cockroach",
            "yugabytedb",
            "yugabyte",
            "supabase",
            "aurora",
            "spanner",
            "planetscale",
            "neon",
            "alloydb",
        ]
        self.assertEqual(len(prompt_texts), len(set(prompt_texts)))
        for prompt in prompts:
            lower_text = prompt["prompt_text"].lower()
            self.assertFalse(any(term in lower_text for term in measured_brand_terms))
            self.assertEqual(prompt["source"]["validation_status"], "case_pattern_validated")
            self.assertGreater(len(prompt["source"]["source_evidence_urls"]), 0)

    def test_prompt_validation_passes_seed_prompts(self):
        prompts = generate_seed_prompts("2026-08", total=120, update_ratio=0.3)

        self.assertEqual(prompt_validation_errors(prompts), [])

    def test_prompt_validation_fails_measured_product_leak(self):
        prompts = generate_seed_prompts("2026-08", total=120, update_ratio=0.3)
        prompts[0] = {
            **prompts[0],
            "brand_class": "non_branded",
            "prompt_text": prompts[0]["prompt_text"] + " Should we use TiDB?",
        }

        errors = prompt_validation_errors(prompts)

        self.assertTrue(any("measured product term 'tidb'" in error for error in errors))

    def test_prompt_validation_allows_branded_prompt_naming_tidb(self):
        prompts = generate_seed_prompts("2026-08", total=120, update_ratio=0.3)
        prompts[0] = {
            **prompts[0],
            "brand_class": "branded",
            "prompt_text": "What is TiDB Cloud Zero?",
        }

        errors = prompt_validation_errors(prompts)

        self.assertFalse(any("measured product term" in error for error in errors))

    def test_prompt_validation_defaults_to_non_branded(self):
        """A prompt with no brand_class is still checked, so old files behave as before."""
        prompts = generate_seed_prompts("2026-08", total=120, update_ratio=0.3)
        prompts[0] = {**prompts[0], "prompt_text": "Is TiDB a good choice?"}
        prompts[0].pop("brand_class", None)

        errors = prompt_validation_errors(prompts)

        self.assertTrue(any("measured product term 'tidb'" in error for error in errors))

    def test_prompt_validation_rejects_invalid_brand_class(self):
        prompts = generate_seed_prompts("2026-08", total=120, update_ratio=0.3)
        prompts[0] = {**prompts[0], "brand_class": "Branded "}

        errors = prompt_validation_errors(prompts)

        self.assertFalse(any("brand_class must be" in error for error in errors))

        prompts[0] = {**prompts[0], "brand_class": "brandd"}
        errors = prompt_validation_errors(prompts)

        self.assertTrue(any("brand_class must be" in error for error in errors))

    def test_prompt_validation_fails_serverless_ai_postgres_leak(self):
        prompts = generate_seed_prompts("2026-08", total=120, update_ratio=0.3)
        index = next(index for index, prompt in enumerate(prompts) if prompt["use_case"] == "serverless_ai")
        prompts[index] = {**prompts[index], "prompt_text": prompts[index]["prompt_text"] + " Compare pgvector."}

        errors = prompt_validation_errors(prompts)

        self.assertTrue(any("serverless_ai prompt_text contains banned term 'pgvector'" in error for error in errors))

    def test_default_targets_include_competitive_set(self):
        self.assertEqual(
            DEFAULT_TARGETS["targets"],
            ["TiDB", "CockroachDB", "YugabyteDB", "Supabase", "PlanetScale", "Neon"],
        )

    def test_ai_infra_prompts_cover_backend_serverless_and_operational_subtypes(self):
        prompts = generate_seed_prompts("2026-08", total=120, update_ratio=0.3)
        ai_prompts = [prompt for prompt in prompts if prompt["prompt_type"] == "ai_infra"]
        use_cases = {prompt["use_case"] for prompt in ai_prompts}
        prompt_text = "\n".join(prompt["prompt_text"].lower() for prompt in ai_prompts)

        self.assertEqual(len(ai_prompts), 30)
        self.assertEqual(use_cases, {"ai_app_backend", "serverless_ai", "operational_ai_data"})
        self.assertIn("auth", prompt_text)
        serverless_text = "\n".join(
            prompt["prompt_text"].lower()
            for prompt in ai_prompts
            if prompt["use_case"] == "serverless_ai"
        )
        self.assertIn("serverless ai app", serverless_text)
        self.assertNotIn("postgres", serverless_text)
        self.assertNotIn("pgvector", serverless_text)
        self.assertIn("fresh operational data", prompt_text)

    def test_load_env_files_reads_local_file_without_overriding_existing_env(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".env.local").write_text(
                "OPENAI_API_KEY=from_file\nANTHROPIC_API_KEY='quoted_value'\n",
                encoding="utf-8",
            )
            old_openai = os.environ.get("OPENAI_API_KEY")
            old_anthropic = os.environ.get("ANTHROPIC_API_KEY")
            try:
                os.environ["OPENAI_API_KEY"] = "existing"
                os.environ.pop("ANTHROPIC_API_KEY", None)
                load_env_files([root])
                self.assertEqual(os.environ["OPENAI_API_KEY"], "existing")
                self.assertEqual(os.environ["ANTHROPIC_API_KEY"], "quoted_value")
            finally:
                restore_env("OPENAI_API_KEY", old_openai)
                restore_env("ANTHROPIC_API_KEY", old_anthropic)

    def test_retry_errors_replaces_failed_raw_answer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prepare(root, "2026-08", 20, 0.3, False)
            prompts = read_json(root / "prompts" / "2026-08" / "prompts.json")
            failed_prompt = prompts[0]
            ok_prompt = prompts[1]
            failed_answer_id = stable_hash(["2026-08", failed_prompt["prompt_id"], "mock", 1])[:24]
            ok_answer_id = stable_hash(["2026-08", ok_prompt["prompt_id"], "mock", 1])[:24]
            raw_path = root / "runs" / "2026-08" / "raw_answers.jsonl"
            write_jsonl(
                raw_path,
                [
                    {
                        "answer_id": failed_answer_id,
                        "run_id": "failed-run",
                        "status": "error",
                        "month": "2026-08",
                        "prompt_id": failed_prompt["prompt_id"],
                        "prompt_text": failed_prompt["prompt_text"],
                        "model_surface": "mock",
                        "model_name": "mock-geo-buyer-v1",
                        "run_index": 1,
                        "timestamp": "2026-08-01T00:00:00+00:00",
                        "error": "synthetic failure",
                    },
                    {
                        "answer_id": ok_answer_id,
                        "run_id": "ok-run",
                        "status": "ok",
                        "month": "2026-08",
                        "prompt_id": ok_prompt["prompt_id"],
                        "prompt_text": ok_prompt["prompt_text"],
                        "model_surface": "mock",
                        "model_name": "mock-geo-buyer-v1",
                        "run_index": 1,
                        "timestamp": "2026-08-01T00:00:00+00:00",
                        "raw_answer": "Existing answer",
                        "raw_citations": [],
                    },
                ],
            )

            result = retry_errors(root, "2026-08", "mock", None, None, 0)
            raw = read_jsonl(raw_path)

            self.assertEqual(result["attempted"], 1)
            self.assertEqual(result["succeeded"], 1)
            self.assertEqual(raw[0]["status"], "ok")
            self.assertEqual(raw[0]["answer_id"], failed_answer_id)
            self.assertEqual(raw[0]["retry_of_run_id"], "failed-run")
            self.assertEqual(raw[1]["raw_answer"], "Existing answer")

    def test_configured_fallback_recovers_eligible_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prepare(root, "2026-08", 20, 0.3, False)
            models = read_json(root / "config" / "models.json")
            models["mock"]["fallback_model"] = "mock-geo-buyer-v1"
            models["mock"]["fallback_max_output_tokens"] = 700
            write_json(root / "config" / "models.json", models)

            prompts = read_json(root / "prompts" / "2026-08" / "prompts.json")
            prompt = prompts[0]
            answer_id = stable_hash(["2026-08", prompt["prompt_id"], "mock", 1])[:24]
            raw_path = root / "runs" / "2026-08" / "raw_answers.jsonl"
            write_jsonl(
                raw_path,
                [
                    {
                        "answer_id": answer_id,
                        "run_id": "failed-run",
                        "status": "error",
                        "month": "2026-08",
                        "prompt_id": prompt["prompt_id"],
                        "prompt_text": prompt["prompt_text"],
                        "model_surface": "mock",
                        "model_name": "mock-geo-buyer-v1",
                        "run_index": 1,
                        "timestamp": "2026-08-01T00:00:00+00:00",
                        "error": "request timed out",
                    }
                ],
            )

            results = retry_configured_errors(root, "2026-08", ["mock"], 0)
            raw = read_jsonl(raw_path)

            self.assertEqual(results[0]["attempted"], 1)
            self.assertEqual(results[0]["succeeded"], 1)
            self.assertEqual(raw[0]["status"], "ok")
            self.assertEqual(raw[0]["retry_model_override"], "mock-geo-buyer-v1")

    def test_filtered_collect_preserves_other_raw_answers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prepare(root, "2026-08", 20, 0.3, False)
            prompts = read_json(root / "prompts" / "2026-08" / "prompts.json")
            pain_prompt = next(prompt for prompt in prompts if prompt["prompt_type"] == "pain_point")
            ai_prompt = next(prompt for prompt in prompts if prompt["prompt_type"] == "ai_infra")
            raw_path = root / "runs" / "2026-08" / "raw_answers.jsonl"
            write_jsonl(
                raw_path,
                [
                    {
                        "answer_id": stable_hash(["2026-08", pain_prompt["prompt_id"], "mock", 1])[:24],
                        "run_id": "keep-me",
                        "status": "ok",
                        "month": "2026-08",
                        "prompt_id": pain_prompt["prompt_id"],
                        "prompt_text": pain_prompt["prompt_text"],
                        "model_surface": "mock",
                        "model_name": "mock-geo-buyer-v1",
                        "run_index": 1,
                        "timestamp": "2026-08-01T00:00:00+00:00",
                        "raw_answer": "Existing pain answer",
                        "raw_citations": [],
                    },
                    {
                        "answer_id": stable_hash(["2026-08", ai_prompt["prompt_id"], "mock", 1])[:24],
                        "run_id": "replace-me",
                        "status": "ok",
                        "month": "2026-08",
                        "prompt_id": ai_prompt["prompt_id"],
                        "prompt_text": ai_prompt["prompt_text"],
                        "model_surface": "mock",
                        "model_name": "mock-geo-buyer-v1",
                        "run_index": 1,
                        "timestamp": "2026-08-01T00:00:00+00:00",
                        "raw_answer": "Old AI answer",
                        "raw_citations": [],
                    },
                ],
            )

            prompt_ids = selected_prompt_ids(root, "2026-08", "ai_infra", None)
            collect(root, "2026-08", ["mock"], 1, 0, True, prompt_ids)
            raw = read_jsonl(raw_path)
            by_prompt = {row["prompt_id"]: row for row in raw}

            self.assertEqual(by_prompt[pain_prompt["prompt_id"]]["raw_answer"], "Existing pain answer")
            self.assertNotEqual(by_prompt[ai_prompt["prompt_id"]]["raw_answer"], "Old AI answer")

    def test_auto_fallback_skips_auth_and_quota_errors(self):
        self.assertFalse(fallback_error_is_eligible({"error": "Missing OPENAI_API_KEY"}))
        self.assertFalse(fallback_error_is_eligible({"error": "HTTP 429: insufficient_quota"}))
        self.assertTrue(fallback_error_is_eligible({"error": "OpenAI returned empty content"}))

    def test_report_writes_single_markdown_with_stable_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            report_dir = Path(tmp)
            summary = {
                "target_order": ["TiDB", "CockroachDB"],
                "targets": {
                    "TiDB": {
                        "overall": {
                            "answer_share": 20,
                            "citation_authority": 10,
                            "qualified_recommendation_rate": 5,
                            "prompt_count": 2,
                            "answer_count": 2,
                        },
                        "unchanged": {
                            "answer_share": 25,
                            "citation_authority": 11,
                            "qualified_recommendation_rate": 6,
                            "prompt_count": 1,
                            "answer_count": 1,
                        },
                        "by_prompt_type": {},
                        "by_model": {},
                        "by_use_case": {},
                        "competitive": {},
                    },
                    "CockroachDB": {
                        "overall": {
                            "answer_share": 40,
                            "citation_authority": 30,
                            "qualified_recommendation_rate": 20,
                            "prompt_count": 2,
                            "answer_count": 2,
                        },
                        "unchanged": {
                            "answer_share": 42,
                            "citation_authority": 31,
                            "qualified_recommendation_rate": 21,
                            "prompt_count": 1,
                            "answer_count": 1,
                        },
                        "by_prompt_type": {},
                        "by_model": {},
                        "by_use_case": {},
                        "competitive": {},
                    },
                },
            }
            write_reports(report_dir, "2026-08", summary, [], {"total_estimated_cost_usd": 0, "pricing_version": "test"})

            markdown_files = sorted(path.name for path in report_dir.glob("*.md"))
            report_text = (report_dir / "llm-report.md").read_text(encoding="utf-8")

            self.assertEqual(markdown_files, ["llm-report.md"])
            self.assertIn("| Target | Answer Share | Citation Authority | Recommendation Rate | Stable Answer Share | Stable Recommendation Rate |", report_text)
            self.assertNotIn("Top 3", report_text)
            self.assertNotIn("Not Mentioned", report_text)


def restore_env(key: str, value: Optional[str]) -> None:
    if value is None:
        os.environ.pop(key, None)
    else:
        os.environ[key] = value


if __name__ == "__main__":
    unittest.main()
