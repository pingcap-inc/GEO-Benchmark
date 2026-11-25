# GEO Benchmark LLM Report - 2026-10

Providers: mock
Web search mode: off
Saved raw records: 219
Successfully scored answers: 219
Failed raw records: 0
Incomplete raw records: 0
Scored target-answer rows: 7884

> Warning: this report includes mock provider output. Use it only as a pipeline smoke test, not as a market benchmark.

## Executive KPI

| Target | Consideration Rate | Mention Rate | Prominence Score | Citation Authority | Recommendation Rate | Comparison Win Rate | Stable Consideration Rate | Stable Mention Rate | Stable Prominence Score | Stable Recommendation Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | N/A | 30.88 | 16.27 | 21.66 | 20.00 | 50.00% (n = 2) — low sample | N/A | 30.88 | 16.27 | 20.00 |
| TiDB | N/A | 43.21 | 28.64 | 34.32 | 34.57 | 64.00% (n = 50) | N/A | 43.21 | 28.64 | 34.57 |
| YugabyteDB | N/A | 36.24 | 21.16 | 24.72 | 30.53 | 0.00% (n = 1) — low sample | N/A | 36.24 | 21.16 | 30.53 |
| Neon | N/A | 36.45 | 18.85 | 20.00 | 20.47 | 60.00% (n = 5) — low sample | N/A | 36.45 | 18.85 | 20.47 |
| Supabase | N/A | 35.65 | 18.90 | 21.31 | 24.81 | 66.67% (n = 3) — low sample | N/A | 35.65 | 18.90 | 24.81 |
| PlanetScale | N/A | 32.41 | 19.20 | 23.35 | 23.26 | 0.00% (n = 3) — low sample | N/A | 32.41 | 19.20 | 23.26 |
| AlloyDB | N/A | 35.16 | 20.19 | 22.96 | 18.18 | N/A | N/A | 35.16 | 20.19 | 18.18 |
| Aurora | N/A | 33.18 | 20.15 | 24.48 | 16.15 | 0.00% (n = 1) — low sample | N/A | 33.18 | 20.15 | 16.15 |
| AuroraDSQL | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| Chroma | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| ClickHouse | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| Databricks | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| Druid | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| Elasticsearch | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 100.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| MariaDB | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| Milvus | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 33.33% (n = 3) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| MongoDB | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 2) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| MySQL | N/A | 75.77 | 24.12 | 0.00 | 31.19 | 20.00% (n = 10) | N/A | 75.77 | 24.12 | 31.19 |
| OceanBase | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| OpenSearch | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| Percona | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| Pinecone | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 50.00% (n = 2) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| Pinot | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| PostgreSQL | N/A | 82.41 | 17.09 | 0.00 | 4.65 | 50.00% (n = 2) — low sample | N/A | 82.41 | 17.09 | 4.65 |
| Qdrant | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| RDS | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| Redis | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| SingleStore | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 66.67% (n = 3) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| Snowflake | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| Spanner | N/A | 33.03 | 19.21 | 22.42 | 20.61 | 100.00% (n = 1) — low sample | N/A | 33.03 | 19.21 | 20.61 |
| StarRocks | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| TimescaleDB | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| Vespa | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| Vitess | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 100.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| Weaviate | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 100.00% (n = 2) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| pgvector | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 2) — low sample | N/A | 0.00 | 0.00 | 0.00 |

## Branded Accuracy

