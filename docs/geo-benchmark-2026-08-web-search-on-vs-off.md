# GEO Benchmark 2026-08 Web Search On vs Off

Run date: 2026-08-10
Prompt set: `geo-benchmark/prompts/2026-08/prompts.json`
Prompt count: 120
Runs per prompt: 1
Targets: TiDB, CockroachDB, YugabyteDB, Supabase, PlanetScale, Neon

## Scope

This is a side-by-side experiment to compare provider web search mode against the existing web-search-off baseline.

Data sources:

- OpenAI off: `geo-benchmark-openai`
- Anthropic off: `geo-benchmark`
- OpenAI and Anthropic on: `geo-benchmark-websearch-on`

Important run notes:

- OpenAI web-search-on was rerun with `gpt-5-mini-2025-08-07`, `--web-search on`, and `--no-fallback`.
- OpenAI web-search-on completed 120/120 prompts with 0 errors and 117 actual web search calls.
- The OpenAI off baseline remains the original completed run: 103 rows used `gpt-5-mini-2025-08-07` and 17 recovered rows used `gpt-4o-mini-2024-07-18` fallback.
- Anthropic used `claude-sonnet-5` in both off and on modes.

## Cost Comparison

| Provider | Off Cost | On Cost | Delta | Multiple | Off Requests | On Requests | Web Search Calls |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenAI | $0.2703 | $2.0109 | +$1.7406 | 7.44x | 120 | 120 | 117 |
| Anthropic | $0.8728 | $5.6844 | +$4.8116 | 6.51x | 120 | 120 | 120 |
| Combined | $1.1431 | $7.6953 | +$6.5522 | 6.73x | 240 | 240 | 237 |

OpenAI cost increased mostly from web search fees and retrieved context tokens. Anthropic cost increased from both web search fees and much higher input-token usage because retrieved web context is counted in the Messages API usage.

## Overall Scoring Comparison

### OpenAI

| Target | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 42.68 | 37.58 | -5.10 | 33.94 | 25.36 | -8.58 | 38.33 | 28.33 | -10.00 |
| Neon | 4.25 | 11.96 | +7.71 | 2.94 | 1.17 | -1.77 | 2.50 | 8.33 | +5.83 |
| PlanetScale | 2.94 | 5.95 | +3.01 | 2.76 | 3.44 | +0.68 | 2.50 | 5.00 | +2.50 |
| Supabase | 8.82 | 12.35 | +3.53 | 4.61 | 7.06 | +2.45 | 6.67 | 10.00 | +3.33 |
| TiDB | 18.89 | 15.62 | -3.27 | 8.05 | 7.28 | -0.77 | 16.67 | 15.00 | -1.67 |
| YugabyteDB | 27.71 | 28.76 | +1.05 | 29.24 | 25.70 | -3.54 | 16.67 | 18.33 | +1.66 |

### Anthropic

| Target | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 24.84 | 31.50 | +6.66 | 15.46 | 5.66 | -9.80 | 21.67 | 35.00 | +13.33 |
| Neon | 14.44 | 13.79 | -0.65 | 10.53 | 1.04 | -9.49 | 8.33 | 11.67 | +3.34 |
| PlanetScale | 3.99 | 1.24 | -2.75 | 3.12 | 0.14 | -2.98 | 3.33 | 0.83 | -2.50 |
| Supabase | 19.28 | 14.71 | -4.57 | 14.65 | 1.48 | -13.17 | 15.00 | 12.50 | -2.50 |
| TiDB | 21.31 | 31.63 | +10.32 | 8.24 | 17.28 | +9.04 | 11.67 | 25.83 | +14.16 |
| YugabyteDB | 14.97 | 18.10 | +3.13 | 12.26 | 9.42 | -2.84 | 8.33 | 14.17 | +5.84 |

## Unchanged-Prompt Scoring Comparison

### OpenAI

