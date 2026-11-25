# GEO Benchmark LLM Report - 2026-11

Providers: anthropic, gemini, openai
Web search mode: on
Saved raw records: 690
Successfully scored answers: 690
Failed raw records: 0
Incomplete raw records: 0
Scored target-answer rows: 24840

## Executive KPI

| Target | Consideration Rate | Mention Rate | Prominence Score | Citation Authority | Recommendation Rate | Comparison Win Rate | Stable Consideration Rate | Stable Mention Rate | Stable Prominence Score | Stable Recommendation Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 5.70 | 13.45 | 5.91 | 2.31 | 10.40 | 0.00% (n = 2) — low sample | 5.70 | 13.45 | 5.91 | 10.40 |
| TiDB | 9.97 | 29.71 | 14.74 | 13.43 | 20.29 | 56.00% (n = 50) | 9.97 | 29.71 | 14.74 | 20.29 |
| YugabyteDB | 2.50 | 5.53 | 1.91 | 1.23 | 2.58 | N/A | 2.50 | 5.53 | 1.91 | 2.58 |
| Neon | 2.07 | 7.85 | 3.90 | 0.75 | 8.94 | 100.00% (n = 1) — low sample | 2.07 | 7.85 | 3.90 | 8.94 |
| Supabase | 1.08 | 4.55 | 1.76 | 0.54 | 2.86 | 100.00% (n = 1) — low sample | 1.08 | 4.55 | 1.76 | 2.86 |
| PlanetScale | 3.13 | 5.14 | 1.71 | 0.52 | 4.29 | 25.00% (n = 4) — low sample | 3.13 | 5.14 | 1.71 | 4.29 |
| AlloyDB | 0.00 | 1.01 | 0.32 | 0.05 | 0.47 | N/A | 0.00 | 1.01 | 0.32 | 0.47 |
| Aurora | 2.34 | 9.80 | 3.23 | 0.50 | 6.15 | 0.00% (n = 1) — low sample | 2.34 | 9.80 | 3.23 | 6.15 |
| AuroraDSQL | 0.00 | 0.29 | 0.06 | 0.00 | 0.23 | N/A | 0.00 | 0.29 | 0.06 | 0.23 |
| Chroma | 0.95 | 2.04 | 0.91 | 0.13 | 1.41 | 100.00% (n = 2) — low sample | 0.95 | 2.04 | 0.91 | 1.41 |
| ClickHouse | 0.89 | 2.32 | 0.85 | 1.05 | 1.86 | N/A | 0.89 | 2.32 | 0.85 | 1.86 |
| Databricks | 0.18 | 3.35 | 1.29 | 2.16 | 2.11 | 0.00% (n = 1) — low sample | 0.18 | 3.35 | 1.29 | 2.11 |
| Druid | 0.00 | 0.14 | 0.02 | 0.00 | 0.00 | N/A | 0.00 | 0.14 | 0.02 | 0.00 |
| Elasticsearch | 1.13 | 4.22 | 1.62 | 0.57 | 2.58 | 100.00% (n = 2) — low sample | 1.13 | 4.22 | 1.62 | 2.58 |
| MariaDB | 0.83 | 2.75 | 0.83 | 0.40 | 0.47 | N/A | 0.83 | 2.75 | 0.83 | 0.47 |
| Milvus | 8.56 | 14.83 | 4.71 | 3.10 | 5.48 | 80.00% (n = 5) — low sample | 8.56 | 14.83 | 4.71 | 5.48 |
| MongoDB | 0.96 | 4.55 | 1.85 | 0.47 | 3.81 | 100.00% (n = 1) — low sample | 0.96 | 4.55 | 1.85 | 3.81 |
| MySQL | 4.86 | 37.56 | 19.79 | 0.16 | 14.44 | 12.50% (n = 8) — low sample | 4.86 | 37.56 | 19.79 | 14.44 |
| OceanBase | 0.00 | 1.16 | 0.25 | 0.51 | 0.47 | N/A | 0.00 | 1.16 | 0.25 | 0.47 |
| OpenSearch | 0.48 | 3.35 | 1.13 | 0.10 | 2.11 | 100.00% (n = 1) — low sample | 0.48 | 3.35 | 1.13 | 2.11 |
| Percona | 0.71 | 0.87 | 0.15 | 0.34 | 0.47 | N/A | 0.71 | 0.87 | 0.15 | 0.47 |
| Pinecone | 7.31 | 18.13 | 6.77 | 2.01 | 10.64 | 0.00% (n = 2) — low sample | 7.31 | 18.13 | 6.77 | 10.64 |
| Pinot | 0.12 | 0.29 | 0.09 | 0.09 | 0.00 | N/A | 0.12 | 0.29 | 0.09 | 0.00 |
| PostgreSQL | 13.06 | 46.55 | 27.21 | 0.91 | 48.10 | 100.00% (n = 1) — low sample | 13.06 | 46.55 | 27.21 | 48.10 |
| Qdrant | 4.65 | 17.03 | 5.82 | 1.77 | 10.09 | 0.00% (n = 1) — low sample | 4.65 | 17.03 | 5.82 | 10.09 |
| RDS | 0.89 | 4.66 | 1.97 | 0.00 | 3.99 | 0.00% (n = 1) — low sample | 0.89 | 4.66 | 1.97 | 3.99 |
| Redis | 4.63 | 13.48 | 5.73 | 4.32 | 9.79 | N/A | 4.63 | 13.48 | 5.73 | 9.79 |
| SingleStore | 1.62 | 3.82 | 1.31 | 0.73 | 1.43 | 100.00% (n = 4) — low sample | 1.62 | 3.82 | 1.31 | 1.43 |
| Snowflake | 0.48 | 2.47 | 1.03 | 0.14 | 1.17 | 0.00% (n = 1) — low sample | 0.48 | 2.47 | 1.03 | 1.17 |
| Spanner | 1.25 | 3.78 | 1.41 | 0.69 | 1.64 | 100.00% (n = 1) — low sample | 1.25 | 3.78 | 1.41 | 1.64 |
| StarRocks | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 |
| TimescaleDB | 0.30 | 1.30 | 0.50 | 0.21 | 1.17 | N/A | 0.30 | 1.30 | 0.50 | 1.17 |
| Vespa | 0.47 | 1.01 | 0.27 | 0.22 | 0.70 | N/A | 0.47 | 1.01 | 0.27 | 0.70 |
| Vitess | 3.04 | 8.30 | 3.09 | 0.96 | 6.34 | 0.00% (n = 1) — low sample | 3.04 | 8.30 | 3.09 | 6.34 |
| Weaviate | 4.74 | 13.30 | 4.52 | 1.85 | 8.98 | 100.00% (n = 1) — low sample | 4.74 | 13.30 | 4.52 | 8.98 |
| pgvector | 10.06 | 26.81 | 11.52 | 1.05 | 23.67 | N/A | 10.06 | 26.81 | 11.52 | 23.67 |

