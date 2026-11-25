# GEO Benchmark LLM Report - 2026-10

Providers: anthropic, gemini, openai
Web search mode: on
Saved raw records: 657
Successfully scored answers: 657
Failed raw records: 0
Incomplete raw records: 0
Scored target-answer rows: 23652

## Executive KPI

| Target | Consideration Rate | Mention Rate | Prominence Score | Citation Authority | Recommendation Rate | Comparison Win Rate | Stable Consideration Rate | Stable Mention Rate | Stable Prominence Score | Stable Recommendation Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 5.46 | 12.14 | 5.29 | 2.55 | 9.74 | 0.00% (n = 2) — low sample | 5.46 | 12.14 | 5.29 | 9.74 |
| TiDB | 11.44 | 33.74 | 15.11 | 14.94 | 20.58 | 62.50% (n = 48) | 11.44 | 33.74 | 15.11 | 20.58 |
| YugabyteDB | 2.31 | 4.28 | 1.77 | 1.58 | 1.78 | N/A | 2.31 | 4.28 | 1.77 | 1.78 |
| Neon | 2.11 | 6.39 | 3.41 | 0.64 | 6.82 | 100.00% (n = 1) — low sample | 2.11 | 6.39 | 3.41 | 6.82 |
| Supabase | 0.44 | 4.94 | 1.79 | 0.52 | 3.10 | N/A | 0.44 | 4.94 | 1.79 | 3.10 |
| PlanetScale | 3.79 | 5.71 | 2.06 | 1.32 | 5.43 | 0.00% (n = 2) — low sample | 3.79 | 5.71 | 2.06 | 5.43 |
| AlloyDB | 0.00 | 1.52 | 0.46 | 0.11 | 0.76 | N/A | 0.00 | 1.52 | 0.46 | 0.76 |
| Aurora | 2.64 | 7.07 | 2.15 | 0.52 | 3.85 | 100.00% (n = 1) — low sample | 2.64 | 7.07 | 2.15 | 3.85 |
| AuroraDSQL | 0.00 | 0.15 | 0.04 | 0.10 | 0.00 | N/A | 0.00 | 0.15 | 0.04 | 0.00 |
| Chroma | 1.12 | 1.53 | 0.37 | 0.06 | 0.51 | N/A | 1.12 | 1.53 | 0.37 | 0.51 |
| ClickHouse | 0.62 | 1.83 | 0.74 | 0.96 | 1.52 | N/A | 0.62 | 1.83 | 0.74 | 1.52 |
| Databricks | 0.25 | 2.75 | 1.06 | 2.51 | 1.02 | N/A | 0.25 | 2.75 | 1.06 | 1.02 |
| Druid | 0.12 | 0.46 | 0.12 | 0.00 | 0.25 | N/A | 0.12 | 0.46 | 0.12 | 0.25 |
| Elasticsearch | 1.87 | 4.13 | 1.76 | 0.83 | 2.80 | 50.00% (n = 2) — low sample | 1.87 | 4.13 | 1.76 | 2.80 |
| MariaDB | 0.87 | 2.44 | 0.70 | 0.32 | 0.00 | N/A | 0.87 | 2.44 | 0.70 | 0.00 |
| Milvus | 7.95 | 14.81 | 4.84 | 4.47 | 7.75 | 83.33% (n = 6) — low sample | 7.95 | 14.81 | 4.84 | 7.75 |
| MongoDB | 0.38 | 5.56 | 2.48 | 0.76 | 6.20 | 33.33% (n = 3) — low sample | 0.38 | 5.56 | 2.48 | 6.20 |
| MySQL | 5.18 | 36.94 | 19.55 | 0.33 | 13.46 | 0.00% (n = 7) — low sample | 5.18 | 36.94 | 19.55 | 13.46 |
| OceanBase | 0.00 | 0.15 | 0.02 | 0.00 | 0.00 | N/A | 0.00 | 0.15 | 0.02 | 0.00 |
| OpenSearch | 0.37 | 2.91 | 1.15 | 0.00 | 1.78 | 100.00% (n = 1) — low sample | 0.37 | 2.91 | 1.15 | 1.78 |
| Percona | 0.50 | 0.91 | 0.24 | 0.49 | 0.76 | N/A | 0.50 | 0.91 | 0.24 | 0.76 |
| Pinecone | 6.97 | 18.59 | 7.22 | 1.68 | 9.49 | 33.33% (n = 3) — low sample | 6.97 | 18.59 | 7.22 | 9.49 |
| Pinot | 0.12 | 0.15 | 0.02 | 0.00 | 0.25 | N/A | 0.12 | 0.15 | 0.02 | 0.25 |
| PostgreSQL | 12.22 | 46.45 | 25.55 | 0.62 | 42.38 | 100.00% (n = 1) — low sample | 12.22 | 46.45 | 25.55 | 42.38 |
| Qdrant | 5.93 | 16.21 | 6.28 | 2.78 | 12.21 | 0.00% (n = 1) — low sample | 5.93 | 16.21 | 6.28 | 12.21 |
| RDS | 0.75 | 4.74 | 1.52 | 0.06 | 2.80 | 0.00% (n = 1) — low sample | 0.75 | 4.74 | 1.52 | 2.80 |
| Redis | 5.21 | 11.42 | 4.99 | 4.58 | 9.34 | N/A | 5.21 | 11.42 | 4.99 | 9.34 |
| SingleStore | 2.27 | 4.78 | 1.75 | 1.43 | 4.13 | 50.00% (n = 4) — low sample | 2.27 | 4.78 | 1.75 | 4.13 |
| Snowflake | 0.81 | 2.60 | 1.19 | 0.15 | 2.04 | 0.00% (n = 2) — low sample | 0.81 | 2.60 | 1.19 | 2.04 |
| Spanner | 1.19 | 3.06 | 1.04 | 0.71 | 1.27 | 50.00% (n = 2) — low sample | 1.19 | 3.06 | 1.04 | 1.27 |
| StarRocks | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 |
| TimescaleDB | 0.00 | 1.37 | 0.45 | 0.00 | 1.26 | N/A | 0.00 | 1.37 | 0.45 | 1.26 |
| Vespa | 1.24 | 1.22 | 0.50 | 0.44 | 1.26 | N/A | 1.24 | 1.22 | 0.50 | 1.26 |
| Vitess | 3.93 | 9.17 | 3.52 | 1.20 | 7.38 | 0.00% (n = 1) — low sample | 3.93 | 9.17 | 3.52 | 7.38 |
| Weaviate | 6.03 | 13.21 | 4.27 | 1.70 | 8.97 | 100.00% (n = 3) — low sample | 6.03 | 13.21 | 4.27 | 8.97 |
| pgvector | 8.57 | 28.04 | 11.19 | 0.36 | 25.20 | 0.00% (n = 1) — low sample | 8.57 | 28.04 | 11.19 | 25.20 |

