# GEO Benchmark LLM Report - 2026-08 - OpenAI

Status: real provider run, OpenAI only  
Primary model: `gpt-5-mini-2025-08-07`  
Fallback model for failed prompts: `gpt-4o-mini-2024-07-18`  
Latest refresh command: `./geo-bench --data-dir geo-benchmark-openai run --month 2026-08 --providers openai --runs 1 --assumed-output-tokens 1600 --force --only-prompt-ids stable_ai_infra_005,stable_ai_infra_006,stable_ai_infra_007,stable_ai_infra_008,stable_ai_infra_017,stable_ai_infra_018,stable_ai_infra_019,stable_ai_infra_020,dyn_202608_ai_infra_008,dyn_202608_ai_infra_009`  
Targets: TiDB, CockroachDB, YugabyteDB, Supabase, PlanetScale, Neon

## Read This First

This is a real OpenAI benchmark result. It is not mixed with Claude or any mock provider.

The latest refresh reran only the rewritten `serverless_ai` prompt instances. These are the 10 generated prompt IDs that correspond to the 4 rewritten serverless AI question templates. The other 110 OpenAI raw answers were preserved.

Coverage:

```text
Prompt requests in final scoring set: 120
Serverless AI prompt instances refreshed: 10
Other prompt answers preserved: 110
Final successful answers: 120
Final error answers: 0
Scored target-answer rows: 720
Actual/usage-estimated cost: $0.2703
Planned cost estimate: $0.3879
```

Model split:

| Model | Requests | Input Tokens | Output Tokens | Estimated Cost |
| --- | ---: | ---: | ---: | ---: |
| `gpt-5-mini-2025-08-07` | 103 | 13,051 | 131,668 | $0.2666 |
| `gpt-4o-mini-2024-07-18` | 17 | 2,196 | 5,580 | $0.0037 |

## Executive KPI

| Target | Answer Share | Citation Authority | Recommendation Rate | Stable Answer Share | Stable Recommendation Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 42.68 | 33.94 | 38.33 | 40.47 | 34.52 |
| TiDB | 18.89 | 8.05 | 16.67 | 20.84 | 17.86 |
| YugabyteDB | 27.71 | 29.24 | 16.67 | 26.54 | 16.67 |
| Neon | 4.25 | 2.94 | 2.50 | 5.23 | 3.57 |
| Supabase | 8.82 | 4.61 | 6.67 | 8.41 | 5.95 |
| PlanetScale | 2.94 | 2.76 | 2.50 | 3.93 | 2.38 |

Overall columns use all prompts for the month. Stable columns use only stable prompts and are the strict month-over-month comparable view.

## Gap To Leader

| Target | Answer Share Gap | Citation Authority Gap | Recommendation Rate Gap |
| --- | ---: | ---: | ---: |
| CockroachDB | +0.00 | +0.00 | +0.00 |
| TiDB | -23.79 | -25.89 | -21.66 |
| YugabyteDB | -14.97 | -4.70 | -21.66 |
| Neon | -38.43 | -31.00 | -35.83 |
| Supabase | -33.86 | -29.33 | -31.66 |
| PlanetScale | -39.74 | -31.18 | -35.83 |

## Prompt-Type Breakdown

### Answer Share

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pain_point` | 48.33 | 30.56 | 32.78 | 0.00 | 0.00 | 1.11 |
| `database_type` | 70.00 | 24.67 | 42.00 | 0.67 | 0.00 | 4.00 |
| `ai_infra` | 17.33 | 0.00 | 6.00 | 14.00 | 30.00 | 6.00 |
| `case_selection` | 43.33 | 20.83 | 39.17 | 0.00 | 0.00 | 0.00 |

### Citation Authority

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pain_point` | 43.14 | 13.32 | 35.56 | 0.00 | 0.00 | 2.00 |
| `database_type` | 53.51 | 12.53 | 51.10 | 2.40 | 0.00 | 2.40 |
| `ai_infra` | 8.47 | 0.00 | 7.47 | 8.40 | 15.67 | 5.40 |
| `case_selection` | 36.56 | 5.72 | 28.50 | 0.00 | 0.00 | 0.00 |