## Branded Accuracy

| Target | Prompts | Legacy accuracy | Legacy coverage | Semantic accuracy | Semantic decision coverage | Judge unavailable |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 2 | 72.22 | 100.00% | N/A | 0.00% | 0 |
| TiDB | 138 | 52.36 | 100.00% | N/A | 0.00% | 0 |
| YugabyteDB | 1 | 100.00 | 100.00% | N/A | 0.00% | 0 |
| Neon | 5 | 20.00 | 100.00% | N/A | 0.00% | 0 |
| Supabase | 3 | 77.78 | 100.00% | N/A | 0.00% | 0 |
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
| `AI Agent Infrastructure` | 8.14 | 0.63 | 1.78 | 7.12 | 4.07 | 3.56 | 0.00 | 1.53 | 0.00 | 3.56 | 2.29 | 0.00 | 0.00 | 0.51 | 0.00 | 14.25 | 1.27 | 1.53 | 0.00 | 0.51 | 0.00 | 16.28 | 0.51 | 25.45 | 12.72 | 2.04 | 12.72 | 1.27 | 1.02 | 0.51 | 0.00 | 0.51 | 0.51 | 1.02 | 9.92 | 20.61 |
| `Competitive Comparisons` | 2.62 | 33.33 | 1.81 | 0.00 | 0.00 | 1.12 | 0.00 | 2.25 | 0.00 | 0.00 | 0.00 | 1.09 | 0.00 | 0.00 | 0.00 | 4.12 | 0.00 | 10.67 | 0.00 | 0.00 | 0.00 | 2.17 | 0.00 | 13.04 | 0.00 | 0.00 | 0.00 | 0.75 | 0.00 | 1.09 | 0.00 | 1.05 | 0.00 | 3.26 | 0.00 | 7.37 |
| `Deployment & Cloud` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 1.85 | 0.00 | 1.75 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.96 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.75 | 0.00 | 1.75 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.75 |
| `Enterprise & Compliance` | 6.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 6.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 6.67 | 0.00 | 0.00 | 0.00 | 0.00 | 13.33 | 0.00 | 13.33 | 6.67 | 6.67 | 20.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 6.67 | 6.67 |
| `Hybrid Search & RAG` | 3.44 | 4.04 | 1.37 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.69 | 0.00 | 0.00 | 0.00 | 6.03 | 0.00 | 20.92 | 1.45 | 0.00 | 0.00 | 2.13 | 0.00 | 14.18 | 0.00 | 17.39 | 9.22 | 0.00 | 4.81 | 1.37 | 1.37 | 2.06 | 0.00 | 0.00 | 2.06 | 0.00 | 11.35 | 18.43 |
| `MCP & Developer Tooling` | 2.90 | 8.33 | 0.00 | 0.00 | 2.90 | 5.80 | 0.00 | 2.90 | 0.00 | 0.00 | 2.90 | 0.00 | 0.00 | 0.00 | 2.90 | 5.80 | 0.00 | 3.17 | 0.00 | 0.00 | 0.00 | 2.90 | 0.00 | 8.70 | 0.00 | 0.00 | 2.90 | 2.90 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.90 | 8.70 |
| `MySQL Scale & Migration` | 22.22 | 57.58 | 9.88 | 0.00 | 0.00 | 19.75 | 0.00 | 9.88 | 0.00 | 0.00 | 2.47 | 0.00 | 0.00 | 0.00 | 12.35 | 0.00 | 0.00 | 83.33 | 0.00 | 0.00 | 12.35 | 0.00 | 0.00 | 4.94 | 0.00 | 0.00 | 0.00 | 12.35 | 0.00 | 7.41 | 0.00 | 0.00 | 0.00 | 34.57 | 0.00 | 0.00 |
| `Observability` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Scale & Architecture` | 13.95 | 17.54 | 9.30 | 4.65 | 0.00 | 9.30 | 0.00 | 6.20 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.55 | 3.10 | 3.88 | 3.42 | 0.00 | 0.00 | 1.55 | 3.10 | 0.00 | 9.30 | 0.00 | 0.00 | 4.65 | 3.10 | 0.00 | 3.10 | 0.00 | 0.00 | 0.00 | 6.20 | 1.55 | 1.55 |
| `TiDB Brand & Definitions` | 2.99 | N/A | 2.99 | 0.00 | 0.00 | 0.00 | 0.00 | 1.99 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.98 | 0.00 | 11.94 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.99 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.99 |

### Mention Rate

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale | AlloyDB | Aurora | AuroraDSQL | Chroma | ClickHouse | Databricks | Druid | Elasticsearch | MariaDB | Milvus | MongoDB | MySQL | OceanBase | OpenSearch | Percona | Pinecone | Pinot | PostgreSQL | Qdrant | RDS | Redis | SingleStore | Snowflake | Spanner | StarRocks | TimescaleDB | Vespa | Vitess | Weaviate | pgvector |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `AI Agent Infrastructure` | 14.69 | 19.73 | 2.82 | 23.16 | 11.30 | 5.65 | 1.69 | 7.34 | 0.00 | 5.65 | 3.39 | 10.17 | 0.56 | 1.13 | 0.00 | 18.08 | 9.04 | 14.69 | 0.56 | 0.00 | 0.00 | 36.16 | 1.13 | 73.45 | 34.46 | 5.08 | 40.11 | 2.82 | 1.69 | 1.69 | 0.00 | 1.69 | 0.00 | 2.26 | 22.60 | 48.59 |
| `Competitive Comparisons` | 11.11 | 66.67 | 5.38 | 2.38 | 0.00 | 2.22 | 0.00 | 10.00 | 1.04 | 1.08 | 2.08 | 0.00 | 0.00 | 1.04 | 0.00 | 11.11 | 0.00 | 62.67 | 0.00 | 1.04 | 1.04 | 7.53 | 0.00 | 44.09 | 4.17 | 3.23 | 1.04 | 2.22 | 1.08 | 6.45 | 0.00 | 0.00 | 0.00 | 10.75 | 5.38 | 17.71 |
| `Deployment & Cloud` | 0.00 | N/A | 0.00 | 1.75 | 3.51 | 1.75 | 0.00 | 3.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 62.96 | 0.00 | 0.00 | 0.00 | 1.67 | 0.00 | 11.67 | 0.00 | 5.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.33 | 0.00 | 5.00 |
| `Enterprise & Compliance` | 8.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 8.33 | 16.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 16.67 | 25.00 | 0.00 | 0.00 | 0.00 | 0.00 | 8.33 | 0.00 | 25.00 | 8.33 | 25.00 | 25.00 | 0.00 | 8.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 25.00 |
| `Hybrid Search & RAG` | 6.84 | 8.33 | 2.56 | 1.71 | 0.85 | 0.00 | 1.71 | 4.27 | 0.00 | 2.56 | 0.85 | 0.00 | 0.00 | 22.81 | 0.00 | 36.84 | 8.11 | 22.52 | 0.00 | 19.30 | 0.00 | 30.70 | 0.00 | 54.05 | 36.84 | 2.56 | 6.84 | 4.27 | 0.85 | 3.42 | 0.00 | 5.13 | 5.98 | 0.00 | 35.09 | 50.98 |
| `MCP & Developer Tooling` | 3.33 | 16.67 | 0.00 | 6.67 | 20.00 | 10.00 | 0.00 | 16.67 | 0.00 | 0.00 | 10.00 | 0.00 | 0.00 | 0.00 | 6.67 | 16.67 | 0.00 | 44.44 | 0.00 | 0.00 | 0.00 | 10.00 | 0.00 | 46.67 | 13.33 | 6.67 | 10.00 | 3.33 | 6.67 | 0.00 | 0.00 | 0.00 | 0.00 | 10.00 | 10.00 | 26.67 |
| `MySQL Scale & Migration` | 35.90 | 100.00 | 28.21 | 0.00 | 0.00 | 28.21 | 0.00 | 23.08 | 2.56 | 0.00 | 5.13 | 2.56 | 0.00 | 0.00 | 20.51 | 0.00 | 2.56 | 100.00 | 12.82 | 0.00 | 10.26 | 0.00 | 0.00 | 43.59 | 0.00 | 2.56 | 0.00 | 23.08 | 2.56 | 15.38 | 0.00 | 0.00 | 0.00 | 66.67 | 0.00 | 0.00 |
| `Observability` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Scale & Architecture` | 44.44 | 44.44 | 18.52 | 9.26 | 3.70 | 12.96 | 0.00 | 16.67 | 0.00 | 0.00 | 0.00 | 5.56 | 0.00 | 0.00 | 1.85 | 5.56 | 0.00 | 45.83 | 3.70 | 0.00 | 1.85 | 7.41 | 0.00 | 50.00 | 1.85 | 12.96 | 7.41 | 3.70 | 0.00 | 5.56 | 0.00 | 0.00 | 0.00 | 20.37 | 3.70 | 9.26 |
| `TiDB Brand & Definitions` | 8.60 | N/A | 4.30 | 0.00 | 0.00 | 1.08 | 1.08 | 13.98 | 0.00 | 0.00 | 2.15 | 1.08 | 0.00 | 0.00 | 8.60 | 7.53 | 2.15 | 63.44 | 0.00 | 0.00 | 0.00 | 9.68 | 0.00 | 19.35 | 4.30 | 1.08 | 3.23 | 2.22 | 8.60 | 4.30 | 0.00 | 0.00 | 0.00 | 1.08 | 1.08 | 7.53 |

