# GEO Benchmark LLM Report - 2026-08

Providers: anthropic
Raw answers: 120
Scored target-answer rows: 720

## Executive KPI

| Target | Answer Share | Citation Authority | Recommendation Rate | Stable Answer Share | Stable Recommendation Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 24.84 | 15.46 | 21.67 | 23.74 | 20.24 |
| TiDB | 21.31 | 8.24 | 11.67 | 20.93 | 11.90 |
| YugabyteDB | 14.97 | 12.26 | 8.33 | 14.39 | 8.33 |
| Neon | 14.44 | 10.53 | 8.33 | 13.93 | 7.14 |
| Supabase | 19.28 | 14.65 | 15.00 | 17.66 | 13.10 |
| PlanetScale | 3.99 | 3.12 | 3.33 | 3.46 | 3.57 |

Overall columns use all prompts for the month. Stable columns use only stable prompts and are the strict comparable view.

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

## Coverage

- Overall prompts per target: 120
- Overall target-answer rows per target: 120
- Unchanged prompts per target: 84
- Unchanged target-answer rows per target: 84

## Quality Signals

- Average source authority shown below is target-specific in `target-kpi-summary.csv`.

## Cost

- Estimated cost: $0.8728
- Pricing version: 2026-07-30
