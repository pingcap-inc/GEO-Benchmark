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
Valid comparisons: `anthropic`, `openai`, `all`, `none`.

Guardrail: do not manually blend providers for executive readouts.

## Input Audit

| View | Target-Answer Rows | Prompt Count | Model Distribution | Web Search Calls | Note |
| --- | ---: | ---: | --- | ---: | --- |
| `anthropic-on` | 720 | 120 | claude-sonnet-5: 120 answers | 120 | same model |
| `openai-on` | 720 | 120 | gpt-5-mini-2025-08-07: 120 answers | 117 | corrected same-model web-on |
| `anthropic-off` | 720 | 120 | claude-sonnet-5: 120 answers | 0 | same model |
| `openai-off` | 720 | 120 | gpt-4o-mini-2024-07-18: 17 answers, gpt-5-mini-2025-08-07: 103 answers | 0 | mixed fallback baseline; not strict same-model |

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

## Provider On/Off Comparisons

### Anthropic Web-On vs Web-Off

#### Overall

| Target | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 24.84 | 31.50 | +6.66 | 15.46 | 5.66 | -9.80 | 21.67 | 35.00 | +13.33 |
| TiDB | 21.31 | 31.63 | +10.32 | 8.24 | 17.28 | +9.04 | 11.67 | 25.83 | +14.16 |
| YugabyteDB | 14.97 | 18.10 | +3.13 | 12.26 | 9.42 | -2.84 | 8.33 | 14.17 | +5.84 |
| Neon | 14.44 | 13.79 | -0.65 | 10.53 | 1.04 | -9.49 | 8.33 | 11.67 | +3.34 |
| Supabase | 19.28 | 14.71 | -4.57 | 14.65 | 1.48 | -13.17 | 15.00 | 12.50 | -2.50 |
| PlanetScale | 3.99 | 1.24 | -2.75 | 3.12 | 0.14 | -2.98 | 3.33 | 0.83 | -2.50 |

#### Stable Prompts

| Target | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 23.74 | 34.21 | +10.47 | 13.06 | 6.06 | -7.00 | 20.24 | 38.10 | +17.86 |
| TiDB | 20.93 | 34.49 | +13.56 | 8.43 | 18.42 | +9.99 | 11.90 | 28.57 | +16.67 |
| YugabyteDB | 14.39 | 18.79 | +4.40 | 11.27 | 9.68 | -1.59 | 8.33 | 13.10 | +4.77 |
| Neon | 13.93 | 14.39 | +0.46 | 9.25 | 1.32 | -7.93 | 7.14 | 10.71 | +3.57 |
| Supabase | 17.66 | 12.90 | -4.76 | 14.26 | 1.81 | -12.45 | 13.10 | 9.52 | -3.58 |
| PlanetScale | 3.46 | 1.78 | -1.68 | 1.51 | 0.14 | -1.37 | 3.57 | 1.19 | -2.38 |

#### TiDB By Prompt Type

| Prompt Type | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ai_infra | 5.33 | 15.33 | +10.00 | 1.50 | 11.59 | +10.09 | 6.67 | 10.00 | +3.33 |
| case_selection | 16.67 | 26.67 | +10.00 | 4.48 | 19.57 | +15.09 | 8.33 | 16.67 | +8.34 |
| database_type | 25.33 | 34.00 | +8.67 | 9.65 | 17.68 | +8.03 | 20.00 | 33.33 | +13.33 |
| pain_point | 34.44 | 46.11 | +11.67 | 14.74 | 20.80 | +6.06 | 11.11 | 38.89 | +27.78 |

### OpenAI Web-On vs Web-Off (Off Baseline Uses Fallback)

Note: OpenAI web-on is all `gpt-5-mini-2025-08-07`, but OpenAI web-off contains 103 `gpt-5-mini-2025-08-07` answers and 17 `gpt-4o-mini-2024-07-18` fallback answers. Treat this as the current published baseline comparison, not a strict same-model comparison.

#### Overall