### Recommendation Rate

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pain_point` | 38.89 | 27.78 | 16.67 | 0.00 | 0.00 | 5.56 |
| `database_type` | 56.67 | 16.67 | 16.67 | 0.00 | 0.00 | 3.33 |
| `ai_infra` | 16.67 | 0.00 | 6.67 | 10.00 | 26.67 | 0.00 |
| `case_selection` | 41.67 | 20.83 | 29.17 | 0.00 | 0.00 | 0.00 |

## AI-Infra Subtype Deep Dive

### Answer Share

| Use Case | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai_app_backend` | 0.00 | 0.00 | 0.00 | 10.00 | 75.00 | 0.00 |
| `serverless_ai` | 10.00 | 0.00 | 0.00 | 30.00 | 0.00 | 18.00 |
| `operational_ai_data` | 52.50 | 0.00 | 22.50 | 0.00 | 0.00 | 0.00 |

### Citation Authority

| Use Case | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai_app_backend` | 0.00 | 0.00 | 0.00 | 7.50 | 39.18 | 0.00 |
| `serverless_ai` | 1.50 | 0.00 | 0.00 | 16.20 | 0.00 | 16.20 |
| `operational_ai_data` | 29.88 | 0.00 | 28.00 | 0.00 | 0.00 | 0.00 |

### Recommendation Rate

| Use Case | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai_app_backend` | 0.00 | 0.00 | 0.00 | 0.00 | 66.67 | 0.00 |
| `serverless_ai` | 10.00 | 0.00 | 0.00 | 30.00 | 0.00 | 0.00 |
| `operational_ai_data` | 50.00 | 0.00 | 25.00 | 0.00 | 0.00 | 0.00 |

## Interpretation

OpenAI still strongly maps generic distributed SQL, SaaS multi-tenancy, relational write scaling, manual sharding replacement, and globally distributed OLTP prompts to CockroachDB.

The rewritten `serverless_ai` prompts no longer include explicit Postgres or pgvector wording. After that cleanup, OpenAI still most often associates serverless AI app data-layer questions with Neon, with some PlanetScale and CockroachDB visibility. Supabase no longer appears in this slice, which suggests the previous serverless result was meaningfully influenced by the old wording.

TiDB's OpenAI gap remains recall in high-value generic categories. It is visible in pain-point and case-selection prompts, but it is absent from the refreshed AI-infra slice, including `operational_ai_data`.

## Recommended Actions To Improve TiDB Scores

1. Build a canonical "TiDB for operational AI data" content cluster: RAG over fresh operational data, agent memory plus durable relational state, tool-call traces plus business records, and transactions plus analytics.
2. Create concrete architecture pages with schemas, diagrams, and code examples for TiDB vector search with SQL filters, HTAP feedback loops, and operational data retrieval.
3. Publish neutral comparison pages for TiDB versus CockroachDB, YugabyteDB, Aurora, Spanner, Supabase, Neon, and common AI app data-layer patterns.
4. Strengthen citation authority with concise fact hubs for distributed SQL, MySQL compatibility, horizontal scale-out, TiFlash/HTAP, TiDB Cloud Serverless, and vector search.
5. Add more US/EU/APAC customer stories that start from the buyer pain: sharding replacement, high-write relational workloads, real-time analytics, and AI applications over transactional data.
6. For serverless AI queries, do not try to make TiDB look like Neon or Supabase. Instead, create "when AI apps outgrow lightweight serverless data layers" pages that position TiDB as the next architecture choice.

## Artifact Links

- Machine report: `geo-benchmark-openai/reports/2026-08/llm-report.md`
- Scored rows: `geo-benchmark-openai/reports/2026-08/scored_answers.csv`
- Raw answers: `geo-benchmark-openai/runs/2026-08/raw_answers.jsonl`