| Target | Prompts | Legacy accuracy | Legacy coverage | Semantic accuracy | Semantic decision coverage | Judge unavailable |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 2 | 100.00 | 100.00% | N/A | 0.00% | 0 |
| TiDB | 138 | 90.84 | 94.93% | N/A | 0.00% | 0 |
| YugabyteDB | 1 | 100.00 | 100.00% | N/A | 0.00% | 0 |
| Neon | 5 | 100.00 | 100.00% | N/A | 0.00% | 0 |
| Supabase | 3 | 100.00 | 100.00% | N/A | 0.00% | 0 |
| PlanetScale | 3 | 100.00 | 100.00% | N/A | 0.00% | 0 |
| Aurora | 2 | N/A | 0.00% | N/A | 0.00% | 0 |
| Chroma | 1 | N/A | 0.00% | N/A | 0.00% | 0 |
| Databricks | 1 | N/A | 0.00% | N/A | 0.00% | 0 |
| Elasticsearch | 1 | N/A | 0.00% | N/A | 0.00% | 0 |
| Milvus | 3 | N/A | 0.00% | N/A | 0.00% | 0 |
| MongoDB | 3 | N/A | 0.00% | N/A | 0.00% | 0 |
| MySQL | 25 | N/A | 0.00% | N/A | 0.00% | 0 |
| OpenSearch | 1 | N/A | 0.00% | N/A | 0.00% | 0 |
| Pinecone | 2 | N/A | 0.00% | N/A | 0.00% | 0 |
| PostgreSQL | 3 | N/A | 0.00% | N/A | 0.00% | 0 |
| Qdrant | 1 | N/A | 0.00% | N/A | 0.00% | 0 |
| RDS | 1 | N/A | 0.00% | N/A | 0.00% | 0 |
| SingleStore | 3 | N/A | 0.00% | N/A | 0.00% | 0 |
| Snowflake | 1 | N/A | 0.00% | N/A | 0.00% | 0 |
| Spanner | 1 | N/A | 0.00% | N/A | 0.00% | 0 |
| Vitess | 1 | N/A | 0.00% | N/A | 0.00% | 0 |
| Weaviate | 2 | N/A | 0.00% | N/A | 0.00% | 0 |
| pgvector | 5 | N/A | 0.00% | N/A | 0.00% | 0 |

Semantic results are written alongside legacy substring scores; they do not replace the official metric during shadow mode.

Overall columns use the saved scored answers in this report, which may be only a subset of the month. Stable columns use the stable subset; compare runs only when prompt and provider coverage also match.

Mention Rate uses non-branded answer rows (questions that do not name the target). Prominence and Citation Authority average those answers per prompt, then apply prompt weights. Recommendation Rate uses only qualifying non-branded recommendation answers. Consideration uses only non-branded answers with captured queries or confirmed no-search status. Branded accuracy uses branded answers with fact decisions; comparison win rate uses valid comparison answers.

N/A means no eligible observations; 0 means eligible observations were measured and the result was zero. CSV exports represent N/A as an empty cell; JSON uses null.

## Prompt-Type Breakdown

### Consideration Rate

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale | AlloyDB | Aurora | AuroraDSQL | Chroma | ClickHouse | Databricks | Druid | Elasticsearch | MariaDB | Milvus | MongoDB | MySQL | OceanBase | OpenSearch | Percona | Pinecone | Pinot | PostgreSQL | Qdrant | RDS | Redis | SingleStore | Snowflake | Spanner | StarRocks | TimescaleDB | Vespa | Vitess | Weaviate | pgvector |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `AI Agent Infrastructure` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `Competitive Comparisons` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `Deployment & Cloud` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `Enterprise & Compliance` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `Hybrid Search & RAG` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `MCP & Developer Tooling` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `MySQL Scale & Migration` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `Observability` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `Scale & Architecture` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `TiDB Brand & Definitions` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

