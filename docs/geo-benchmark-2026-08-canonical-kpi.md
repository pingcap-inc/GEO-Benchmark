# GEO Benchmark 2026-08 Canonical KPI

Generated from committed scored outputs only. No raw answers are read and no provider APIs are called.

Regenerate all four canonical views:

```bash
python3 scripts/generate-canonical-kpi-report.py --month 2026-08
```

Generate one view:

```bash
python3 scripts/generate-canonical-kpi-report.py --month 2026-08 --view anthropic-on
```

Valid views: `anthropic-on`, `openai-on`, `anthropic-off`, `openai-off`.

Guardrail: do not manually blend providers for executive readouts.

## Anthropic Web-On

View: `anthropic-on`
Provider: `anthropic`
Web search mode: `on`
Target-answer rows: `720`

| Target | Answer Share | Citation Authority | Recommendation Rate | Stable Answer Share | Stable Recommendation Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 31.50 | 5.66 | 35.00 | 34.21 | 38.10 |
| TiDB | 31.63 | 17.28 | 25.83 | 34.49 | 28.57 |
| YugabyteDB | 18.10 | 9.42 | 14.17 | 18.79 | 13.10 |
| Neon | 13.79 | 1.04 | 11.67 | 14.39 | 10.71 |
| Supabase | 14.71 | 1.48 | 12.50 | 12.90 | 9.52 |
| PlanetScale | 1.24 | 0.14 | 0.83 | 1.78 | 1.19 |

## OpenAI Web-On

View: `openai-on`
Provider: `openai`
Web search mode: `on`
Target-answer rows: `720`

| Target | Answer Share | Citation Authority | Recommendation Rate | Stable Answer Share | Stable Recommendation Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 37.58 | 25.36 | 28.33 | 38.97 | 32.14 |
| TiDB | 15.62 | 7.28 | 15.00 | 17.66 | 17.86 |
| YugabyteDB | 28.76 | 25.70 | 18.33 | 27.38 | 20.24 |
| Neon | 11.96 | 1.17 | 8.33 | 14.02 | 9.52 |
| Supabase | 12.35 | 7.06 | 10.00 | 13.46 | 10.71 |
| PlanetScale | 5.95 | 3.44 | 5.00 | 6.17 | 4.76 |

## Anthropic Web-Off

View: `anthropic-off`
Provider: `anthropic`
Web search mode: `off`
Target-answer rows: `720`

| Target | Answer Share | Citation Authority | Recommendation Rate | Stable Answer Share | Stable Recommendation Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 24.84 | 15.46 | 21.67 | 23.74 | 20.24 |
| TiDB | 21.31 | 8.24 | 11.67 | 20.93 | 11.90 |
| YugabyteDB | 14.97 | 12.26 | 8.33 | 14.39 | 8.33 |
| Neon | 14.44 | 10.53 | 8.33 | 13.93 | 7.14 |
| Supabase | 19.28 | 14.65 | 15.00 | 17.66 | 13.10 |
| PlanetScale | 3.99 | 3.12 | 3.33 | 3.46 | 3.57 |

## OpenAI Web-Off

View: `openai-off`
Provider: `openai`
Web search mode: `off`
Target-answer rows: `720`

| Target | Answer Share | Citation Authority | Recommendation Rate | Stable Answer Share | Stable Recommendation Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 42.68 | 33.94 | 38.33 | 40.47 | 34.52 |
| TiDB | 18.89 | 8.05 | 16.67 | 20.84 | 17.86 |
| YugabyteDB | 27.71 | 29.24 | 16.67 | 26.54 | 16.67 |
| Neon | 4.25 | 2.94 | 2.50 | 5.23 | 3.57 |
| Supabase | 8.82 | 4.61 | 6.67 | 8.41 | 5.95 |
| PlanetScale | 2.94 | 2.76 | 2.50 | 3.93 | 2.38 |