## Branded Accuracy

| Target | Prompts | Legacy accuracy | Legacy coverage | Semantic accuracy | Semantic decision coverage | Judge unavailable |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 2 | 83.34 | 100.00% | N/A | 0.00% | 0 |
| TiDB | 138 | 52.36 | 100.00% | N/A | 0.00% | 0 |
| YugabyteDB | 1 | 100.00 | 100.00% | N/A | 0.00% | 0 |
| Neon | 5 | 26.67 | 100.00% | N/A | 0.00% | 0 |
| Supabase | 3 | 83.33 | 100.00% | N/A | 0.00% | 0 |
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
| `AI Agent Infrastructure` | 6.29 | 1.65 | 2.20 | 7.86 | 1.57 | 4.40 | 0.00 | 2.20 | 0.00 | 3.14 | 2.52 | 0.00 | 0.63 | 1.26 | 0.00 | 15.09 | 0.00 | 0.63 | 0.00 | 0.00 | 0.00 | 17.92 | 0.63 | 25.16 | 14.47 | 0.63 | 18.24 | 3.14 | 1.26 | 1.89 | 0.00 | 0.00 | 1.89 | 1.26 | 13.84 | 20.75 |
| `Competitive Comparisons` | 1.87 | 0.00 | 1.81 | 0.00 | 0.00 | 1.12 | 0.00 | 2.25 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.87 | 0.00 | 9.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 13.04 | 0.70 | 1.09 | 0.70 | 0.00 | 0.00 | 1.09 | 0.00 | 0.00 | 0.00 | 4.35 | 0.00 | 3.16 |
| `Deployment & Cloud` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 1.85 | 0.00 | 1.75 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.92 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.51 | 0.00 | 1.75 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.75 |
| `Enterprise & Compliance` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 6.67 | 0.00 | 13.33 | 0.00 | 0.00 | 0.00 | 13.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 13.33 | 0.00 | 6.67 | 0.00 | 0.00 | 6.67 | 0.00 | 13.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 13.33 | 6.67 |
| `Hybrid Search & RAG` | 2.75 | 0.00 | 1.37 | 0.00 | 0.69 | 0.00 | 0.00 | 0.69 | 0.00 | 2.06 | 0.00 | 0.00 | 0.00 | 6.74 | 0.00 | 18.44 | 2.17 | 0.00 | 0.00 | 2.13 | 0.00 | 13.12 | 0.00 | 13.77 | 12.06 | 0.69 | 5.50 | 2.06 | 0.00 | 0.00 | 0.00 | 0.00 | 4.81 | 0.00 | 14.54 | 16.08 |
| `MCP & Developer Tooling` | 2.90 | 16.67 | 0.00 | 0.00 | 0.00 | 5.80 | 0.00 | 2.90 | 0.00 | 0.00 | 2.90 | 0.00 | 0.00 | 0.00 | 0.00 | 2.90 | 0.00 | 9.52 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 11.59 | 5.80 | 0.00 | 2.90 | 5.80 | 2.90 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 8.70 |
| `MySQL Scale & Migration` | 24.69 | 60.61 | 9.88 | 0.00 | 0.00 | 24.69 | 0.00 | 14.81 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 12.35 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | 9.88 | 0.00 | 0.00 | 4.94 | 0.00 | 2.47 | 0.00 | 17.28 | 0.00 | 7.41 | 0.00 | 0.00 | 0.00 | 34.57 | 0.00 | 0.00 |
| `Observability` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Scale & Architecture` | 23.26 | 17.54 | 8.53 | 4.65 | 0.00 | 10.85 | 0.00 | 4.65 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.88 | 3.10 | 8.53 | 0.00 | 3.42 | 0.00 | 0.00 | 0.00 | 6.98 | 0.00 | 9.30 | 5.43 | 0.00 | 3.10 | 1.55 | 0.00 | 3.10 | 0.00 | 0.00 | 0.00 | 11.63 | 3.88 | 3.10 |
| `TiDB Brand & Definitions` | 1.00 | N/A | 1.00 | 1.00 | 0.00 | 1.00 | 0.00 | 1.99 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.99 | 0.00 | 11.44 | 0.00 | 0.00 | 0.00 | 1.99 | 0.00 | 3.98 | 1.00 | 0.00 | 0.00 | 0.00 | 1.49 | 0.00 | 0.00 | 0.00 | 0.00 | 1.99 | 1.00 | 1.99 |

### Mention Rate

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale | AlloyDB | Aurora | AuroraDSQL | Chroma | ClickHouse | Databricks | Druid | Elasticsearch | MariaDB | Milvus | MongoDB | MySQL | OceanBase | OpenSearch | Percona | Pinecone | Pinot | PostgreSQL | Qdrant | RDS | Redis | SingleStore | Snowflake | Spanner | StarRocks | TimescaleDB | Vespa | Vitess | Weaviate | pgvector |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `AI Agent Infrastructure` | 13.19 | 21.93 | 2.78 | 20.14 | 9.72 | 4.86 | 2.78 | 4.17 | 0.00 | 6.25 | 5.56 | 4.86 | 0.69 | 1.39 | 0.00 | 20.14 | 11.11 | 15.28 | 0.00 | 0.00 | 0.00 | 40.97 | 0.00 | 74.31 | 38.89 | 4.17 | 38.19 | 4.86 | 1.39 | 3.47 | 0.00 | 4.86 | 0.69 | 2.08 | 26.39 | 55.56 |
| `Competitive Comparisons` | 7.78 | 33.33 | 3.23 | 1.19 | 0.00 | 3.33 | 1.04 | 10.00 | 1.04 | 0.00 | 0.00 | 1.08 | 0.00 | 0.00 | 0.00 | 10.00 | 1.08 | 65.33 | 0.00 | 0.00 | 1.04 | 5.38 | 0.00 | 48.39 | 4.17 | 9.68 | 1.04 | 1.11 | 3.23 | 5.38 | 0.00 | 2.08 | 0.00 | 10.75 | 0.00 | 12.50 |
| `Deployment & Cloud` | 0.00 | N/A | 0.00 | 0.00 | 3.51 | 1.75 | 0.00 | 1.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.67 | 62.96 | 0.00 | 0.00 | 0.00 | 1.67 | 0.00 | 20.00 | 0.00 | 1.67 | 1.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.33 | 0.00 | 8.33 |
| `Enterprise & Compliance` | 8.33 | 16.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 25.00 | 0.00 | 0.00 | 0.00 | 0.00 | 16.67 | 0.00 | 0.00 | 0.00 | 0.00 | 25.00 | 0.00 | 25.00 | 0.00 | 8.33 | 8.33 | 8.33 | 25.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 8.33 | 25.00 |
| `Hybrid Search & RAG` | 4.27 | 12.50 | 2.56 | 1.71 | 5.13 | 0.00 | 2.56 | 2.56 | 0.00 | 0.00 | 0.00 | 1.71 | 0.00 | 21.05 | 0.00 | 35.96 | 10.81 | 16.22 | 0.00 | 14.91 | 0.00 | 29.82 | 0.00 | 56.76 | 35.09 | 3.42 | 8.55 | 5.13 | 0.85 | 0.00 | 0.00 | 0.00 | 5.13 | 0.00 | 36.84 | 60.78 |
| `MCP & Developer Tooling` | 3.33 | 41.67 | 0.00 | 6.67 | 13.33 | 10.00 | 6.67 | 10.00 | 0.00 | 3.33 | 3.33 | 10.00 | 3.33 | 0.00 | 0.00 | 13.33 | 10.00 | 33.33 | 0.00 | 0.00 | 0.00 | 6.67 | 0.00 | 36.67 | 3.33 | 13.33 | 6.67 | 6.67 | 6.67 | 0.00 | 0.00 | 0.00 | 0.00 | 6.67 | 3.33 | 23.33 |
| `MySQL Scale & Migration` | 30.77 | 100.00 | 12.82 | 0.00 | 0.00 | 35.90 | 0.00 | 20.51 | 0.00 | 0.00 | 2.56 | 0.00 | 2.56 | 0.00 | 23.08 | 2.56 | 2.56 | 100.00 | 2.56 | 0.00 | 10.26 | 0.00 | 2.56 | 35.90 | 0.00 | 10.26 | 0.00 | 23.08 | 0.00 | 10.26 | 0.00 | 0.00 | 0.00 | 69.23 | 0.00 | 0.00 |
| `Observability` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 8.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Scale & Architecture` | 42.59 | 40.74 | 12.96 | 12.96 | 9.26 | 14.81 | 0.00 | 5.56 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.85 | 1.85 | 7.41 | 0.00 | 41.67 | 0.00 | 3.70 | 0.00 | 11.11 | 0.00 | 46.30 | 7.41 | 0.00 | 5.56 | 3.70 | 0.00 | 5.56 | 0.00 | 0.00 | 1.85 | 25.93 | 0.00 | 5.56 |
| `TiDB Brand & Definitions` | 11.83 | N/A | 6.45 | 0.00 | 1.08 | 1.08 | 0.00 | 13.98 | 0.00 | 0.00 | 2.15 | 2.15 | 0.00 | 0.00 | 6.45 | 8.60 | 0.00 | 60.22 | 0.00 | 0.00 | 1.08 | 11.83 | 0.00 | 22.58 | 1.08 | 2.15 | 2.15 | 3.33 | 6.45 | 3.23 | 0.00 | 0.00 | 0.00 | 2.15 | 4.30 | 8.60 |