| Target | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 40.47 | 38.97 | -1.50 | 34.09 | 25.48 | -8.61 | 34.52 | 32.14 | -2.38 |
| Neon | 5.23 | 14.02 | +8.79 | 3.57 | 1.32 | -2.25 | 3.57 | 9.52 | +5.95 |
| PlanetScale | 3.93 | 6.17 | +2.24 | 3.45 | 3.62 | +0.17 | 2.38 | 4.76 | +2.38 |
| Supabase | 8.41 | 13.46 | +5.05 | 4.70 | 7.82 | +3.12 | 5.95 | 10.71 | +4.76 |
| TiDB | 20.84 | 17.66 | -3.18 | 8.58 | 7.74 | -0.84 | 17.86 | 17.86 | +0.00 |
| YugabyteDB | 26.54 | 27.38 | +0.84 | 29.59 | 25.54 | -4.05 | 16.67 | 20.24 | +3.57 |

### Anthropic

| Target | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 23.74 | 34.21 | +10.47 | 13.06 | 6.06 | -7.00 | 20.24 | 38.10 | +17.86 |
| Neon | 13.93 | 14.39 | +0.46 | 9.25 | 1.32 | -7.93 | 7.14 | 10.71 | +3.57 |
| PlanetScale | 3.46 | 1.78 | -1.68 | 1.51 | 0.14 | -1.37 | 3.57 | 1.19 | -2.38 |
| Supabase | 17.66 | 12.90 | -4.76 | 14.26 | 1.81 | -12.45 | 13.10 | 9.52 | -3.58 |
| TiDB | 20.93 | 34.49 | +13.56 | 8.43 | 18.42 | +9.99 | 11.90 | 28.57 | +16.67 |
| YugabyteDB | 14.39 | 18.79 | +4.40 | 11.27 | 9.68 | -1.59 | 8.33 | 13.10 | +4.77 |

## TiDB Deep Dive By Prompt Type

### OpenAI

| Prompt Type | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ai_infra | 0.00 | 3.33 | +3.33 | 0.00 | 1.80 | +1.80 | 0.00 | 3.33 | +3.33 |
| case_selection | 20.83 | 25.83 | +5.00 | 5.72 | 15.64 | +9.92 | 20.83 | 25.00 | +4.17 |
| database_type | 24.67 | 16.00 | -8.67 | 12.53 | 8.27 | -4.26 | 16.67 | 16.67 | +0.00 |
| pain_point | 30.56 | 21.11 | -9.45 | 13.32 | 7.59 | -5.73 | 27.78 | 16.67 | -11.11 |

### Anthropic

| Prompt Type | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ai_infra | 5.33 | 15.33 | +10.00 | 1.50 | 11.59 | +10.09 | 6.67 | 10.00 | +3.33 |
| case_selection | 16.67 | 26.67 | +10.00 | 4.48 | 19.57 | +15.09 | 8.33 | 16.67 | +8.34 |
| database_type | 25.33 | 34.00 | +8.67 | 9.65 | 17.68 | +8.03 | 20.00 | 33.33 | +13.33 |
| pain_point | 34.44 | 46.11 | +11.67 | 14.74 | 20.80 | +6.06 | 11.11 | 38.89 | +27.78 |

## Readout

OpenAI web-search-on is now a valid same-model comparison for the on side. It does not materially improve TiDB in this run: TiDB overall Answer Share drops by 3.27 points, Citation Authority drops by 0.77 points, and Recommendation Rate drops by 1.67 points. On unchanged prompts, TiDB Recommendation Rate is flat at 17.86, while Answer Share and Citation Authority both move down slightly.

The OpenAI movement is not uniformly negative across the market. Web search raises Neon, Supabase, and PlanetScale visibility, especially in unchanged prompts. This is directionally plausible because web search pulls in more current serverless and app-platform material, where those vendors have stronger public-market narratives.

Anthropic web search remains the stronger positive TiDB signal in this experiment. TiDB gains +10.32 Answer Share, +9.04 Citation Authority, and +14.16 Recommendation Rate overall. The largest TiDB movement is in pain-point prompts, where Recommendation Rate rises from 11.11 to 38.89.

## Recommendation

Keep web search as a separate benchmark mode rather than replacing the default monthly KPI. Use web-search-off for continuity with the existing baseline, and run web-search-on as a citation-grounded diagnostic view. For OpenAI specifically, track the same-model web-on series from this corrected `gpt-5-mini` run onward; do not compare future OpenAI web-on runs against the earlier invalid `gpt-4o-mini` web-on output.
