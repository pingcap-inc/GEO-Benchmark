# GEO Benchmark LLM Report - 2026-11

Providers: mock
Web search mode: off
Saved raw records: 230
Successfully scored answers: 230
Failed raw records: 0
Incomplete raw records: 0
Scored target-answer rows: 8280

> Warning: this report includes mock provider output. Use it only as a pipeline smoke test, not as a market benchmark.

## Executive KPI

| Target | Consideration Rate | Mention Rate | Prominence Score | Citation Authority | Recommendation Rate | Comparison Win Rate | Stable Consideration Rate | Stable Mention Rate | Stable Prominence Score | Stable Recommendation Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | N/A | 32.02 | 17.63 | 23.20 | 22.70 | 50.00% (n = 2) — low sample | N/A | 32.02 | 17.63 | 22.70 |
| TiDB | N/A | 41.30 | 27.63 | 32.99 | 32.61 | 64.00% (n = 50) | N/A | 41.30 | 27.63 | 32.61 |
| YugabyteDB | N/A | 37.12 | 21.50 | 25.58 | 31.69 | 0.00% (n = 1) — low sample | N/A | 37.12 | 21.50 | 31.69 |
| Neon | N/A | 36.44 | 19.20 | 20.57 | 21.74 | 60.00% (n = 5) — low sample | N/A | 36.44 | 19.20 | 21.74 |
| Supabase | N/A | 37.00 | 19.75 | 22.30 | 27.14 | 66.67% (n = 3) — low sample | N/A | 37.00 | 19.75 | 27.14 |
| PlanetScale | N/A | 33.92 | 19.42 | 23.27 | 24.29 | 0.00% (n = 3) — low sample | N/A | 33.92 | 19.42 | 24.29 |
| AlloyDB | N/A | 34.78 | 20.14 | 22.74 | 18.18 | N/A | N/A | 34.78 | 20.14 | 18.18 |
| Aurora | N/A | 33.77 | 20.29 | 24.64 | 17.73 | 0.00% (n = 1) — low sample | N/A | 33.77 | 20.29 | 17.73 |
| AuroraDSQL | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| Chroma | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| ClickHouse | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| Databricks | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| Druid | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| Elasticsearch | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 100.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| MariaDB | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| Milvus | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 33.33% (n = 3) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| MongoDB | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 2) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| MySQL | N/A | 74.15 | 23.39 | 0.00 | 28.33 | 20.00% (n = 10) | N/A | 74.15 | 23.39 | 28.33 |
| OceanBase | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| OpenSearch | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| Percona | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| Pinecone | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 50.00% (n = 2) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| Pinot | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| PostgreSQL | N/A | 83.26 | 17.22 | 0.00 | 4.29 | 50.00% (n = 2) — low sample | N/A | 83.26 | 17.22 | 4.29 |
| Qdrant | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| RDS | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| Redis | N/A | 0.00 | 0.00 | 0.00 | 0.00 | N/A | N/A | 0.00 | 0.00 | 0.00 |
| SingleStore | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 66.67% (n = 3) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| Snowflake | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00% (n = 1) — low sample | N/A | 0.00 | 0.00 | 0.00 |
| Spanner | N/A | 32.75 | 18.96 | 22.22 | 21.13 | 100.00% (n = 1) — low sample | N/A | 32.75 | 18.96 | 21.13 |
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
| `AI Agent Infrastructure` | 47.46 | 46.94 | 50.85 | 35.59 | 47.46 | 37.29 | 44.07 | 38.98 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 59.32 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 98.31 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 42.37 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
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
| `AI Agent Infrastructure` | 30.53 | 29.06 | 30.84 | 22.44 | 23.05 | 19.08 | 25.04 | 27.48 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 12.82 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 19.54 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 25.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
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
| `AI Agent Infrastructure` | 39.69 | 33.96 | 41.22 | 22.67 | 26.11 | 20.61 | 28.17 | 34.35 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 31.60 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
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
| `AI Agent Infrastructure` | 38.00 | 32.65 | 48.00 | 28.00 | 34.00 | 28.00 | 36.00 | 34.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 38.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
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
| CockroachDB | 228 | 2 | 230 |
| TiDB | 92 | 138 | 230 |
| YugabyteDB | 229 | 1 | 230 |
| Neon | 225 | 5 | 230 |
| Supabase | 227 | 3 | 230 |
| PlanetScale | 227 | 3 | 230 |
| AlloyDB | 230 | 0 | 230 |
| Aurora | 228 | 2 | 230 |
| AuroraDSQL | 230 | 0 | 230 |
| Chroma | 229 | 1 | 230 |
| ClickHouse | 230 | 0 | 230 |
| Databricks | 229 | 1 | 230 |
| Druid | 230 | 0 | 230 |
| Elasticsearch | 229 | 1 | 230 |
| MariaDB | 230 | 0 | 230 |
| Milvus | 227 | 3 | 230 |
| MongoDB | 227 | 3 | 230 |
| MySQL | 205 | 25 | 230 |
| OceanBase | 230 | 0 | 230 |
| OpenSearch | 229 | 1 | 230 |
| Percona | 230 | 0 | 230 |
| Pinecone | 228 | 2 | 230 |
| Pinot | 230 | 0 | 230 |
| PostgreSQL | 227 | 3 | 230 |
| Qdrant | 229 | 1 | 230 |
| RDS | 229 | 1 | 230 |
| Redis | 230 | 0 | 230 |
| SingleStore | 227 | 3 | 230 |
| Snowflake | 229 | 1 | 230 |
| Spanner | 229 | 1 | 230 |
| StarRocks | 230 | 0 | 230 |
| TimescaleDB | 230 | 0 | 230 |
| Vespa | 230 | 0 | 230 |
| Vitess | 229 | 1 | 230 |
| Weaviate | 228 | 2 | 230 |
| pgvector | 225 | 5 | 230 |