### Prominence Score

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale | AlloyDB | Aurora | AuroraDSQL | Chroma | ClickHouse | Databricks | Druid | Elasticsearch | MariaDB | Milvus | MongoDB | MySQL | OceanBase | OpenSearch | Percona | Pinecone | Pinot | PostgreSQL | Qdrant | RDS | Redis | SingleStore | Snowflake | Spanner | StarRocks | TimescaleDB | Vespa | Vitess | Weaviate | pgvector |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `AI Agent Infrastructure` | 8.50 | 8.99 | 1.02 | 13.18 | 4.78 | 1.88 | 0.31 | 2.80 | 0.00 | 3.21 | 1.68 | 4.38 | 0.10 | 0.20 | 0.00 | 6.77 | 3.61 | 5.80 | 0.15 | 0.00 | 0.00 | 15.32 | 0.41 | 55.17 | 14.10 | 1.58 | 19.34 | 0.81 | 1.32 | 0.51 | 0.00 | 0.71 | 0.00 | 0.46 | 7.53 | 24.94 |
| `Competitive Comparisons` | 3.67 | 26.67 | 2.17 | 0.48 | 0.00 | 0.37 | 0.00 | 4.94 | 0.21 | 0.22 | 0.42 | 0.00 | 0.00 | 0.63 | 0.00 | 2.62 | 0.00 | 28.53 | 0.00 | 0.21 | 0.21 | 1.96 | 0.00 | 18.19 | 0.77 | 1.30 | 0.63 | 0.37 | 0.22 | 2.17 | 0.00 | 0.00 | 0.00 | 2.54 | 1.01 | 5.26 |
| `Deployment & Cloud` | 0.00 | N/A | 0.00 | 0.37 | 1.85 | 0.37 | 0.00 | 0.70 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 34.90 | 0.00 | 0.00 | 0.00 | 1.05 | 0.00 | 4.56 | 0.00 | 3.16 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.40 | 0.00 | 1.05 |
| `Enterprise & Compliance` | 6.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.33 | 8.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 8.00 | 19.33 | 0.00 | 0.00 | 0.00 | 0.00 | 1.33 | 0.00 | 14.67 | 1.33 | 16.67 | 6.67 | 0.00 | 4.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 12.00 |
| `Hybrid Search & RAG` | 2.20 | 3.23 | 0.96 | 0.62 | 0.14 | 0.00 | 1.10 | 1.03 | 0.00 | 0.69 | 0.21 | 0.00 | 0.00 | 8.72 | 0.00 | 11.28 | 3.19 | 9.96 | 0.00 | 6.52 | 0.00 | 11.91 | 0.00 | 32.10 | 12.13 | 1.44 | 1.99 | 1.44 | 0.14 | 1.10 | 0.00 | 1.92 | 1.58 | 0.00 | 14.26 | 21.02 |
| `MCP & Developer Tooling` | 0.58 | 3.33 | 0.00 | 2.32 | 8.99 | 5.22 | 0.00 | 5.22 | 0.00 | 0.00 | 4.06 | 0.00 | 0.00 | 0.00 | 2.32 | 3.48 | 0.00 | 25.71 | 0.00 | 0.00 | 0.00 | 2.32 | 0.00 | 33.33 | 2.61 | 2.32 | 4.93 | 0.58 | 2.32 | 0.00 | 0.00 | 0.00 | 0.00 | 4.06 | 2.32 | 13.04 |
| `MySQL Scale & Migration` | 8.89 | 57.58 | 6.42 | 0.00 | 0.00 | 9.38 | 0.00 | 4.44 | 0.49 | 0.00 | 0.99 | 1.48 | 0.00 | 0.00 | 3.95 | 0.00 | 0.49 | 100.00 | 3.46 | 0.00 | 1.98 | 0.00 | 0.00 | 11.36 | 0.00 | 0.49 | 0.00 | 12.35 | 0.49 | 2.96 | 0.00 | 0.00 | 0.00 | 35.56 | 0.00 | 0.00 |
| `Observability` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Scale & Architecture` | 24.50 | 23.86 | 9.30 | 5.43 | 0.62 | 6.05 | 0.00 | 5.58 | 0.00 | 0.00 | 0.00 | 2.17 | 0.00 | 0.00 | 0.31 | 0.93 | 0.00 | 24.44 | 0.62 | 0.00 | 0.31 | 2.48 | 0.00 | 28.22 | 0.93 | 4.81 | 4.96 | 0.62 | 0.00 | 3.57 | 0.00 | 0.00 | 0.00 | 6.67 | 0.62 | 3.57 |
| `TiDB Brand & Definitions` | 3.88 | N/A | 1.00 | 0.00 | 0.00 | 0.20 | 0.30 | 4.28 | 0.00 | 0.00 | 1.19 | 0.20 | 0.00 | 0.00 | 4.38 | 3.38 | 0.80 | 36.32 | 0.00 | 0.00 | 0.00 | 3.38 | 0.00 | 7.86 | 1.19 | 0.20 | 0.60 | 1.13 | 3.88 | 2.69 | 0.00 | 0.00 | 0.00 | 0.20 | 0.20 | 2.19 |

### Citation Authority

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale | AlloyDB | Aurora | AuroraDSQL | Chroma | ClickHouse | Databricks | Druid | Elasticsearch | MariaDB | Milvus | MongoDB | MySQL | OceanBase | OpenSearch | Percona | Pinecone | Pinot | PostgreSQL | Qdrant | RDS | Redis | SingleStore | Snowflake | Spanner | StarRocks | TimescaleDB | Vespa | Vitess | Weaviate | pgvector |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `AI Agent Infrastructure` | 4.92 | 10.98 | 1.48 | 2.66 | 2.29 | 0.11 | 0.00 | 0.26 | 0.00 | 0.55 | 2.06 | 6.94 | 0.00 | 0.23 | 0.00 | 4.31 | 0.82 | 0.00 | 0.34 | 0.00 | 0.00 | 5.96 | 0.37 | 2.73 | 4.72 | 0.00 | 13.06 | 0.37 | 0.00 | 0.73 | 0.00 | 0.37 | 0.00 | 0.00 | 5.08 | 3.11 |
| `Competitive Comparisons` | 0.88 | 26.25 | 1.31 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 4.08 | 0.00 | 0.00 | 0.00 | 0.00 | 0.47 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.47 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Deployment & Cloud` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Enterprise & Compliance` | 3.20 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 5.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 6.14 | 0.00 | 0.00 | 0.00 | 0.00 | 4.80 | 0.00 | 0.00 | 4.80 | 0.00 | 7.80 | 0.00 | 3.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Hybrid Search & RAG` | 1.67 | 9.77 | 0.55 | 0.00 | 0.00 | 0.00 | 0.31 | 0.00 | 0.00 | 0.00 | 1.98 | 0.62 | 0.00 | 3.10 | 0.00 | 6.38 | 0.98 | 0.00 | 0.00 | 0.57 | 0.00 | 2.74 | 0.00 | 1.07 | 3.45 | 0.00 | 4.09 | 0.96 | 0.49 | 0.49 | 0.00 | 0.74 | 1.30 | 0.00 | 3.86 | 2.01 |
| `MCP & Developer Tooling` | 2.09 | 1.88 | 0.00 | 0.00 | 0.00 | 1.30 | 0.00 | 1.45 | 0.00 | 0.00 | 2.09 | 0.00 | 0.00 | 0.00 | 1.30 | 2.09 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.45 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `MySQL Scale & Migration` | 4.67 | 37.30 | 5.73 | 0.00 | 0.00 | 8.00 | 0.00 | 5.93 | 0.00 | 0.00 | 1.78 | 4.44 | 0.00 | 0.00 | 5.33 | 0.00 | 0.00 | 19.50 | 6.67 | 0.00 | 3.56 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 8.00 | 0.00 | 5.33 | 0.00 | 0.00 | 0.00 | 15.11 | 0.00 | 0.00 |
| `Observability` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `Scale & Architecture` | 4.56 | 12.20 | 3.80 | 1.40 | 0.00 | 0.70 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.79 | 0.00 | 0.00 | 1.12 | 1.12 | 0.00 | 0.00 | 1.40 | 0.00 | 1.12 | 0.70 | 0.00 | 1.12 | 0.00 | 0.00 | 3.76 | 1.12 | 0.00 | 2.23 | 0.00 | 0.00 | 0.00 | 2.93 | 0.00 | 0.00 |
| `TiDB Brand & Definitions` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.45 | 0.00 | 0.00 | 0.00 | 0.00 | 1.34 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### Recommendation Rate

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale | AlloyDB | Aurora | AuroraDSQL | Chroma | ClickHouse | Databricks | Druid | Elasticsearch | MariaDB | Milvus | MongoDB | MySQL | OceanBase | OpenSearch | Percona | Pinecone | Pinot | PostgreSQL | Qdrant | RDS | Redis | SingleStore | Snowflake | Spanner | StarRocks | TimescaleDB | Vespa | Vitess | Weaviate | pgvector |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `AI Agent Infrastructure` | 10.00 | 12.24 | 0.00 | 20.67 | 7.33 | 2.67 | 0.67 | 6.00 | 0.00 | 2.67 | 2.00 | 6.00 | 0.00 | 0.00 | 0.00 | 6.00 | 6.67 | 5.33 | 0.67 | 0.00 | 0.00 | 20.00 | 0.00 | 68.00 | 15.33 | 4.00 | 21.33 | 0.67 | 2.00 | 0.67 | 0.00 | 1.33 | 0.00 | 0.00 | 13.33 | 37.33 |
| `Competitive Comparisons` | 5.56 | 33.33 | 3.23 | 0.00 | 0.00 | 2.22 | 0.00 | 6.67 | 0.00 | 0.00 | 1.04 | 0.00 | 0.00 | 0.00 | 0.00 | 2.22 | 0.00 | 32.00 | 0.00 | 0.00 | 1.04 | 2.15 | 0.00 | 25.81 | 1.04 | 2.15 | 1.04 | 0.00 | 0.00 | 1.08 | 0.00 | 0.00 | 0.00 | 3.23 | 1.08 | 6.25 |
| `Deployment & Cloud` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 5.56 | 0.00 | 4.76 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 33.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 23.81 | 0.00 | 4.76 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 4.76 | 0.00 | 0.00 |
| `Enterprise & Compliance` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 33.33 | 33.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 33.33 | 0.00 | 16.67 | 16.67 | 0.00 | 16.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 16.67 |
| `Hybrid Search & RAG` | 4.94 | 2.08 | 1.23 | 2.47 | 0.00 | 0.00 | 1.23 | 2.47 | 0.00 | 2.47 | 1.23 | 0.00 | 0.00 | 14.10 | 0.00 | 10.26 | 4.00 | 6.67 | 0.00 | 11.54 | 0.00 | 15.38 | 0.00 | 45.33 | 19.23 | 3.70 | 4.94 | 1.23 | 0.00 | 2.47 | 0.00 | 3.70 | 3.70 | 0.00 | 20.51 | 39.39 |
| `MCP & Developer Tooling` | 8.33 | 8.33 | 0.00 | 0.00 | 8.33 | 16.67 | 0.00 | 25.00 | 0.00 | 0.00 | 16.67 | 0.00 | 0.00 | 0.00 | 16.67 | 16.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 75.00 | 25.00 | 16.67 | 8.33 | 8.33 | 8.33 | 0.00 | 0.00 | 0.00 | 0.00 | 16.67 | 8.33 | 33.33 |
| `MySQL Scale & Migration` | 24.24 | 81.82 | 12.12 | 0.00 | 0.00 | 18.18 | 0.00 | 9.09 | 3.03 | 0.00 | 3.03 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.03 | 100.00 | 3.03 | 0.00 | 3.03 | 0.00 | 0.00 | 33.33 | 0.00 | 0.00 | 0.00 | 9.09 | 0.00 | 3.03 | 0.00 | 0.00 | 0.00 | 48.48 | 0.00 | 0.00 |
| `Observability` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `Scale & Architecture` | 40.74 | 29.63 | 11.11 | 14.81 | 0.00 | 11.11 | 0.00 | 7.41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 9.52 | 0.00 | 0.00 | 0.00 | 3.70 | 0.00 | 55.56 | 3.70 | 7.41 | 11.11 | 0.00 | 0.00 | 7.41 | 0.00 | 0.00 | 0.00 | 18.52 | 0.00 | 18.52 |
| `TiDB Brand & Definitions` | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 66.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | N/A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## Coverage