| Target | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 42.68 | 37.58 | -5.10 | 33.94 | 25.36 | -8.58 | 38.33 | 28.33 | -10.00 |
| TiDB | 18.89 | 15.62 | -3.27 | 8.05 | 7.28 | -0.77 | 16.67 | 15.00 | -1.67 |
| YugabyteDB | 27.71 | 28.76 | +1.05 | 29.24 | 25.70 | -3.54 | 16.67 | 18.33 | +1.66 |
| Neon | 4.25 | 11.96 | +7.71 | 2.94 | 1.17 | -1.77 | 2.50 | 8.33 | +5.83 |
| Supabase | 8.82 | 12.35 | +3.53 | 4.61 | 7.06 | +2.45 | 6.67 | 10.00 | +3.33 |
| PlanetScale | 2.94 | 5.95 | +3.01 | 2.76 | 3.44 | +0.68 | 2.50 | 5.00 | +2.50 |

#### Stable Prompts

| Target | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 40.47 | 38.97 | -1.50 | 34.09 | 25.48 | -8.61 | 34.52 | 32.14 | -2.38 |
| TiDB | 20.84 | 17.66 | -3.18 | 8.58 | 7.74 | -0.84 | 17.86 | 17.86 | +0.00 |
| YugabyteDB | 26.54 | 27.38 | +0.84 | 29.59 | 25.54 | -4.05 | 16.67 | 20.24 | +3.57 |
| Neon | 5.23 | 14.02 | +8.79 | 3.57 | 1.32 | -2.25 | 3.57 | 9.52 | +5.95 |
| Supabase | 8.41 | 13.46 | +5.05 | 4.70 | 7.82 | +3.12 | 5.95 | 10.71 | +4.76 |
| PlanetScale | 3.93 | 6.17 | +2.24 | 3.45 | 3.62 | +0.17 | 2.38 | 4.76 | +2.38 |

#### TiDB By Prompt Type

| Prompt Type | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ai_infra | 0.00 | 3.33 | +3.33 | 0.00 | 1.80 | +1.80 | 0.00 | 3.33 | +3.33 |
| case_selection | 20.83 | 25.83 | +5.00 | 5.72 | 15.64 | +9.92 | 20.83 | 25.00 | +4.17 |
| database_type | 24.67 | 16.00 | -8.67 | 12.53 | 8.27 | -4.26 | 16.67 | 16.67 | +0.00 |
| pain_point | 30.56 | 21.11 | -9.45 | 13.32 | 7.59 | -5.73 | 27.78 | 16.67 | -11.11 |

## Suggested Next Steps For TiDB AEO

1. Strengthen OpenAI-facing discoverability for pain-point and database-type queries.
OpenAI web-on lowers TiDB Answer Share in `pain_point` and `database_type` prompts, while Anthropic web-on improves TiDB strongly. Build concise public pages that map buyer pains to TiDB-fit language: scale-out SQL, MySQL compatibility, HTAP, operational analytics, AI application data, and vector search with transactional data.

2. Create citation-ready comparison and use-case pages.
TiDB Citation Authority is much stronger in Anthropic web-on (17.28) than OpenAI web-on (7.28). Publish pages with clear claims, current dates, source links, schema examples, and comparison tables for TiDB vs CockroachDB, YugabyteDB, Aurora, Neon, Supabase, and PlanetScale.

3. Improve recommendation language around exact-fit scenarios.
Anthropic Recommendation Rate moves from 11.67 to 25.83, but OpenAI moves from 16.67 to 15.00. Add explicit 'choose TiDB when...' sections for real-time operational analytics, high-write transactional workloads, MySQL scale-out, and hybrid transactional plus analytical workloads.

4. Add serverless AI positioning without forcing PostgreSQL framing.
For AI infrastructure prompts, TiDB still trails Neon and Supabase in OpenAI. Create TiDB Serverless AI pages and examples around agent state, RAG over fresh operational data, vector search with SQL filters, and transactional metadata at scale.

5. Make customer proof easier for answer engines to quote.
Package customer stories into structured, crawlable pages with industry, workload, before/after pain, architecture, measurable outcome, and links to docs. The benchmark case-selection prompts reward concrete use-case proof more than generic product messaging.