### Prominence Score

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale | AlloyDB | Aurora | AuroraDSQL | Chroma | ClickHouse | Databricks | Druid | Elasticsearch | MariaDB | Milvus | MongoDB | MySQL | OceanBase | OpenSearch | Percona | Pinecone | Pinot | PostgreSQL | Qdrant | RDS | Redis | SingleStore | Snowflake | Spanner | StarRocks | TimescaleDB | Vespa | Vitess | Weaviate | pgvector |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `AI Agent Infrastructure` | 7.30 | 8.56 | 1.82 | 12.45 | 4.21 | 1.64 | 1.01 | 1.95 | 0.00 | 1.76 | 2.77 | 2.58 | 0.38 | 0.25 | 0.00 | 7.23 | 5.16 | 6.23 | 0.00 | 0.00 | 0.00 | 19.75 | 0.00 | 51.07 | 17.61 | 1.57 | 19.69 | 2.39 | 1.01 | 0.88 | 0.00 | 1.95 | 0.13 | 0.38 | 8.36 | 26.67 |
| `Competitive Comparisons` | 3.00 | 20.00 | 2.03 | 0.24 | 0.00 | 1.12 | 0.21 | 3.37 | 0.21 | 0.00 | 0.00 | 0.22 | 0.00 | 0.00 | 0.00 | 2.70 | 0.43 | 29.60 | 0.00 | 0.00 | 0.63 | 1.52 | 0.00 | 19.86 | 1.26 | 2.75 | 0.14 | 0.45 | 0.65 | 1.96 | 0.00 | 0.35 | 0.00 | 3.48 | 0.00 | 4.14 |
| `Deployment & Cloud` | 0.00 | N/A | 0.00 | 0.00 | 1.85 | 0.37 | 0.00 | 1.05 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.05 | 32.55 | 0.00 | 0.00 | 0.00 | 0.35 | 0.00 | 8.65 | 0.00 | 1.05 | 0.23 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.70 | 0.00 | 2.34 |
| `Enterprise & Compliance` | 6.67 | 10.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 9.33 | 0.00 | 0.00 | 0.00 | 0.00 | 8.00 | 0.00 | 0.00 | 0.00 | 0.00 | 9.33 | 0.00 | 14.67 | 0.00 | 4.00 | 1.33 | 4.00 | 17.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.33 | 9.33 |
| `Hybrid Search & RAG` | 1.24 | 4.04 | 1.24 | 0.27 | 1.37 | 0.00 | 0.69 | 0.69 | 0.00 | 0.00 | 0.00 | 0.27 | 0.00 | 9.08 | 0.00 | 11.42 | 5.51 | 8.50 | 0.00 | 5.74 | 0.00 | 9.36 | 0.00 | 32.61 | 11.91 | 1.37 | 2.47 | 1.51 | 0.14 | 0.00 | 0.00 | 0.00 | 2.47 | 0.00 | 13.76 | 23.61 |
| `MCP & Developer Tooling` | 0.58 | 11.67 | 0.00 | 3.48 | 4.64 | 5.22 | 2.32 | 1.74 | 0.00 | 0.58 | 0.58 | 5.22 | 0.58 | 0.00 | 0.00 | 6.38 | 2.90 | 18.10 | 0.00 | 0.00 | 0.00 | 5.22 | 0.00 | 27.54 | 1.74 | 2.32 | 2.61 | 1.16 | 4.64 | 0.00 | 0.00 | 0.00 | 0.00 | 3.48 | 0.87 | 9.57 |
| `MySQL Scale & Migration` | 9.88 | 51.52 | 3.46 | 0.00 | 0.00 | 13.83 | 0.00 | 3.95 | 0.00 | 0.00 | 0.49 | 0.00 | 0.49 | 0.00 | 4.44 | 0.49 | 0.49 | 100.00 | 0.49 | 0.00 | 1.98 | 0.00 | 0.49 | 8.89 | 0.00 | 2.96 | 0.00 | 10.37 | 0.00 | 1.98 | 0.00 | 0.00 | 0.00 | 35.80 | 0.00 | 0.00 |
| `Observability` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 5.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Scale & Architecture` | 22.02 | 22.11 | 4.34 | 7.75 | 2.79 | 6.67 | 0.00 | 1.55 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.40 | 0.31 | 2.33 | 0.00 | 19.15 | 0.00 | 1.71 | 0.00 | 6.05 | 0.00 | 26.05 | 3.88 | 0.00 | 4.65 | 0.62 | 0.00 | 2.95 | 0.00 | 0.00 | 0.31 | 9.46 | 0.00 | 1.55 |
| `TiDB Brand & Definitions` | 5.27 | N/A | 2.49 | 0.00 | 0.60 | 0.20 | 0.00 | 4.38 | 0.00 | 0.00 | 1.19 | 0.50 | 0.00 | 0.00 | 3.58 | 3.18 | 0.00 | 35.92 | 0.00 | 0.00 | 0.20 | 3.38 | 0.00 | 9.55 | 0.60 | 0.40 | 0.80 | 1.74 | 2.59 | 1.49 | 0.00 | 0.00 | 0.00 | 0.40 | 0.80 | 1.99 |

### Citation Authority

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale | AlloyDB | Aurora | AuroraDSQL | Chroma | ClickHouse | Databricks | Druid | Elasticsearch | MariaDB | Milvus | MongoDB | MySQL | OceanBase | OpenSearch | Percona | Pinecone | Pinot | PostgreSQL | Qdrant | RDS | Redis | SingleStore | Snowflake | Spanner | StarRocks | TimescaleDB | Vespa | Vitess | Weaviate | pgvector |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `AI Agent Infrastructure` | 6.05 | 11.06 | 2.21 | 2.46 | 1.19 | 1.13 | 0.00 | 0.52 | 0.00 | 0.28 | 2.75 | 4.67 | 0.00 | 0.57 | 0.00 | 3.91 | 1.36 | 0.28 | 0.00 | 0.00 | 0.00 | 3.87 | 0.00 | 1.89 | 7.10 | 0.31 | 16.24 | 1.58 | 0.00 | 0.91 | 0.00 | 0.00 | 0.45 | 0.00 | 3.25 | 0.91 |
| `Competitive Comparisons` | 0.54 | 30.00 | 2.42 | 0.00 | 0.00 | 0.81 | 0.00 | 0.90 | 0.00 | 0.00 | 0.76 | 0.82 | 0.00 | 0.00 | 0.00 | 6.10 | 0.00 | 0.00 | 0.00 | 0.00 | 1.42 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.78 | 0.00 | 0.00 |
| `Deployment & Cloud` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.79 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Enterprise & Compliance` | 2.00 | 5.62 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 7.80 | 0.00 | 3.00 | 0.00 | 0.00 | 3.00 | 0.00 | 0.00 | 0.00 | 0.00 | 7.80 | 0.00 | 0.00 | 0.00 | 0.00 | 3.00 | 3.00 | 7.80 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Hybrid Search & RAG` | 1.01 | 7.14 | 1.04 | 0.00 | 1.30 | 0.31 | 0.00 | 0.00 | 0.00 | 0.00 | 0.77 | 3.28 | 0.00 | 3.26 | 0.00 | 10.88 | 2.16 | 0.00 | 0.00 | 0.00 | 0.00 | 2.50 | 0.00 | 0.52 | 4.98 | 0.00 | 4.50 | 1.92 | 0.00 | 0.00 | 0.00 | 0.00 | 1.92 | 0.00 | 5.43 | 1.09 |
| `MCP & Developer Tooling` | 1.39 | 13.50 | 0.00 | 0.00 | 0.00 | 3.39 | 2.61 | 1.45 | 0.00 | 0.00 | 2.09 | 2.61 | 0.00 | 0.00 | 1.30 | 0.00 | 1.30 | 2.29 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.09 | 0.00 | 6.75 | 2.09 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `MySQL Scale & Migration` | 9.32 | 41.70 | 7.70 | 0.00 | 0.00 | 8.44 | 0.00 | 3.95 | 1.98 | 0.00 | 0.00 | 2.22 | 0.00 | 0.00 | 3.56 | 2.22 | 0.00 | 19.50 | 0.00 | 0.00 | 4.67 | 0.00 | 0.00 | 1.11 | 0.00 | 0.00 | 0.00 | 8.67 | 0.00 | 5.33 | 0.00 | 0.00 | 0.00 | 14.67 | 0.00 | 0.00 |
| `Observability` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Scale & Architecture` | 5.07 | 15.06 | 1.74 | 1.77 | 0.56 | 3.91 | 0.00 | 0.00 | 0.00 | 0.00 | 0.70 | 3.49 | 0.00 | 1.12 | 1.12 | 2.79 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.91 | 0.00 | 1.12 | 3.91 | 0.00 | 1.40 | 2.09 | 0.00 | 2.23 | 0.00 | 0.00 | 0.00 | 2.93 | 0.00 | 0.00 |
| `TiDB Brand & Definitions` | 0.72 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.57 | 0.00 | 0.00 | 0.00 | 2.96 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.72 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.72 | 0.72 | 0.00 |