| Target | Non-branded prompts | Branded prompts | Target-answer rows |
| --- | ---: | ---: | ---: |
| CockroachDB | 228 | 2 | 690 |
| TiDB | 92 | 138 | 690 |
| YugabyteDB | 229 | 1 | 690 |
| Neon | 225 | 5 | 690 |
| Supabase | 227 | 3 | 690 |
| PlanetScale | 227 | 3 | 690 |
| AlloyDB | 230 | 0 | 690 |
| Aurora | 228 | 2 | 690 |
| AuroraDSQL | 230 | 0 | 690 |
| Chroma | 229 | 1 | 690 |
| ClickHouse | 230 | 0 | 690 |
| Databricks | 229 | 1 | 690 |
| Druid | 230 | 0 | 690 |
| Elasticsearch | 229 | 1 | 690 |
| MariaDB | 230 | 0 | 690 |
| Milvus | 227 | 3 | 690 |
| MongoDB | 227 | 3 | 690 |
| MySQL | 205 | 25 | 690 |
| OceanBase | 230 | 0 | 690 |
| OpenSearch | 229 | 1 | 690 |
| Percona | 230 | 0 | 690 |
| Pinecone | 228 | 2 | 690 |
| Pinot | 230 | 0 | 690 |
| PostgreSQL | 227 | 3 | 690 |
| Qdrant | 229 | 1 | 690 |
| RDS | 229 | 1 | 690 |
| Redis | 230 | 0 | 690 |
| SingleStore | 227 | 3 | 690 |
| Snowflake | 229 | 1 | 690 |
| Spanner | 229 | 1 | 690 |
| StarRocks | 230 | 0 | 690 |
| TimescaleDB | 230 | 0 | 690 |
| Vespa | 230 | 0 | 690 |
| Vitess | 229 | 1 | 690 |
| Weaviate | 228 | 2 | 690 |
| pgvector | 225 | 5 | 690 |

