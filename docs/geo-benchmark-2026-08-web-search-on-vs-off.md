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

Important caveat: OpenAI web-search-on was completed with `gpt-4o-mini-2024-07-18`. A smoke test with the configured `gpt-5-mini` web-search path returned empty content, so the experiment used the validated fallback model to complete the 120-prompt run. Anthropic used `claude-sonnet-5` in both off and on modes.

## Cost Comparison

| Provider | Off Cost | On Cost | Delta | Off Requests | On Requests | Web Search Calls |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenAI | $0.2703 | $1.2328 | +$0.9625 | 120 | 120 | 120 |
| Anthropic | $0.8728 | $5.6844 | +$4.8116 | 120 | 120 | 120 |
| Combined | $1.1431 | $6.9172 | +$5.7741 | 240 | 240 | 240 |

OpenAI cost increased mostly from the web search fee. Anthropic cost increased from both web search fees and much higher input-token usage because retrieved web context is counted in the Messages API usage.

## Overall Scoring Comparison

### OpenAI

| Target | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 42.68 | 32.48 | -10.20 | 33.94 | 22.96 | -10.98 | 38.33 | 13.33 | -25.00 |
| Neon | 4.25 | 0.00 | -4.25 | 2.94 | 0.00 | -2.94 | 2.50 | 0.00 | -2.50 |
| PlanetScale | 2.94 | 0.72 | -2.22 | 2.76 | 0.71 | -2.05 | 2.50 | 0.00 | -2.50 |
| Supabase | 8.82 | 4.51 | -4.31 | 4.61 | 2.34 | -2.27 | 6.67 | 1.67 | -5.00 |
| TiDB | 18.89 | 1.18 | -17.71 | 8.05 | 0.71 | -7.34 | 16.67 | 0.83 | -15.84 |
| YugabyteDB | 27.71 | 5.82 | -21.89 | 29.24 | 4.09 | -25.15 | 16.67 | 3.33 | -13.34 |

### Anthropic

| Target | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CockroachDB | 24.84 | 31.50 | +6.66 | 15.46 | 5.66 | -9.80 | 21.67 | 35.00 | +13.33 |
| Neon | 14.44 | 13.79 | -0.65 | 10.53 | 1.04 | -9.49 | 8.33 | 11.67 | +3.34 |
| PlanetScale | 3.99 | 1.24 | -2.75 | 3.12 | 0.14 | -2.98 | 3.33 | 0.83 | -2.50 |
| Supabase | 19.28 | 14.71 | -4.57 | 14.65 | 1.48 | -13.17 | 15.00 | 12.50 | -2.50 |
| TiDB | 21.31 | 31.63 | +10.32 | 8.24 | 17.28 | +9.04 | 11.67 | 25.83 | +14.16 |
| YugabyteDB | 14.97 | 18.10 | +3.13 | 12.26 | 9.42 | -2.84 | 8.33 | 14.17 | +5.84 |

## TiDB Deep Dive By Prompt Type

### OpenAI

| Prompt Type | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ai_infra | 0.00 | 0.00 | +0.00 | 0.00 | 0.00 | +0.00 | 0.00 | 0.00 | +0.00 |
| case_selection | 20.83 | 0.00 | -20.83 | 5.72 | 0.00 | -5.72 | 20.83 | 0.00 | -20.83 |
| database_type | 24.67 | 0.00 | -24.67 | 12.53 | 0.00 | -12.53 | 16.67 | 0.00 | -16.67 |
| pain_point | 30.56 | 3.33 | -27.23 | 13.32 | 2.00 | -11.32 | 27.78 | 2.78 | -25.00 |

### Anthropic

| Prompt Type | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ai_infra | 5.33 | 15.33 | +10.00 | 1.50 | 11.59 | +10.09 | 6.67 | 10.00 | +3.33 |
| case_selection | 16.67 | 26.67 | +10.00 | 4.48 | 19.57 | +15.09 | 8.33 | 16.67 | +8.34 |
| database_type | 25.33 | 34.00 | +8.67 | 9.65 | 17.68 | +8.03 | 20.00 | 33.33 | +13.33 |
| pain_point | 34.44 | 46.11 | +11.67 | 14.74 | 20.80 | +6.06 | 11.11 | 38.89 | +27.78 |

## Readout

Anthropic web search materially improves TiDB visibility and recommendation strength in this run. TiDB gains +10.32 Answer Share, +9.04 Citation Authority, and +14.16 Recommendation Rate overall. The largest TiDB movement is in pain-point prompts, where Recommendation Rate rises from 11.11 to 38.89.

OpenAI web search does not improve TiDB in this run. This result should be interpreted cautiously because the web-on run used `gpt-4o-mini` while the off baseline used mostly `gpt-5-mini`. It is still useful operationally: OpenAI web-on in low mode was more search-grounded but less likely to name database products in the same way as the baseline.

The biggest cost change is Anthropic. Web search raised Anthropic cost from $0.8728 to $5.6844 for 120 prompts. Most of that increase came from retrieved web context tokens, not just the per-search fee.

## Recommendation

Keep web search as a separate benchmark mode rather than replacing the default monthly KPI. Use web-search-off for continuity with the existing baseline, and run web-search-on as a citation-grounded diagnostic view. For action planning, Anthropic web-on is the more useful signal in this experiment; OpenAI web-on needs a same-model supported configuration before it should be used for strategic trend claims.