### Recommendation Rate

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale | AlloyDB | Aurora | AuroraDSQL | Chroma | ClickHouse | Databricks | Druid | Elasticsearch | MariaDB | Milvus | MongoDB | MySQL | OceanBase | OpenSearch | Percona | Pinecone | Pinot | PostgreSQL | Qdrant | RDS | Redis | SingleStore | Snowflake | Spanner | StarRocks | TimescaleDB | Vespa | Vitess | Weaviate | pgvector |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `AI Agent Infrastructure` | 10.26 | 10.53 | 0.85 | 16.24 | 5.98 | 0.85 | 0.85 | 1.71 | 0.00 | 1.71 | 4.27 | 1.71 | 0.00 | 0.85 | 0.00 | 10.26 | 11.11 | 0.85 | 0.00 | 0.00 | 0.00 | 21.37 | 0.00 | 63.25 | 23.93 | 0.85 | 23.93 | 3.42 | 1.71 | 0.85 | 0.00 | 3.42 | 0.00 | 0.00 | 15.38 | 41.03 |
| `Competitive Comparisons` | 4.44 | 33.33 | 1.08 | 0.00 | 0.00 | 3.33 | 0.00 | 6.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.33 | 0.00 | 37.33 | 0.00 | 0.00 | 1.04 | 1.08 | 0.00 | 23.66 | 2.08 | 5.38 | 0.00 | 1.11 | 2.15 | 1.08 | 0.00 | 1.04 | 0.00 | 6.45 | 0.00 | 7.29 |
| `Deployment & Cloud` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 26.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 23.81 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 4.76 | 0.00 | 14.29 |
| `Enterprise & Compliance` | 16.67 | 16.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 16.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 50.00 | 0.00 | 16.67 | 0.00 | 16.67 | 33.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 50.00 |
| `Hybrid Search & RAG` | 2.47 | 10.42 | 2.47 | 0.00 | 1.23 | 0.00 | 0.00 | 1.23 | 0.00 | 0.00 | 0.00 | 1.23 | 0.00 | 12.82 | 0.00 | 14.10 | 10.67 | 1.33 | 0.00 | 8.97 | 0.00 | 11.54 | 0.00 | 46.67 | 19.23 | 0.00 | 6.17 | 6.17 | 0.00 | 0.00 | 0.00 | 0.00 | 6.17 | 0.00 | 21.79 | 45.45 |
| `MCP & Developer Tooling` | 8.33 | 33.33 | 0.00 | 16.67 | 16.67 | 25.00 | 16.67 | 16.67 | 0.00 | 0.00 | 0.00 | 8.33 | 0.00 | 0.00 | 0.00 | 8.33 | 16.67 | 11.11 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 66.67 | 8.33 | 16.67 | 8.33 | 8.33 | 16.67 | 0.00 | 0.00 | 0.00 | 0.00 | 8.33 | 0.00 | 33.33 |
| `MySQL Scale & Migration` | 18.18 | 57.58 | 0.00 | 0.00 | 0.00 | 24.24 | 0.00 | 9.09 | 0.00 | 0.00 | 3.03 | 0.00 | 3.03 | 0.00 | 0.00 | 0.00 | 0.00 | 100.00 | 0.00 | 0.00 | 6.06 | 0.00 | 3.03 | 6.06 | 0.00 | 6.06 | 0.00 | 9.09 | 0.00 | 3.03 | 0.00 | 0.00 | 0.00 | 42.42 | 0.00 | 0.00 |
| `Observability` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `Scale & Architecture` | 44.44 | 29.63 | 11.11 | 18.52 | 7.41 | 22.22 | 0.00 | 3.70 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 11.11 | 0.00 | 9.52 | 0.00 | 0.00 | 0.00 | 7.41 | 0.00 | 55.56 | 7.41 | 0.00 | 11.11 | 3.70 | 0.00 | 7.41 | 0.00 | 0.00 | 0.00 | 25.93 | 0.00 | 3.70 |
| `TiDB Brand & Definitions` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 33.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## Coverage

