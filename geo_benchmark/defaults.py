from __future__ import annotations


DEFAULT_MODELS = {
    "mock": {
        "provider": "mock",
        "model": "mock-geo-buyer-v1",
        "temperature": 0.2,
        "max_output_tokens": 700,
        "env_var": None,
    },
    "openai": {
        "provider": "openai",
        "model": "gpt-5-mini",
        "temperature": None,
        "max_output_tokens": 1600,
        "env_var": "OPENAI_API_KEY",
        "fallback_model": "gpt-4o-mini",
        "fallback_max_output_tokens": 1000,
        "fallback_retries": 1,
    },
    "anthropic": {
        "provider": "anthropic",
        "model": "claude-sonnet-5",
        "temperature": None,
        "max_output_tokens": 700,
        "env_var": "ANTHROPIC_API_KEY",
    },
    "gemini": {
        "provider": "gemini",
        "model": "gemini-2.5-flash-lite",
        "temperature": 0.2,
        "max_output_tokens": 700,
        "env_var": "GEMINI_API_KEY",
    },
    "perplexity": {
        "provider": "perplexity",
        "model": "sonar",
        "temperature": 0.2,
        "max_output_tokens": 700,
        "env_var": "PERPLEXITY_API_KEY",
        "search_context_size": "low",
    },
}


DEFAULT_TARGETS = {
    "targets": ["TiDB", "CockroachDB", "YugabyteDB", "Supabase", "PlanetScale", "Neon"]
}


DEFAULT_PRICING = {
    "pricing_version": "2026-07-30",
    "currency": "USD",
    "notes": [
        "Prices are editable planning defaults; always verify provider billing pages before a production run.",
        "Per-token prices are per 1M tokens. Per-request prices are per request.",
    ],
    "models": {
        "gpt-5-mini": {
            "input_per_1m": 0.25,
            "output_per_1m": 2.00,
            "request_fee": 0.0,
            "web_search_fee": 0.01,
            "source": "https://openai.com/index/introducing-gpt-5-for-developers/",
        },
        "gpt-4o-mini": {
            "input_per_1m": 0.15,
            "output_per_1m": 0.60,
            "request_fee": 0.0,
            "web_search_fee": 0.01,
            "source": "https://developers.openai.com/api/docs/models/gpt-4o-mini",
        },
        "claude-sonnet-5": {
            "input_per_1m": 2.00,
            "output_per_1m": 10.00,
            "request_fee": 0.0,
            "web_search_fee": 0.01,
            "source": "https://claude.com/pricing",
        },
        "gemini-2.5-flash-lite": {
            "input_per_1m": 0.10,
            "output_per_1m": 0.40,
            "request_fee": 0.0,
            "source": "https://ai.google.dev/gemini-api/docs/pricing",
        },
        "sonar": {
            "input_per_1m": 1.00,
            "output_per_1m": 1.00,
            "request_fee": 0.005,
            "source": "https://docs.perplexity.ai/docs/getting-started/pricing",
        },
        "sonar-pro": {
            "input_per_1m": 3.00,
            "output_per_1m": 15.00,
            "request_fee": 0.006,
            "source": "https://docs.perplexity.ai/docs/getting-started/pricing",
        },
        "mock-geo-buyer-v1": {
            "input_per_1m": 0.0,
            "output_per_1m": 0.0,
            "request_fee": 0.0,
            "source": "local mock provider",
        },
    },
}