| Target | Visibility answers | Recommendation-eligible answers | Consideration-eligible answers |
| --- | ---: | ---: | ---: |
| CockroachDB | 684 | 423 | 684 |
| TiDB | 276 | 276 | 276 |
| YugabyteDB | 687 | 426 | 687 |
| Neon | 675 | 414 | 675 |
| Supabase | 681 | 420 | 681 |
| PlanetScale | 681 | 420 | 681 |
| AlloyDB | 690 | 429 | 690 |
| Aurora | 684 | 423 | 684 |
| AuroraDSQL | 690 | 429 | 690 |
| Chroma | 687 | 426 | 687 |
| ClickHouse | 690 | 429 | 690 |
| Databricks | 687 | 426 | 687 |
| Druid | 690 | 429 | 690 |
| Elasticsearch | 687 | 426 | 687 |
| MariaDB | 690 | 429 | 690 |
| Milvus | 681 | 420 | 681 |
| MongoDB | 681 | 420 | 681 |
| MySQL | 615 | 360 | 615 |
| OceanBase | 690 | 429 | 690 |
| OpenSearch | 687 | 426 | 687 |
| Percona | 690 | 429 | 690 |
| Pinecone | 684 | 423 | 684 |
| Pinot | 690 | 429 | 690 |
| PostgreSQL | 681 | 420 | 681 |
| Qdrant | 687 | 426 | 687 |
| RDS | 687 | 426 | 687 |
| Redis | 690 | 429 | 690 |
| SingleStore | 681 | 420 | 681 |
| Snowflake | 687 | 426 | 687 |
| Spanner | 687 | 426 | 687 |
| StarRocks | 690 | 429 | 690 |
| TimescaleDB | 690 | 429 | 690 |
| Vespa | 690 | 429 | 690 |
| Vitess | 687 | 426 | 687 |
| Weaviate | 684 | 423 | 684 |
| pgvector | 675 | 414 | 675 |

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
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### Chroma

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 1
- Conditional / use-case split answers: 1
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 2
- Target win rate: 100.00% (n = 2) — low sample
- Winner counts: {'Chroma': 2}

