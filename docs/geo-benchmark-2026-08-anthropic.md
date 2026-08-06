# GEO Benchmark LLM Report - 2026-08 - Anthropic

Status: real provider run, Anthropic only  
Provider: `anthropic`  
Model: `claude-sonnet-5`  
Latest refresh command: `./geo-bench --data-dir geo-benchmark run --month 2026-08 --providers anthropic --runs 1 --force --only-prompt-type ai_infra`  
Targets: TiDB, CockroachDB, YugabyteDB, Supabase, PlanetScale, Neon

## Read This First

This is a real Claude-only benchmark result. It is not mixed with OpenAI or any mock provider.

The latest refresh reran the full 30-prompt `ai_infra` slice for Anthropic. The other 90 non-AI Anthropic raw answers were preserved.

Coverage:

```text
Prompt requests in final scoring set: 120
AI-infra prompts refreshed: 30
Non-AI prompts preserved: 90
Final successful answers: 120
Final error answers: 0
Scored target-answer rows: 720
Actual/usage-estimated cost: $0.8728
Planned cost estimate: $0.8715
```

## Executive KPI

| Target | Answer Share | Citation Authority | Recommendation Rate | Stable Answer Share | Stable Recommendation Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 24.84 | 15.46 | 21.67 | 23.74 | 20.24 |
| TiDB | 21.31 | 8.24 | 11.67 | 20.93 | 11.90 |
| YugabyteDB | 14.97 | 12.26 | 8.33 | 14.39 | 8.33 |
| Neon | 14.44 | 10.53 | 8.33 | 13.93 | 7.14 |
| Supabase | 19.28 | 14.65 | 15.00 | 17.66 | 13.10 |
| PlanetScale | 3.99 | 3.12 | 3.33 | 3.46 | 3.57 |

Overall columns use all prompts for the month. Stable columns use only stable prompts and are the strict month-over-month comparable view.

## Gap To Leader

| Target | Answer Share Gap | Citation Authority Gap | Recommendation Rate Gap |
| --- | ---: | ---: | ---: |
| CockroachDB | +0.00 | +0.00 | +0.00 |
| TiDB | -3.53 | -7.22 | -10.00 |
| YugabyteDB | -9.87 | -3.20 | -13.34 |
| Neon | -10.40 | -4.93 | -13.34 |
| Supabase | -5.56 | -0.81 | -6.67 |
| PlanetScale | -20.85 | -12.34 | -18.34 |

## Prompt-Type Breakdown

### Answer Share

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pain_point` | 35.00 | 34.44 | 22.78 | 7.78 | 0.56 | 1.67 |
| `database_type` | 50.67 | 25.33 | 28.67 | 6.67 | 5.33 | 6.00 |
| `ai_infra` | 0.67 | 5.33 | 0.00 | 34.00 | 61.33 | 4.00 |
| `case_selection` | 15.00 | 16.67 | 8.33 | 2.50 | 0.00 | 6.67 |

### Citation Authority

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pain_point` | 28.41 | 14.74 | 25.25 | 5.25 | 2.00 | 2.00 |
| `database_type` | 25.02 | 9.65 | 17.10 | 2.40 | 0.00 | 3.90 |
| `ai_infra` | 0.00 | 1.50 | 0.00 | 27.90 | 47.40 | 3.00 |
| `case_selection` | 3.33 | 4.48 | 0.00 | 0.00 | 0.00 | 4.87 |

### Recommendation Rate

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pain_point` | 27.78 | 11.11 | 16.67 | 2.78 | 0.00 | 0.00 |
| `database_type` | 40.00 | 20.00 | 13.33 | 0.00 | 3.33 | 3.33 |
| `ai_infra` | 3.33 | 6.67 | 0.00 | 26.67 | 56.67 | 6.67 |
| `case_selection` | 12.50 | 8.33 | 0.00 | 4.17 | 0.00 | 4.17 |

## AI-Infra Subtype Deep Dive

### Answer Share

| Use Case | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai_app_backend` | 0.00 | 0.00 | 0.00 | 25.00 | 100.00 | 0.00 |
| `serverless_ai` | 0.00 | 10.00 | 0.00 | 66.00 | 52.00 | 12.00 |
| `operational_ai_data` | 2.50 | 7.50 | 0.00 | 7.50 | 15.00 | 0.00 |

### Citation Authority

| Use Case | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai_app_backend` | 0.00 | 0.00 | 0.00 | 24.75 | 66.00 | 0.00 |
| `serverless_ai` | 0.00 | 4.50 | 0.00 | 54.00 | 63.00 | 9.00 |
| `operational_ai_data` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### Recommendation Rate

| Use Case | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai_app_backend` | 0.00 | 0.00 | 0.00 | 8.33 | 91.67 | 0.00 |
| `serverless_ai` | 0.00 | 10.00 | 0.00 | 60.00 | 50.00 | 20.00 |
| `operational_ai_data` | 12.50 | 12.50 | 0.00 | 12.50 | 12.50 | 0.00 |

## Interpretation

Claude is more balanced than OpenAI across the overall target set. CockroachDB still leads overall, but TiDB is closer on Answer Share and Supabase becomes highly visible in the refreshed AI-infra slice.

The rewritten `serverless_ai` prompts no longer include explicit Postgres or pgvector wording. Claude still maps this slice strongly to Neon and Supabase, which is credible for serverless AI app workflows. TiDB now appears in both `serverless_ai` and `operational_ai_data`, but its Citation Authority remains weak.

TiDB's largest Claude gap is still conversion and citation depth. It is visible in pain-point and case-selection prompts, but Claude less often uses TiDB as the final recommendation and less often cites fact-rich TiDB material.

## Recommended Actions To Improve TiDB Scores

1. Build TiDB pages for operational AI data patterns where Claude already shows some TiDB recall: fresh operational retrieval, durable agent state, high-write event memory, and mixed transactional/analytical AI workflows.
2. Improve citation depth with concise fact hubs for TiDB Cloud, vector search, HTAP/TiFlash, MySQL compatibility, horizontal scale-out, and current serverless capabilities.
3. Publish customer stories and architecture notes that use buyer-language headings rather than brand-first headings.
4. Create comparison content for "when AI apps outgrow lightweight serverless data layers" so TiDB competes as the scale-up architecture, not as a direct Supabase/Neon clone.
5. Keep case-selection content concrete: workload shape, migration trigger, why TiDB was chosen, operational result, and current product capability.

## Artifact Links

- Machine report: `geo-benchmark/reports/2026-08/llm-report.md`
- Scored rows: `geo-benchmark/reports/2026-08/scored_answers.csv`
- Raw answers: `geo-benchmark/runs/2026-08/raw_answers.jsonl`