| Target | Visibility answers | Recommendation-eligible answers | Consideration-eligible answers |
| --- | ---: | ---: | ---: |
| CockroachDB | 228 | 141 | 0 |
| TiDB | 92 | 92 | 0 |
| YugabyteDB | 229 | 142 | 0 |
| Neon | 225 | 138 | 0 |
| Supabase | 227 | 140 | 0 |
| PlanetScale | 227 | 140 | 0 |
| AlloyDB | 230 | 143 | 0 |
| Aurora | 228 | 141 | 0 |
| AuroraDSQL | 230 | 143 | 0 |
| Chroma | 229 | 142 | 0 |
| ClickHouse | 230 | 143 | 0 |
| Databricks | 229 | 142 | 0 |
| Druid | 230 | 143 | 0 |
| Elasticsearch | 229 | 142 | 0 |
| MariaDB | 230 | 143 | 0 |
| Milvus | 227 | 140 | 0 |
| MongoDB | 227 | 140 | 0 |
| MySQL | 205 | 120 | 0 |
| OceanBase | 230 | 143 | 0 |
| OpenSearch | 229 | 142 | 0 |
| Percona | 230 | 143 | 0 |
| Pinecone | 228 | 141 | 0 |
| Pinot | 230 | 143 | 0 |
| PostgreSQL | 227 | 140 | 0 |
| Qdrant | 229 | 142 | 0 |
| RDS | 229 | 142 | 0 |
| Redis | 230 | 143 | 0 |
| SingleStore | 227 | 140 | 0 |
| Snowflake | 229 | 142 | 0 |
| Spanner | 229 | 142 | 0 |
| StarRocks | 230 | 143 | 0 |
| TimescaleDB | 230 | 143 | 0 |
| Vespa | 230 | 143 | 0 |
| Vitess | 229 | 142 | 0 |
| Weaviate | 228 | 141 | 0 |
| pgvector | 225 | 138 | 0 |

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
- Planned scope: 230 prompts × 1 runs per provider.
- Selected prompts and providers, assuming fresh collection; excludes fact judging, retries and fallback. Not an incremental bill for rerunning cached answers.
- Assumptions: Input tokens are approximated from prompt text. Output tokens and searches per answer use previous saved usage when available, otherwise provider config; explicit output-token overrides take precedence.

- mock planned token cost: $0.0; planned web search cost: $0.0.
- mock assumptions: 137.758 output tokens per answer from previous cost_summary.json; 0.0 searches per answer from previous cost_summary.json.

## Run Metadata

- Prompt set hash (effective metadata): `9d571b44ea7db287bb6405b3213401a32904b62cfa375a9551554017eab85e00`
- Frozen source prompt hash: `9d571b44ea7db287bb6405b3213401a32904b62cfa375a9551554017eab85e00`
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
| docs.pingcap.com | PingCAP | 110 | 110 | 110 | TiDB (52), Spanner (17), AlloyDB (16), Neon (3), SingleStore (2), Supabase (2), Weaviate (2), CockroachDB (1), Elasticsearch (1), Milvus (1), MySQL (1), Pinecone (1), PostgreSQL (1), Vitess (1) |
| cloud.google.com | Competitor | 81 | 81 | 62 | Aurora (23), Neon (17), Spanner (17), AlloyDB (16) |
| docs.yugabyte.com | Competitor | 66 | 66 | 23 | YugabyteDB (23), TiDB (22), CockroachDB (12) |
| planetscale.com | Competitor | 66 | 66 | 3 | YugabyteDB (23), Supabase (16), PlanetScale (12), TiDB (2) |
| supabase.com | Competitor | 65 | 65 | 3 | YugabyteDB (23), Supabase (18), CockroachDB (12), TiDB (1) |
| docs.aws.amazon.com | Competitor | 60 | 60 | 26 | Aurora (23), Neon (17), PlanetScale (12), TiDB (2) |
| cockroachlabs.com | Competitor | 58 | 58 | 44 | TiDB (22), AlloyDB (16), CockroachDB (13) |
| neon.tech | Competitor | 58 | 58 | 5 | Neon (20), Supabase (16), PlanetScale (12), TiDB (2) |

Recommendations are observed in answers that cite the domain; this is an association, not proof of causation.