### CockroachDB

- Comparison answers: 6
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 4
- Conditional / use-case split answers: 2
- No clear winner answers: 2
- Valid comparison answers (detected winners only): 2
- Target win rate: 0.00% (n = 2) — low sample
- Winner counts: {'PostgreSQL': 1, 'TiDB': 1}

### Databricks

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 2
- Conditional / use-case split answers: 2
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### Elasticsearch

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 1
- Conditional / use-case split answers: 1
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 2
- Target win rate: 100.00% (n = 2) — low sample
- Winner counts: {'Elasticsearch': 2}

### Milvus

- Comparison answers: 9
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 4
- Conditional / use-case split answers: 4
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 5
- Target win rate: 80.00% (n = 5) — low sample
- Winner counts: {'Milvus': 4, 'TiDB': 1}

### MongoDB

- Comparison answers: 6
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 5
- Conditional / use-case split answers: 4
- No clear winner answers: 1
- Valid comparison answers (detected winners only): 1
- Target win rate: 100.00% (n = 1) — low sample
- Winner counts: {'MongoDB': 1}

### MySQL

- Comparison answers: 30
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 22
- Conditional / use-case split answers: 10
- No clear winner answers: 12
- Valid comparison answers (detected winners only): 8
- Target win rate: 12.50% (n = 8) — low sample
- Winner counts: {'TiDB': 5, 'PostgreSQL': 1, 'PlanetScale': 1, 'MySQL': 1}