### Mention Rate

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale | AlloyDB | Aurora | AuroraDSQL | Chroma | ClickHouse | Databricks | Druid | Elasticsearch | MariaDB | Milvus | MongoDB | MySQL | OceanBase | OpenSearch | Percona | Pinecone | Pinot | PostgreSQL | Qdrant | RDS | Redis | SingleStore | Snowflake | Spanner | StarRocks | TimescaleDB | Vespa | Vitess | Weaviate | pgvector |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `AI Agent Infrastructure` | 45.83 | 52.63 | 50.00 | 35.42 | 43.75 | 31.25 | 47.92 | 37.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 62.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 97.92 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 45.83 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Competitive Comparisons` | 0.00 | 0.00 | 0.00 | 3.57 | 0.00 | 0.00 | 3.12 | 3.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 32.26 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.23 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Deployment & Cloud` | 30.00 | N/A | 20.00 | 21.05 | 10.53 | 21.05 | 45.00 | 35.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 61.11 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 75.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 45.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Enterprise & Compliance` | 0.00 | 0.00 | 25.00 | 100.00 | 75.00 | 75.00 | 25.00 | 75.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 75.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 25.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Hybrid Search & RAG` | 35.90 | 43.75 | 38.46 | 30.77 | 30.77 | 25.64 | 33.33 | 25.64 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 83.78 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 72.97 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 28.21 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `MCP & Developer Tooling` | 40.00 | 25.00 | 50.00 | 50.00 | 60.00 | 60.00 | 30.00 | 40.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 55.56 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 40.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `MySQL Scale & Migration` | 38.46 | 45.45 | 53.85 | 53.85 | 76.92 | 53.85 | 23.08 | 38.46 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 50.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 23.08 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Observability` | 50.00 | N/A | 25.00 | 25.00 | 0.00 | 25.00 | 75.00 | 50.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 75.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 75.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Scale & Architecture` | 27.78 | 22.22 | 44.44 | 66.67 | 61.11 | 61.11 | 33.33 | 38.89 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 93.75 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 33.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `TiDB Brand & Definitions` | 29.03 | N/A | 45.16 | 48.39 | 38.71 | 41.94 | 48.39 | 48.39 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 74.19 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 96.77 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 38.71 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### Prominence Score

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale | AlloyDB | Aurora | AuroraDSQL | Chroma | ClickHouse | Databricks | Druid | Elasticsearch | MariaDB | Milvus | MongoDB | MySQL | OceanBase | OpenSearch | Percona | Pinecone | Pinot | PostgreSQL | Qdrant | RDS | Redis | SingleStore | Snowflake | Spanner | StarRocks | TimescaleDB | Vespa | Vitess | Weaviate | pgvector |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `AI Agent Infrastructure` | 26.79 | 31.60 | 31.32 | 21.51 | 19.62 | 17.92 | 26.42 | 28.49 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 13.58 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 19.43 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 28.30 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Competitive Comparisons` | 0.00 | 0.00 | 0.00 | 2.41 | 0.00 | 0.00 | 0.42 | 1.35 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 53.60 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 12.83 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.30 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Deployment & Cloud` | 18.95 | N/A | 8.42 | 15.56 | 6.67 | 9.63 | 27.37 | 24.56 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 21.57 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 16.84 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 26.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Enterprise & Compliance` | 0.00 | 0.00 | 30.00 | 56.00 | 68.00 | 48.00 | 4.00 | 22.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 16.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 20.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 12.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Hybrid Search & RAG` | 18.76 | 35.15 | 19.38 | 15.88 | 13.20 | 17.32 | 20.41 | 14.23 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 27.69 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 13.48 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 15.26 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `MCP & Developer Tooling` | 24.35 | 15.00 | 33.04 | 29.57 | 31.30 | 32.17 | 15.65 | 30.43 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 10.48 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 20.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 26.96 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `MySQL Scale & Migration` | 22.22 | 34.55 | 40.00 | 27.41 | 48.15 | 30.37 | 10.37 | 17.04 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 10.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 20.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 16.30 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Observability` | 20.00 | N/A | 5.00 | 15.00 | 0.00 | 25.00 | 55.00 | 40.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 15.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 20.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 45.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Scale & Architecture` | 10.23 | 12.63 | 35.35 | 28.84 | 42.79 | 39.07 | 19.53 | 18.60 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 18.46 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 20.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 24.65 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `TiDB Brand & Definitions` | 15.82 | N/A | 28.36 | 23.58 | 25.67 | 30.15 | 34.03 | 31.64 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 16.12 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 19.40 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 20.30 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### Citation Authority

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale | AlloyDB | Aurora | AuroraDSQL | Chroma | ClickHouse | Databricks | Druid | Elasticsearch | MariaDB | Milvus | MongoDB | MySQL | OceanBase | OpenSearch | Percona | Pinecone | Pinot | PostgreSQL | Qdrant | RDS | Redis | SingleStore | Snowflake | Spanner | StarRocks | TimescaleDB | Vespa | Vitess | Weaviate | pgvector |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `AI Agent Infrastructure` | 35.85 | 37.04 | 40.57 | 20.38 | 22.08 | 20.38 | 30.57 | 35.85 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 34.81 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Competitive Comparisons` | 0.00 | 0.00 | 0.00 | 2.17 | 0.00 | 0.00 | 0.00 | 2.25 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.96 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Deployment & Cloud` | 21.05 | N/A | 10.53 | 16.67 | 10.00 | 6.67 | 31.58 | 31.58 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 31.58 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Enterprise & Compliance` | 0.00 | 0.00 | 30.00 | 63.00 | 72.00 | 72.00 | 0.00 | 20.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 18.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Hybrid Search & RAG` | 26.80 | 42.42 | 22.68 | 17.63 | 13.92 | 19.48 | 21.34 | 19.59 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 15.77 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `MCP & Developer Tooling` | 26.09 | 25.00 | 43.48 | 31.30 | 39.13 | 35.22 | 19.57 | 39.13 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 31.30 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `MySQL Scale & Migration` | 29.63 | 36.36 | 51.85 | 30.00 | 50.00 | 43.33 | 13.33 | 14.81 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 20.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Observability` | 25.00 | N/A | 0.00 | 22.50 | 0.00 | 22.50 | 67.50 | 50.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 45.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Scale & Architecture` | 11.63 | 21.05 | 37.21 | 31.40 | 48.14 | 54.42 | 25.12 | 18.60 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 25.12 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `TiDB Brand & Definitions` | 25.37 | N/A | 26.87 | 25.52 | 29.55 | 38.96 | 37.61 | 35.82 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 25.52 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### Recommendation Rate

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale | AlloyDB | Aurora | AuroraDSQL | Chroma | ClickHouse | Databricks | Druid | Elasticsearch | MariaDB | Milvus | MongoDB | MySQL | OceanBase | OpenSearch | Percona | Pinecone | Pinot | PostgreSQL | Qdrant | RDS | Redis | SingleStore | Snowflake | Spanner | StarRocks | TimescaleDB | Vespa | Vitess | Weaviate | pgvector |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `AI Agent Infrastructure` | 33.33 | 36.84 | 48.72 | 25.64 | 28.21 | 25.64 | 41.03 | 33.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.56 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 41.03 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Competitive Comparisons` | 0.00 | 0.00 | 0.00 | 3.57 | 0.00 | 0.00 | 0.00 | 3.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 80.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 16.13 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.23 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Deployment & Cloud` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 80.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 14.29 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Enterprise & Compliance` | 0.00 | 0.00 | 0.00 | 100.00 | 50.00 | 50.00 | 0.00 | 50.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 50.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Hybrid Search & RAG` | 22.22 | 43.75 | 29.63 | 22.22 | 22.22 | 25.93 | 11.11 | 11.11 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 32.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 11.11 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `MCP & Developer Tooling` | 25.00 | 25.00 | 75.00 | 0.00 | 75.00 | 50.00 | 25.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 25.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `MySQL Scale & Migration` | 45.45 | 36.36 | 54.55 | 36.36 | 45.45 | 36.36 | 18.18 | 18.18 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 27.27 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Observability` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `Scale & Architecture` | 11.11 | 22.22 | 44.44 | 33.33 | 66.67 | 66.67 | 22.22 | 11.11 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 22.22 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `TiDB Brand & Definitions` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## Coverage

| Target | Non-branded prompts | Branded prompts | Target-answer rows |
| --- | ---: | ---: | ---: |
| CockroachDB | 217 | 2 | 219 |
| TiDB | 81 | 138 | 219 |
| YugabyteDB | 218 | 1 | 219 |
| Neon | 214 | 5 | 219 |
| Supabase | 216 | 3 | 219 |
| PlanetScale | 216 | 3 | 219 |
| AlloyDB | 219 | 0 | 219 |
| Aurora | 217 | 2 | 219 |
| AuroraDSQL | 219 | 0 | 219 |
| Chroma | 218 | 1 | 219 |
| ClickHouse | 219 | 0 | 219 |
| Databricks | 218 | 1 | 219 |
| Druid | 219 | 0 | 219 |
| Elasticsearch | 218 | 1 | 219 |
| MariaDB | 219 | 0 | 219 |
| Milvus | 216 | 3 | 219 |
| MongoDB | 216 | 3 | 219 |
| MySQL | 194 | 25 | 219 |
| OceanBase | 219 | 0 | 219 |
| OpenSearch | 218 | 1 | 219 |
| Percona | 219 | 0 | 219 |
| Pinecone | 217 | 2 | 219 |
| Pinot | 219 | 0 | 219 |
| PostgreSQL | 216 | 3 | 219 |
| Qdrant | 218 | 1 | 219 |
| RDS | 218 | 1 | 219 |
| Redis | 219 | 0 | 219 |
| SingleStore | 216 | 3 | 219 |
| Snowflake | 218 | 1 | 219 |
| Spanner | 218 | 1 | 219 |
| StarRocks | 219 | 0 | 219 |
| TimescaleDB | 219 | 0 | 219 |
| Vespa | 219 | 0 | 219 |
| Vitess | 218 | 1 | 219 |
| Weaviate | 217 | 2 | 219 |
| pgvector | 214 | 5 | 219 |

| Target | Visibility answers | Recommendation-eligible answers | Consideration-eligible answers |
| --- | ---: | ---: | ---: |
| CockroachDB | 217 | 130 | 0 |
| TiDB | 81 | 81 | 0 |
| YugabyteDB | 218 | 131 | 0 |
| Neon | 214 | 127 | 0 |
| Supabase | 216 | 129 | 0 |
| PlanetScale | 216 | 129 | 0 |
| AlloyDB | 219 | 132 | 0 |
| Aurora | 217 | 130 | 0 |
| AuroraDSQL | 219 | 132 | 0 |
| Chroma | 218 | 131 | 0 |
| ClickHouse | 219 | 132 | 0 |
| Databricks | 218 | 131 | 0 |
| Druid | 219 | 132 | 0 |
| Elasticsearch | 218 | 131 | 0 |
| MariaDB | 219 | 132 | 0 |
| Milvus | 216 | 129 | 0 |
| MongoDB | 216 | 129 | 0 |
| MySQL | 194 | 109 | 0 |
| OceanBase | 219 | 132 | 0 |
| OpenSearch | 218 | 131 | 0 |
| Percona | 219 | 132 | 0 |
| Pinecone | 217 | 130 | 0 |
| Pinot | 219 | 132 | 0 |
| PostgreSQL | 216 | 129 | 0 |
| Qdrant | 218 | 131 | 0 |
| RDS | 218 | 131 | 0 |
| Redis | 219 | 132 | 0 |
| SingleStore | 216 | 129 | 0 |
| Snowflake | 218 | 131 | 0 |
| Spanner | 218 | 131 | 0 |
| StarRocks | 219 | 132 | 0 |
| TimescaleDB | 219 | 132 | 0 |
| Vespa | 219 | 132 | 0 |
| Vitess | 218 | 131 | 0 |
| Weaviate | 217 | 130 | 0 |
| pgvector | 214 | 127 | 0 |

### Visibility coverage warnings

- Competitive Comparisons: 1 non-branded prompts for TiDB, below the configured minimum of 3.
- Deployment & Cloud: 0 non-branded prompts for TiDB, visibility KPIs are N/A by design.
- Enterprise & Compliance: 2 non-branded prompts for TiDB, below the configured minimum of 3.
- Observability: 0 non-branded prompts for TiDB, visibility KPIs are N/A by design.
- TiDB Brand & Definitions: 0 non-branded prompts for TiDB, visibility KPIs are N/A by design.
- MySQL Scale & Migration: 2 non-branded prompts for MySQL, below the configured minimum of 3.

## Quality Signals

- Average source authority shown below is target-specific in `target-kpi-summary.csv`.

## Competitive

### Aurora

- Comparison answers: 2
- Excluded pending prompt review: 1
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### Chroma

- Comparison answers: 1
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### CockroachDB

- Comparison answers: 2
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 2
- Target win rate: 50.00% (n = 2) — low sample
- Winner counts: {'CockroachDB': 1, 'TiDB': 1}

### Databricks

- Comparison answers: 1
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### Elasticsearch

- Comparison answers: 1
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 100.00% (n = 1) — low sample
- Winner counts: {'Elasticsearch': 1}

### Milvus

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 3
- Target win rate: 33.33% (n = 3) — low sample
- Winner counts: {'TiDB': 2, 'Milvus': 1}

### MongoDB

- Comparison answers: 2
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 2
- Target win rate: 0.00% (n = 2) — low sample
- Winner counts: {'TiDB': 2}

### MySQL

- Comparison answers: 10
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 10
- Target win rate: 20.00% (n = 10)
- Winner counts: {'Pinecone': 1, 'TiDB': 5, 'Vitess': 1, 'CockroachDB': 1, 'MySQL': 2}

### Neon

- Comparison answers: 5
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 5
- Target win rate: 60.00% (n = 5) — low sample
- Winner counts: {'Neon': 3, 'TiDB': 2}

### OpenSearch

- Comparison answers: 1
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### Pinecone

- Comparison answers: 2
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 2
- Target win rate: 50.00% (n = 2) — low sample
- Winner counts: {'Pinecone': 1, 'TiDB': 1}

### PlanetScale

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 3
- Target win rate: 0.00% (n = 3) — low sample
- Winner counts: {'TiDB': 3}

### PostgreSQL

- Comparison answers: 2
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 2
- Target win rate: 50.00% (n = 2) — low sample
- Winner counts: {'PostgreSQL': 1, 'TiDB': 1}

### Qdrant

- Comparison answers: 1
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### RDS

- Comparison answers: 1
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### SingleStore

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 3
- Target win rate: 66.67% (n = 3) — low sample
- Winner counts: {'SingleStore': 2, 'TiDB': 1}

### Snowflake

- Comparison answers: 1
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### Spanner

- Comparison answers: 1
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 100.00% (n = 1) — low sample
- Winner counts: {'Spanner': 1}

### Supabase

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 3
- Target win rate: 66.67% (n = 3) — low sample
- Winner counts: {'Supabase': 2, 'TiDB': 1}

### TiDB

- Comparison answers: 51
- Excluded pending prompt review: 1
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 50
- Target win rate: 64.00% (n = 50)
- Winner counts: {'TiDB': 32, 'Weaviate': 2, 'Elasticsearch': 1, 'PostgreSQL': 1, 'Pinecone': 1, 'Neon': 3, 'Vitess': 1, 'Spanner': 1, 'CockroachDB': 1, 'Supabase': 2, 'SingleStore': 2, 'Milvus': 1, 'MySQL': 2}

### Vitess

- Comparison answers: 1
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 100.00% (n = 1) — low sample
- Winner counts: {'Vitess': 1}

### Weaviate

- Comparison answers: 2
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 2
- Target win rate: 100.00% (n = 2) — low sample
- Winner counts: {'Weaviate': 2}

### YugabyteDB

- Comparison answers: 1
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### pgvector

- Comparison answers: 2
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 0
- Conditional / use-case split answers: 0
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 2
- Target win rate: 0.00% (n = 2) — low sample
- Winner counts: {'TiDB': 1, 'PostgreSQL': 1}

## Cost

- Saved-answer usage estimate: $0.0
- Scope: Usage estimate for successful saved answers in this report's search mode. Not a billing ledger; excludes failed or overwritten attempts and may include answers collected previously.
- Pricing version: 2026-09-03
- Fact judge mode: off
- Fact judge estimated cost: $0.0
- Combined provider and judge cost: $0.0
- Judge cost covers this scoring invocation. Cache hits add no new judge calls; previous judge charges are not included. The combined figure is not lifetime project spend.

- mock saved token cost: $0.0; saved web search cost: $0.0.

- Planned fresh-collection estimate: $0.0
- Planned scope: 219 prompts × 1 runs per provider.
- Selected prompts and providers, assuming fresh collection; excludes fact judging, retries and fallback. Not an incremental bill for rerunning cached answers.
- Assumptions: Input tokens are approximated from prompt text. Output tokens and searches per answer use previous saved usage when available, otherwise provider config; explicit output-token overrides take precedence.

- mock planned token cost: $0.0; planned web search cost: $0.0.
- mock assumptions: 700.0 output tokens per answer from models config; 0.0 searches per answer from models config.

## Run Metadata

- Prompt set hash (effective metadata): `6dde3e4577f292823c5955d18ab10577ce8464ac1a70405348c8edc195852d9d`
- Frozen source prompt hash: `f60c9f578eb58f2d783842ba0389387f3fdd5ddaa7c4d5354f2614715e6a6460`
- Prompt metadata revision: `2026-09-18-review-1`
- Legacy facts version: `2026-07-30`
- Semantic fact-base version: `None`
- Source-authority version: `2026-09-25-path-aware`
- Models config hash: `6da2e62eb56a50bdddda7d0d2aba354e57ab3156fc095fe1ab527bb4c4849a51`

## Semantic Coverage Audit

Decision coverage is not processing coverage. Comparison-only mappings can occur in any topic cluster. A legacy checked-fact count does not establish semantic eligibility.

| Outcome | Branded answers | Explanation |
| --- | ---: | --- |
| disabled | 138 | Semantic judging was disabled for this answer. |

Reconciled total: 138/138 branded answers. See `semantic-coverage-audit.csv` for exact prompt/provider IDs and pending fact IDs. Scored answers may still have pending review items. Existing accuracy and coverage denominators are unchanged.

## Cited Domain Analysis

Domains are ranked by the number of unique prompts for which they were cited. Open the [filterable cited-domain report](cited-domains.html) for answer-level evidence.

| Domain | Type | Prompts | Cited answers | TiDB appeared | Recommended products |
| --- | --- | ---: | ---: | ---: | --- |
| docs.pingcap.com | PingCAP | 108 | 108 | 108 | TiDB (51), Spanner (17), AlloyDB (15), Neon (3), SingleStore (2), Supabase (2), Weaviate (2), CockroachDB (1), Elasticsearch (1), Milvus (1), MySQL (1), Pinecone (1), PostgreSQL (1), Vitess (1) |
| cloud.google.com | Competitor | 78 | 78 | 60 | Aurora (22), Spanner (17), Neon (16), AlloyDB (15) |
| planetscale.com | Competitor | 63 | 63 | 3 | YugabyteDB (23), Supabase (15), PlanetScale (12), TiDB (2) |
| docs.yugabyte.com | Competitor | 61 | 61 | 22 | YugabyteDB (23), TiDB (21), CockroachDB (9) |
| supabase.com | Competitor | 59 | 59 | 3 | YugabyteDB (23), Supabase (17), CockroachDB (9), TiDB (1) |
| docs.aws.amazon.com | Competitor | 57 | 57 | 25 | Aurora (22), Neon (16), PlanetScale (12), TiDB (2) |
| neon.tech | Competitor | 54 | 54 | 5 | Neon (19), Supabase (15), PlanetScale (12), TiDB (2) |
| cockroachlabs.com | Competitor | 52 | 52 | 42 | TiDB (21), AlloyDB (15), CockroachDB (10) |

Recommendations are observed in answers that cite the domain; this is an association, not proof of causation.
