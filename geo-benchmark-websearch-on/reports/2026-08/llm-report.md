# GEO Benchmark LLM Report - 2026-08

Providers: anthropic, openai
Web search mode: on
Raw answers: 240
Scored target-answer rows: 1440

## Executive KPI

| Target | Answer Share | Citation Authority | Recommendation Rate | Stable Answer Share | Stable Recommendation Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 31.99 | 14.31 | 24.17 | 32.76 | 25.60 |
| TiDB | 16.41 | 8.99 | 13.33 | 17.38 | 14.29 |
| YugabyteDB | 11.96 | 6.75 | 8.75 | 12.34 | 8.33 |
| Neon | 6.90 | 0.52 | 5.83 | 7.20 | 5.36 |
| Supabase | 9.61 | 1.91 | 7.08 | 8.97 | 5.95 |
| PlanetScale | 0.98 | 0.42 | 0.42 | 1.40 | 0.60 |

Overall columns use all prompts for the month. Stable columns use only stable prompts and are the strict comparable view.

## Prompt-Type Breakdown

### Answer Share

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pain_point` | 42.78 | 24.72 | 13.61 | 3.06 | 1.39 | 0.83 |
| `database_type` | 54.67 | 17.00 | 26.67 | 3.67 | 2.00 | 2.00 |
| `ai_infra` | 5.00 | 7.67 | 1.00 | 16.67 | 29.00 | 1.00 |
| `case_selection` | 30.00 | 13.33 | 10.42 | 1.25 | 1.25 | 0.00 |

### Citation Authority

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pain_point` | 18.11 | 11.40 | 6.90 | 0.28 | 0.00 | 0.07 |
| `database_type` | 23.53 | 8.84 | 18.21 | 0.30 | 0.12 | 0.24 |
| `ai_infra` | 2.90 | 5.79 | 0.00 | 1.23 | 6.41 | 1.20 |
| `case_selection` | 15.62 | 9.79 | 4.78 | 0.00 | 0.00 | 0.00 |

### Recommendation Rate

| Type | CockroachDB | TiDB | YugabyteDB | Neon | Supabase | PlanetScale |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pain_point` | 26.39 | 20.83 | 8.33 | 2.78 | 1.39 | 0.00 |
| `database_type` | 48.33 | 16.67 | 20.00 | 1.67 | 1.67 | 1.67 |
| `ai_infra` | 1.67 | 5.00 | 0.00 | 16.67 | 23.33 | 0.00 |
| `case_selection` | 18.75 | 8.33 | 6.25 | 2.08 | 2.08 | 0.00 |

## Coverage

- Overall prompts per target: 120
- Overall target-answer rows per target: 240
- Unchanged prompts per target: 84
- Unchanged target-answer rows per target: 168

## Quality Signals

- Average source authority shown below is target-specific in `target-kpi-summary.csv`.

## Cost

- Estimated cost: $6.9172
- Pricing version: 2026-07-30