| Target | Non-branded prompts | Branded prompts | Target-answer rows |
| --- | ---: | ---: | ---: |
| CockroachDB | 217 | 2 | 657 |
| TiDB | 81 | 138 | 657 |
| YugabyteDB | 218 | 1 | 657 |
| Neon | 214 | 5 | 657 |
| Supabase | 216 | 3 | 657 |
| PlanetScale | 216 | 3 | 657 |
| AlloyDB | 219 | 0 | 657 |
| Aurora | 217 | 2 | 657 |
| AuroraDSQL | 219 | 0 | 657 |
| Chroma | 218 | 1 | 657 |
| ClickHouse | 219 | 0 | 657 |
| Databricks | 218 | 1 | 657 |
| Druid | 219 | 0 | 657 |
| Elasticsearch | 218 | 1 | 657 |
| MariaDB | 219 | 0 | 657 |
| Milvus | 216 | 3 | 657 |
| MongoDB | 216 | 3 | 657 |
| MySQL | 194 | 25 | 657 |
| OceanBase | 219 | 0 | 657 |
| OpenSearch | 218 | 1 | 657 |
| Percona | 219 | 0 | 657 |
| Pinecone | 217 | 2 | 657 |
| Pinot | 219 | 0 | 657 |
| PostgreSQL | 216 | 3 | 657 |
| Qdrant | 218 | 1 | 657 |
| RDS | 218 | 1 | 657 |
| Redis | 219 | 0 | 657 |
| SingleStore | 216 | 3 | 657 |
| Snowflake | 218 | 1 | 657 |
| Spanner | 218 | 1 | 657 |
| StarRocks | 219 | 0 | 657 |
| TimescaleDB | 219 | 0 | 657 |
| Vespa | 219 | 0 | 657 |
| Vitess | 218 | 1 | 657 |
| Weaviate | 217 | 2 | 657 |
| pgvector | 214 | 5 | 657 |