### Neon

- Comparison answers: 15
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 14
- Conditional / use-case split answers: 9
- No clear winner answers: 5
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
- Eligible answers without a detected winner: 4
- Conditional / use-case split answers: 4
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 2
- Target win rate: 0.00% (n = 2) — low sample
- Winner counts: {'TiDB': 2}

### PlanetScale

- Comparison answers: 9
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 5
- Conditional / use-case split answers: 2
- No clear winner answers: 3
- Valid comparison answers (detected winners only): 4
- Target win rate: 25.00% (n = 4) — low sample
- Winner counts: {'TiDB': 3, 'PlanetScale': 1}

### PostgreSQL

- Comparison answers: 6
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 5
- Conditional / use-case split answers: 4
- No clear winner answers: 1
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
- Conditional / use-case split answers: 1
- No clear winner answers: 1
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
- Target win rate: 100.00% (n = 4) — low sample
- Winner counts: {'SingleStore': 4}

### Snowflake

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 2
- Conditional / use-case split answers: 2
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### Spanner

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 2
- Conditional / use-case split answers: 2
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 100.00% (n = 1) — low sample
- Winner counts: {'Spanner': 1}

### Supabase

- Comparison answers: 9
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 8
- Conditional / use-case split answers: 4
- No clear winner answers: 4
- Valid comparison answers (detected winners only): 1
- Target win rate: 100.00% (n = 1) — low sample
- Winner counts: {'Supabase': 1}

