# GEO Benchmark LLM Report - 2026-08

Providers: anthropic, openai
Web search mode: on
Raw answers: 240
Scored target-answer rows: 1440

## Executive KPI

| Target | Answer Share | Citation Authority | Recommendation Rate | Stable Answer Share | Stable Recommendation Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 34.54 | 15.51 | 31.67 | 36.59 | 35.12 |
| TiDB | 23.63 | 12.28 | 20.42 | 26.07 | 23.21 |
| YugabyteDB | 23.43 | 17.56 | 16.25 | 23.08 | 16.67 |
| Neon | 12.88 | 1.11 | 10.00 | 14.21 | 10.12 |
| Supabase | 13.53 | 4.27 | 11.25 | 13.18 | 10.12 |
| PlanetScale | 3.59 | 1.79 | 2.92 | 3.97 | 2.98 |

Overall columns use all prompts for the month. Stable columns use only stable prompts and are the strict comparable view.

## Prompt-Type Breakdown

### Answer Share

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pain_point` | 46.94 | 33.61 | 30.00 | 3.06 | 1.39 | 2.50 |
| `database_type` | 54.67 | 25.00 | 41.00 | 4.67 | 2.00 | 6.33 |
| `ai_infra` | 8.67 | 9.33 | 3.67 | 36.33 | 42.33 | 5.00 |
| `case_selection` | 30.00 | 26.25 | 23.75 | 1.25 | 1.25 | 0.00 |

### Citation Authority

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pain_point` | 18.19 | 14.19 | 22.01 | 0.28 | 0.00 | 0.07 |
| `database_type` | 28.11 | 12.97 | 31.17 | 0.49 | 0.12 | 2.04 |
| `ai_infra` | 2.50 | 6.69 | 1.33 | 3.10 | 14.44 | 4.65 |
| `case_selection` | 18.13 | 17.60 | 20.96 | 0.00 | 0.00 | 0.00 |

### Recommendation Rate

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pain_point` | 38.89 | 27.78 | 16.67 | 2.78 | 1.39 | 1.39 |
| `database_type` | 51.67 | 25.00 | 30.00 | 1.67 | 1.67 | 6.67 |
| `ai_infra` | 6.67 | 6.67 | 3.33 | 33.33 | 40.00 | 3.33 |
| `case_selection` | 27.08 | 20.83 | 14.58 | 2.08 | 2.08 | 0.00 |

## Coverage

- Overall prompts per target: 120
- Overall target-answer rows per target: 240
- Unchanged prompts per target: 84
- Unchanged target-answer rows per target: 168

## Quality Signals

- Average source authority shown below is target-specific in `target-kpi-summary.csv`.

## Cost

- Estimated cost: $7.6953
- Pricing version: 2026-07-30