| Target | Visibility answers | Recommendation-eligible answers | Consideration-eligible answers |
| --- | ---: | ---: | ---: |
| CockroachDB | 651 | 390 | 651 |
| TiDB | 243 | 243 | 243 |
| YugabyteDB | 654 | 393 | 654 |
| Neon | 642 | 381 | 642 |
| Supabase | 648 | 387 | 648 |
| PlanetScale | 648 | 387 | 648 |
| AlloyDB | 657 | 396 | 657 |
| Aurora | 651 | 390 | 651 |
| AuroraDSQL | 657 | 396 | 657 |
| Chroma | 654 | 393 | 654 |
| ClickHouse | 657 | 396 | 657 |
| Databricks | 654 | 393 | 654 |
| Druid | 657 | 396 | 657 |
| Elasticsearch | 654 | 393 | 654 |
| MariaDB | 657 | 396 | 657 |
| Milvus | 648 | 387 | 648 |
| MongoDB | 648 | 387 | 648 |
| MySQL | 582 | 327 | 582 |
| OceanBase | 657 | 396 | 657 |
| OpenSearch | 654 | 393 | 654 |
| Percona | 657 | 396 | 657 |
| Pinecone | 651 | 390 | 651 |
| Pinot | 657 | 396 | 657 |
| PostgreSQL | 648 | 387 | 648 |
| Qdrant | 654 | 393 | 654 |
| RDS | 654 | 393 | 654 |
| Redis | 657 | 396 | 657 |
| SingleStore | 648 | 387 | 648 |
| Snowflake | 654 | 393 | 654 |
| Spanner | 654 | 393 | 654 |
| StarRocks | 657 | 396 | 657 |
| TimescaleDB | 657 | 396 | 657 |
| Vespa | 657 | 396 | 657 |
| Vitess | 654 | 393 | 654 |
| Weaviate | 651 | 390 | 651 |
| pgvector | 642 | 381 | 642 |

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