DEFAULT_SOURCE_AUTHORITY = {
    "source_authority_version": "2026-09-02",
    "rules": [
        {"contains": "docs.pingcap.com", "weight": 1.0, "label": "official_docs"},
        {"contains": "pingcap.com", "weight": 1.0, "label": "official_site"},
        {"contains": "tidb.net", "weight": 1.0, "label": "official_community"},
        {"contains": "github.com/pingcap", "weight": 1.0, "label": "github"},
        {"contains": "mem9.ai", "weight": 1.0, "label": "official_site"},
        {"contains": "drive9.ai", "weight": 1.0, "label": "official_site"},
        {"contains": "tidb.io", "weight": 1.0, "label": "official_site"},
        {"contains": "cockroachlabs.com/docs", "weight": 1.0, "label": "official_docs"},
        {"contains": "cockroachlabs.com", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/cockroachdb", "weight": 1.0, "label": "github"},
        {"contains": "docs.yugabyte.com", "weight": 1.0, "label": "official_docs"},
        {"contains": "yugabyte.com", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/yugabyte", "weight": 1.0, "label": "github"},
        {"contains": "cloud.google.com/spanner", "weight": 1.0, "label": "official_docs"},
        {"contains": "cloud.google.com/alloydb", "weight": 1.0, "label": "official_docs"},
        {"contains": "oceanbase.com", "weight": 1.0, "label": "official_site"},
        {"contains": "singlestore.com", "weight": 1.0, "label": "official_site"},
        {"contains": "docs.aws.amazon.com/aurora-dsql/", "weight": 1.0, "label": "official_docs"},
        {
            "contains": "docs.aws.amazon.com/amazonrds/latest/aurorauserguide/",
            "weight": 1.0,
            "label": "official_docs",
        },
        {
            "contains": "docs.aws.amazon.com/amazonrds/latest/userguide/",
            "weight": 1.0,
            "label": "official_docs",
        },
        {"contains": "aws.amazon.com/rds/aurora/dsql/", "weight": 1.0, "label": "official_site"},
        {"contains": "aws.amazon.com/marketplace", "weight": 1.0, "label": "marketplace"},
        {"contains": "aws.amazon.com", "weight": 0.9, "label": "cloud_partner"},
        {"contains": "mariadb.org", "weight": 1.0, "label": "official_site"},
        {"contains": "mariadb.com", "weight": 1.0, "label": "official_site"},
        {"contains": "percona.com", "weight": 1.0, "label": "official_site"},
        {"contains": "vitess.io", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/vitessio", "weight": 1.0, "label": "github"},
        {"contains": "planetscale.com/docs", "weight": 1.0, "label": "official_docs"},
        {"contains": "planetscale.com", "weight": 1.0, "label": "official_site"},
        {"contains": "supabase.com/docs", "weight": 1.0, "label": "official_docs"},
        {"contains": "supabase.com", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/supabase", "weight": 1.0, "label": "github"},
        {"contains": "neon.tech/docs", "weight": 1.0, "label": "official_docs"},
        {"contains": "neon.tech", "weight": 1.0, "label": "official_site"},
        {"contains": "pinecone.io", "weight": 1.0, "label": "official_site"},
        {"contains": "weaviate.io", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/weaviate", "weight": 1.0, "label": "github"},
        {"contains": "qdrant.tech", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/qdrant", "weight": 1.0, "label": "github"},
        {"contains": "milvus.io", "weight": 1.0, "label": "official_site"},
        {"contains": "zilliz.com", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/milvus-io", "weight": 1.0, "label": "github"},
        {"contains": "trychroma.com", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/chroma-core", "weight": 1.0, "label": "github"},
        {"contains": "vespa.ai", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/vespa-engine", "weight": 1.0, "label": "github"},
        {"contains": "github.com/pgvector", "weight": 1.0, "label": "github"},
        {"contains": "redis.io", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/redis", "weight": 1.0, "label": "github"},
        {"contains": "elastic.co", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/elastic", "weight": 1.0, "label": "github"},
        {"contains": "opensearch.org", "weight": 1.0, "label": "official_site"},
        {"contains": "clickhouse.com", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/clickhouse", "weight": 1.0, "label": "github"},
        {"contains": "druid.apache.org", "weight": 1.0, "label": "official_site"},
        {"contains": "pinot.apache.org", "weight": 1.0, "label": "official_site"},
        {"contains": "startree.ai", "weight": 1.0, "label": "official_site"},
        {"contains": "docs.tigerdata.com", "weight": 1.0, "label": "official_docs"},
        {"contains": "timescale.com", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/timescale", "weight": 1.0, "label": "github"},
        {"contains": "starrocks.io", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/starrocks", "weight": 1.0, "label": "github"},
        {"contains": "mongodb.com", "weight": 1.0, "label": "official_site"},
        {"contains": "github.com/mongodb", "weight": 1.0, "label": "github"},
        {"contains": "docs.snowflake.com", "weight": 1.0, "label": "official_docs"},
        {"contains": "snowflake.com", "weight": 1.0, "label": "official_site"},
        {"contains": "docs.databricks.com", "weight": 1.0, "label": "official_docs"},
        {"contains": "databricks.com", "weight": 1.0, "label": "official_site"},
        {"contains": "dev.mysql.com", "weight": 1.0, "label": "official_docs"},
        {"contains": "mysql.com", "weight": 1.0, "label": "official_site"},
        {"contains": "postgresql.org", "weight": 1.0, "label": "official_site"},
        {"contains": "gartner.com", "weight": 0.8, "label": "analyst"},
        {"contains": "forrester.com", "weight": 0.8, "label": "analyst"},
        {"contains": "medium.com", "weight": 0.5, "label": "third_party_blog"},
        {"contains": "dev.to", "weight": 0.5, "label": "third_party_blog"},
        {"contains": "stackoverflow.com", "weight": 0.2, "label": "forum"},
    ],
    "default_weight": 0.2,
}


DEFAULT_FACTS = {
    "facts_version": "2026-07-30",
    "targets": {
        "TiDB": [
            {
                "fact_id": "distributed_sql",
                "triggers": ["tidb", "distributed sql", "distributed database", "scale-out", "horizontal"],
                "expected_any": ["distributed sql", "distributed database", "horizontal", "scale-out"],
                "wrong_any": ["single-node only", "not distributed"],
            },
            {
                "fact_id": "mysql_compatibility",
                "triggers": ["tidb", "mysql", "compatibility", "compatible"],
                "expected_any": ["mysql", "compatible"],
                "wrong_any": ["postgres-compatible", "postgres compatible", "only postgresql"],
            },
            {
                "fact_id": "htap",
                "triggers": ["tidb", "htap", "real-time analytics", "analytics"],
                "expected_any": ["htap", "tiflash", "real-time analytics", "transactional and analytical"],
                "wrong_any": ["oltp only", "no analytics"],
            },
            {
                "fact_id": "vector_search",
                "triggers": ["tidb", "vector", "embedding", "semantic search"],
                "expected_any": ["vector", "embedding", "semantic"],
                "wrong_any": ["does not support vector", "no vector"],
            },
        ],
        "CockroachDB": [
            {
                "fact_id": "distributed_sql",
                "triggers": ["cockroachdb", "distributed sql", "distributed database", "scale-out", "horizontal"],
                "expected_any": ["distributed sql", "distributed database", "horizontal", "scale-out"],
                "wrong_any": ["single-node only", "not distributed"],
            },
            {
                "fact_id": "postgres_compatibility",
                "triggers": ["cockroachdb", "postgres", "postgresql", "compatibility", "compatible"],
                "expected_any": ["postgres", "postgresql", "compatible"],
                "wrong_any": ["mysql-compatible", "mysql compatible", "only mysql"],
            },
            {
                "fact_id": "multi_region",
                "triggers": ["cockroachdb", "multi-region", "global", "resilience"],
                "expected_any": ["multi-region", "global", "resilience", "distributed"],
                "wrong_any": ["single-region only"],
            },
        ],
        "YugabyteDB": [
            {
                "fact_id": "distributed_sql",
                "triggers": ["yugabytedb", "yugabyte", "distributed sql", "distributed database", "scale-out", "horizontal"],
                "expected_any": ["distributed sql", "distributed database", "horizontal", "scale-out", "distributed"],
                "wrong_any": ["single-node only", "not distributed"],
            },
            {
                "fact_id": "postgres_compatibility",
                "triggers": ["yugabytedb", "yugabyte", "postgres", "postgresql", "compatibility", "compatible"],
                "expected_any": ["postgres", "postgresql", "compatible"],
                "wrong_any": ["mysql-compatible only", "only mysql"],
            },
        ],
        "Supabase": [
            {
                "fact_id": "postgres_app_platform",
                "triggers": ["supabase", "postgres", "postgresql", "app platform", "auth", "realtime"],
                "expected_any": ["postgres", "postgresql", "auth", "storage", "realtime", "app platform"],
                "wrong_any": ["mysql-compatible", "mysql compatible", "not postgres"],
            },
            {
                "fact_id": "vector_app_development",
                "triggers": ["supabase", "vector", "embedding", "semantic search"],
                "expected_any": ["vector", "embedding", "semantic", "pgvector"],
                "wrong_any": ["does not support vector", "no vector"],
            },
        ],
        "PlanetScale": [
            {
                "fact_id": "mysql_workflow",
                "triggers": ["planetscale", "mysql", "vitess", "branching"],
                "expected_any": ["mysql", "vitess", "branching", "developer workflow"],
                "wrong_any": ["postgres-compatible", "postgres compatible", "only postgresql"],
            },
            {
                "fact_id": "managed_scaling",
                "triggers": ["planetscale", "scale", "scaling", "serverless"],
                "expected_any": ["scale", "scaling", "serverless", "managed"],
                "wrong_any": ["single-node only"],
            },
        ],
        "Neon": [
            {
                "fact_id": "serverless_postgres",
                "triggers": ["neon", "postgres", "postgresql", "serverless", "branching"],
                "expected_any": ["postgres", "postgresql", "serverless", "branching"],
                "wrong_any": ["mysql-compatible", "mysql compatible", "not postgres"],
            },
        ],
    },
}