### TiDB

- Comparison answers: 153
- Excluded pending prompt review: 3
- Eligible answers without a detected winner: 100
- Conditional / use-case split answers: 66
- No clear winner answers: 34
- Valid comparison answers (detected winners only): 50
- Target win rate: 56.00% (n = 50)
- Winner counts: {'TiDB': 28, 'Elasticsearch': 2, 'MongoDB': 1, 'Spanner': 1, 'PostgreSQL': 2, 'SingleStore': 4, 'Milvus': 4, 'Chroma': 2, 'PlanetScale': 1, 'OpenSearch': 1, 'MySQL': 1, 'Weaviate': 1, 'Supabase': 1, 'Neon': 1}

### Vitess

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 2
- Conditional / use-case split answers: 1
- No clear winner answers: 1
- Valid comparison answers (detected winners only): 1
- Target win rate: 0.00% (n = 1) — low sample
- Winner counts: {'TiDB': 1}

### Weaviate

- Comparison answers: 6
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 5
- Conditional / use-case split answers: 5
- No clear winner answers: 0
- Valid comparison answers (detected winners only): 1
- Target win rate: 100.00% (n = 1) — low sample
- Winner counts: {'Weaviate': 1}

### YugabyteDB

- Comparison answers: 3
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 3
- Conditional / use-case split answers: 1
- No clear winner answers: 2
- Valid comparison answers (detected winners only): 0
- Target win rate: N/A
- Winner counts: {}

### pgvector

- Comparison answers: 6
- Excluded pending prompt review: 0
- Eligible answers without a detected winner: 6
- Conditional / use-case split answers: 4
- No clear winner answers: 2
- Valid comparison answers (detected winners only): 0
- Target win rate: N/A
- Winner counts: {}

## Cost

- Saved-answer usage estimate: $28.0617
- Scope: Usage estimate for successful saved answers in this report's search mode. Not a billing ledger; excludes failed or overwritten attempts and may include answers collected previously.
- Pricing version: 2026-09-03
- Fact judge mode: off
- Fact judge estimated cost: $0.0
- Combined provider and judge cost: $28.0617
- Judge cost covers this scoring invocation. Cache hits add no new judge calls; previous judge charges are not included. The combined figure is not lifetime project spend.

- anthropic saved token cost: $13.3715; saved web search cost: $4.5.
- gemini saved token cost: $0.2662; saved web search cost: $5.082.
- openai saved token cost: $1.352; saved web search cost: $3.49.

## Run Metadata

- Prompt set hash (effective metadata): `9d571b44ea7db287bb6405b3213401a32904b62cfa375a9551554017eab85e00`
- Frozen source prompt hash: `9d571b44ea7db287bb6405b3213401a32904b62cfa375a9551554017eab85e00`
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
| pingcap.com | PingCAP | 194 | 410 | 178 | TiDB (22), PostgreSQL (3), Vitess (2), Aurora (1), Neon (1), Pinecone (1), PlanetScale (1), Redis (1), SingleStore (1), Spanner (1), pgvector (1) |
| docs.pingcap.com | PingCAP | 135 | 290 | 135 | TiDB (17), PostgreSQL (4), MySQL (2), Chroma (1), Milvus (1), Neon (1), Pinecone (1) |
| arxiv.org | Other | 99 | 106 | 56 | TiDB (3), PostgreSQL (1), Redis (1), Weaviate (1), pgvector (1) |
| medium.com | Other | 91 | 111 | 65 | TiDB (7), Neon (3), MongoDB (1), PostgreSQL (1), pgvector (1) |
| dev.to | Other | 81 | 99 | 48 | TiDB (4), Neon (1), Qdrant (1), Redis (1), pgvector (1) |
| en.wikipedia.org | Other | 71 | 75 | 56 | TiDB (4), Pinecone (1), PostgreSQL (1), Vitess (1) |
| youtube.com | Other | 49 | 50 | 33 | Neon (2), Qdrant (1) |
| github.com/pingcap | PingCAP | 44 | 66 | 44 | TiDB (4) |
| redis.io | Competitor | 42 | 59 | 8 | PostgreSQL (1), Redis (1), pgvector (1) |
| pingcap.co.jp | PingCAP | 37 | 39 | 37 | TiDB (4) |

Recommendations are observed in answers that cite the domain; this is an association, not proof of causation.