- Comparison answers: 6
- Excluded pending prompt review: 3
- Eligible answers without a detected winner: 2
- Conditional / use-case split answers: 1
- No clear winner answers: 1
- Valid comparison answers (detected winners only): 1
- Target win rate: 100.00% (n = 1) — low sample
- Winner counts: {'Aurora': 1}

### Chroma

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 3
- Conditional / use-case split answers: 3
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 0
- Target win rate: N/A
- Winner counts: {}

### CockroachDB

- Comparison answers: 6
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 4
- Conditional / use-case split answers: 2
- No clear winner answers: 2
- Valid comparison answers (detected winners only): 2
- Target win rate: 0.00% (n = 2) — low sample
- Winner counts: {'TiDB': 2}

### Databricks

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 3
- Conditional / use-case split answers: 2
- No clear winner answers: 1
- Valid comparison answers (detected winners only): 0
- Target win rate: N/A
- Winner counts: {}

### Elasticsearch

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 1
- Conditional / use-case split answers: 1
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 2
- Target win rate: 50.00% (n = 2) — low sample
- Winner counts: {'TiDB': 1, 'Elasticsearch': 1}

### Milvus

- Comparison answers: 9
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 3
- Conditional / use-case split answers: 3
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 6
- Target win rate: 83.33% (n = 6) — low sample
- Winner counts: {'Milvus': 5, 'TiDB': 1}

### MongoDB

- Comparison answers: 6
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 3
- Conditional / use-case split answers: 3
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 3
- Target win rate: 33.33% (n = 3) — low sample
- Winner counts: {'TiDB': 2, 'MongoDB': 1}

### MySQL

- Comparison answers: 30
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 23
- Conditional / use-case split answers: 11
- No clear winner answers: 12
- Valid comparison answers (detected winners only): 7
- Target win rate: 0.00% (n = 7) — low sample
- Winner counts: {'TiDB': 6, 'Aurora': 1}

### Neon

- Comparison answers: 15
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 14
- Conditional / use-case split answers: 12
- No clear winner answers: 2
- Valid comparison answers (detected winners only): 1
- Target win rate: 100.00% (n = 1) — low sample
- Winner counts: {'Neon': 1}

### OpenSearch

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 2
- Conditional / use-case split answers: 2
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 100.00% (n = 1) — low sample
- Winner counts: {'OpenSearch': 1}

### Pinecone

- Comparison answers: 6
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 3
- Conditional / use-case split answers: 2
- No clear winner answers: 1
- Valid comparison answers (detected winners only): 3
- Target win rate: 33.33% (n = 3) — low sample
- Winner counts: {'TiDB': 2, 'Pinecone': 1}

### PlanetScale

- Comparison answers: 9
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 7
- Conditional / use-case split answers: 4
- No clear winner answers: 3
- Valid comparison answers (detected winners only): 2
- Target win rate: 0.00% (n = 2) — low sample
- Winner counts: {'TiDB': 2}

### PostgreSQL

- Comparison answers: 6
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 5
- Conditional / use-case split answers: 3
- No clear winner answers: 2
- Valid comparison answers (detected winners only): 1
- Target win rate: 100.00% (n = 1) — low sample
- Winner counts: {'PostgreSQL': 1}

### Qdrant

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 2
- Conditional / use-case split answers: 2
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### RDS

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 2
- Conditional / use-case split answers: 2
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### SingleStore

- Comparison answers: 9
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 5
- Conditional / use-case split answers: 4
- No clear winner answers: 1
- Valid comparison answers (detected winners only): 4
- Target win rate: 50.00% (n = 4) — low sample
- Winner counts: {'TiDB': 2, 'SingleStore': 2}

### Snowflake

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 1
- Conditional / use-case split answers: 1
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 2
- Target win rate: 0.00% (n = 2) — low sample
- Winner counts: {'TiDB': 2}

### Spanner

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 1
- Conditional / use-case split answers: 1
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 2
- Target win rate: 50.00% (n = 2) — low sample
- Winner counts: {'TiDB': 1, 'Spanner': 1}

### Supabase

- Comparison answers: 9
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 9
- Conditional / use-case split answers: 6
- No clear winner answers: 3
- Valid comparison answers (detected winners only): 0
- Target win rate: N/A
- Winner counts: {}

### TiDB

- Comparison answers: 153
- Excluded pending prompt review: 3
- Eligible answers without a detected winner: 102
- Conditional / use-case split answers: 68
- No clear winner answers: 34
- Valid comparison answers (detected winners only): 48
- Target win rate: 62.50% (n = 48)
- Winner counts: {'TiDB': 30, 'OpenSearch': 1, 'Milvus': 5, 'SingleStore': 2, 'Weaviate': 3, 'Elasticsearch': 1, 'MongoDB': 1, 'Aurora': 1, 'Spanner': 1, 'Pinecone': 1, 'PostgreSQL': 1, 'Neon': 1}

### Vitess

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 2
- Conditional / use-case split answers: 2
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### Weaviate

- Comparison answers: 6
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 3
- Conditional / use-case split answers: 2
- No clear winner answers: 1
- Valid comparison answers (detected winners only): 3
- Target win rate: 100.00% (n = 3) — low sample
- Winner counts: {'Weaviate': 3}

### YugabyteDB

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 3
- Conditional / use-case split answers: 2
- No clear winner answers: 1
- Valid comparison answers (detected winners only): 0
- Target win rate: N/A
- Winner counts: {}

### pgvector

- Comparison answers: 6
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 5
- Conditional / use-case split answers: 2
- No clear winner answers: 3
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

## Cost

- Saved-answer usage estimate: $26.2203
- Scope: Usage estimate for successful saved answers in this report's search mode. Not a billing ledger; excludes failed or overwritten attempts and may include answers collected previously.
- Pricing version: 2026-09-03
- Fact judge mode: off
- Fact judge estimated cost: $0.0
- Combined provider and judge cost: $26.2203
- Judge cost covers this scoring invocation. Cache hits add no new judge calls; previous judge charges are not included. The combined figure is not lifetime project spend.

- anthropic saved token cost: $12.0266; saved web search cost: $4.27.
- gemini saved token cost: $0.254; saved web search cost: $4.97.
- openai saved token cost: $1.3097; saved web search cost: $3.39.

- Planned fresh-collection estimate: $3.4548
- Planned scope: 219 prompts × 1 runs per provider.
- Selected prompts and providers, assuming fresh collection; excludes fact judging, retries and fallback. Not an incremental bill for rerunning cached answers.
- Assumptions: Input tokens are approximated from prompt text. Output tokens and searches per answer use previous saved usage when available, otherwise provider config; explicit output-token overrides take precedence.

- gemini planned token cost: $0.3888; planned web search cost: $3.066.
- gemini assumptions: 700.0 output tokens per answer from models config; 1.0 searches per answer from models config.

## Run Metadata

- Prompt set hash (effective metadata): `6dde3e4577f292823c5955d18ab10577ce8464ac1a70405348c8edc195852d9d`
- Frozen source prompt hash: `f60c9f578eb58f2d783842ba0389387f3fdd5ddaa7c4d5354f2614715e6a6460`
- Prompt metadata revision: `2026-09-18-review-1`
- Legacy facts version: `2026-07-30`
- Semantic fact-base version: `None`
- Source-authority version: `2026-09-25-path-aware`
- Models config hash: `ae56ecaf99b8952f55872823f42888b68afb776dbec663b53f7104ce1be9a084`

## Semantic Coverage Audit

Decision coverage is not processing coverage. Comparison-only mappings can occur in any topic cluster. A legacy checked-fact count does not establish semantic eligibility.

| Outcome | Branded answers | Explanation |
| --- | ---: | --- |
| disabled | 414 | Semantic judging was disabled for this answer. |

Reconciled total: 414/414 branded answers. See `semantic-coverage-audit.csv` for exact prompt/provider IDs and pending fact IDs. Scored answers may still have pending review items. Existing accuracy and coverage denominators are unchanged.

## Cited Domain Analysis

Domains are ranked by the number of unique prompts for which they were cited. Open the [filterable cited-domain report](cited-domains.html) for answer-level evidence.

| Domain | Type | Prompts | Cited answers | TiDB appeared | Recommended products |
| --- | --- | ---: | ---: | ---: | --- |
| pingcap.com | PingCAP | 191 | 403 | 180 | TiDB (24), PostgreSQL (4), Vitess (3), SingleStore (2), MySQL (1), Neon (1), OpenSearch (1), PlanetScale (1), Qdrant (1), YugabyteDB (1) |
| docs.pingcap.com | PingCAP | 129 | 277 | 129 | TiDB (22), PostgreSQL (3), MySQL (1), Neon (1), OpenSearch (1), Qdrant (1), SingleStore (1), Weaviate (1) |
| medium.com | Other | 87 | 105 | 60 | TiDB (4), PostgreSQL (3), Neon (1), Qdrant (1), Vitess (1), YugabyteDB (1) |
| arxiv.org | Other | 86 | 98 | 59 | TiDB (6), Milvus (1), Neon (1), OpenSearch (1), Qdrant (1), SingleStore (1), pgvector (1) |
| dev.to | Other | 83 | 96 | 56 | TiDB (4), Neon (1), PostgreSQL (1), Qdrant (1), YugabyteDB (1), pgvector (1) |
| youtube.com | Other | 62 | 63 | 44 | TiDB (3), MongoDB (2), Neon (2) |
| en.wikipedia.org | Other | 51 | 54 | 46 | TiDB (5), Milvus (1), OpenSearch (1), Qdrant (1) |
| pingcap.co.jp | PingCAP | 49 | 50 | 48 | TiDB (8), OpenSearch (1), PostgreSQL (1), Qdrant (1) |
| redis.io | Competitor | 39 | 59 | 12 | Milvus (2), PostgreSQL (2), YugabyteDB (1), pgvector (1) |
| aws.amazon.com | Competitor | 38 | 46 | 27 | TiDB (2), Aurora (1), PlanetScale (1) |

Recommendations are observed in answers that cite the domain; this is an association, not proof of causation.
