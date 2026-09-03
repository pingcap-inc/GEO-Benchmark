# GEO Benchmark Suite Runbook

## One-Command Run

Normal monthly runs should use the guarded workflow wrapper:

```bash
MONTH=2026-08 PROVIDERS=mock RUNS=1 ./scripts/run-benchmark-workflow.sh
```

This workflow:

1. Validates the canonical prompt set and stops on policy violations.
2. Runs collection through the selected providers.
3. Retries only recoverable technical failures when fallback is configured.
4. Scores the final answer set.
5. Generates the single LLM report and machine-readable artifacts.
6. Runs local code checks.

The repository also includes a dependency-light Python CLI:

```bash
./geo-bench run --month 2026-08 --providers mock --runs 1
```

Web search is off by default. To enable provider web search for OpenAI, Anthropic, and Gemini, use low mode:

```bash
MONTH=2026-08 PROVIDERS=openai,anthropic,gemini WEB_SEARCH=on RUNS=1 ./scripts/run-benchmark-workflow.sh
```

Equivalent CLI flag:

```bash
./geo-bench run --month 2026-08 --providers openai,anthropic,gemini --runs 1 --web-search on
```

`web_search=off` and `web_search=on` rows are stored with separate answer IDs. Scoring and reports aggregate only the selected mode, so the two modes are not mixed in one KPI table.

This command:

1. Creates or reads the monthly prompt set.
2. Calls the selected provider.
3. Stores provider answers.
4. Retries failed answers for providers with fallback configuration.
5. Scores Consideration Rate, Answer Share, Citation Authority, and Recommendation Rate.
6. Generates Overall and Unchanged KPI views for every target in `targets.json`.
7. Writes cost estimates and reports.

Output layout:

```text
geo-benchmark/
  config/
  prompts/<month>/
  runs/<month>/
  reports/<month>/
```

Prompt uniqueness rule: `geo-benchmark/prompts/<month>/prompts.json` is the only canonical prompt source. Provider-specific directories such as `geo-benchmark-openai` must not keep separate prompt copies; they read from the canonical prompt tree.

Primary report artifacts:

```text
geo-benchmark/reports/<month>/llm-report.md
geo-benchmark/reports/<month>/target-kpi-summary.csv
geo-benchmark/reports/<month>/kpi_summary.json
geo-benchmark/reports/<month>/planned_cost_summary.json
geo-benchmark/reports/<month>/cost_summary.json
```

The human-readable LLM report is always a single Markdown file: `llm-report.md`. CSV and JSON files are audit and downstream-analysis artifacts.

## Query Fan-Out and Consideration Rate

When web search is enabled, the collector stores the search queries exposed by the provider in `fan_out_queries`. Each answer also records a `fan_out_status`:

| Status | Meaning | Included in consideration rate |
| --- | --- | --- |
| `captured` | One or more executed search queries were returned | Yes |
| `no_search` | Query capture is supported, but the model did not search | Yes, as not considered |
| `not_exposed` | Search happened or is built in, but the response omitted query text | No |
| `disabled` | Web search was disabled for the request | No |
| `request_failed` | The provider request failed | No |
| `not_supported` | The provider adapter does not support query capture, including mock runs | No |
| `unavailable` | A legacy row has no fan-out status | No |

Provider behavior is based on the structured response returned by each developer API:

| Provider | Response field | Support |
| --- | --- | --- |
| OpenAI | `web_search_call.action.query` or `.queries` | Captured |
| Anthropic | `server_tool_use.input.query` for `web_search` | Captured, with up to five searches per answer by default |
| Gemini | `groundingMetadata.webSearchQueries` | Captured when `--web-search on` enables Google Search grounding |
| Perplexity Sonar | `search_results` contains result pages, but no executed query field | Marked `not_exposed` |

Consideration is scored per target-answer row. A target is considered when one of its configured product aliases appears in at least one captured query. The aggregate rate is intent-weighted in the same way as Answer Share. It uses only non-branded rows and only providers where query capture is observable. `consideration_coverage` reports the fraction of non-branded answer rows in that denominator, so unsupported or missing data cannot silently become a zero.

Existing raw rows have no fan-out fields and remain outside the consideration denominator. Re-collect with `--web-search on` to populate the metric. Provider response schemas: [OpenAI web search](https://developers.openai.com/api/docs/guides/tools-web-search), [Anthropic web search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool), [Gemini Google Search grounding](https://ai.google.dev/gemini-api/docs/generate-content/google-search), and [Perplexity Sonar](https://docs.perplexity.ai/docs/sonar/models/sonar).

## Real Providers

The `mock` provider is free and useful for pipeline validation, but it is not a market benchmark. Before running real providers, configure API keys:

```bash
export OPENAI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
export GEMINI_API_KEY="..."
export PERPLEXITY_API_KEY="..."
```

Then run:

```bash
./geo-bench run \
  --month 2026-08 \
  --providers openai,anthropic,gemini,perplexity \
  --runs 3 \
  --web-search off
```

## Filtered Refresh

If only one prompt slice changes, do not rerun the whole month. Use a filtered refresh to preserve all other provider answers:

```bash
MONTH=2026-08 \
DATA_DIR=geo-benchmark-openai \
PROVIDERS=openai \
RUNS=1 \
FORCE=1 \
ONLY_PROMPT_TYPE=ai_infra \
ASSUMED_OUTPUT_TOKENS=1600 \
./scripts/run-benchmark-workflow.sh
```

You can also refresh exact prompt IDs:

```bash
MONTH=2026-08 \
DATA_DIR=geo-benchmark-openai \
PROVIDERS=openai \
RUNS=1 \
FORCE=1 \
ONLY_PROMPT_IDS=stable_ai_infra_001,dyn_202608_ai_infra_009 \
./scripts/run-benchmark-workflow.sh
```

Semantics:

1. `--force` alone removes that provider's monthly raw answers and reruns the full provider/month.
2. `--force --only-prompt-type <type>` removes only matching provider/prompt-type rows.
3. `--force --only-prompt-ids <ids>` removes only matching provider/prompt-id rows.
4. Every filtered refresh still regenerates the full score and report from the final answer set.

## OpenAI Fallback

The standard OpenAI execution policy is:

```text
primary:  gpt-5-mini, max_output_tokens=1600
fallback: gpt-4o-mini, max_output_tokens=1000
```

`run` calls the primary model first. If OpenAI returns recoverable failures such as empty content or timeout, the CLI retries only failed rows and then scores/reports the final answer set. Missing keys, invalid keys, insufficient quota, billing, and authorization errors are not automatically retried.

To audit pure primary-model output, disable fallback:

```bash
./geo-bench run \
  --month 2026-08 \
  --providers openai \
  --runs 1 \
  --no-fallback
```

To repair failures after a completed run:

```bash
./geo-bench retry-errors \
  --month 2026-08 \
  --provider openai \
  --model gpt-4o-mini \
  --max-output-tokens 1000
```

## Configuration

Provider and model settings:

```text
geo-benchmark/config/models.json
```

Pricing settings:

```text
geo-benchmark/config/pricing.json
```

Prices change over time. Review pricing before production runs.

Target products:

```text
geo-benchmark/config/targets.json
```

Default target set: TiDB, CockroachDB, YugabyteDB, Supabase, PlanetScale, Neon.

## Prompt Audit

Hard validation gate:

```bash
./geo-bench validate-prompts --month 2026-08
```

This exits non-zero when:

- Prompt text contains a measured product name.
- Prompt text is duplicated.
- Source evidence metadata is missing.
- A `serverless_ai` prompt mentions PostgreSQL, Postgres, or pgvector.

Check whether prompt text contains measured target names:

```bash
./geo-bench audit-prompts --month 2026-08
```

Current starter-set audit:

```text
Total prompts: 120
tidb: 0
cockroachdb: 0
yugabytedb: 0
aurora: 0
spanner: 0
planetscale: 0
alloydb: 0
```

The starter set asks buyer-pain, database-category, AI-infrastructure, and case-selection questions without naming measured vendors.

## Cost Estimate

Estimate budget without calling providers:

```bash
./geo-bench estimate-cost \
  --month 2026-08 \
  --providers openai,anthropic,gemini,perplexity \
  --runs 3 \
  --assumed-output-tokens 700 \
  --web-search on
```

Default planning assumptions: 120 prompts, 4 providers, 3 runs per prompt, and 700 assumed output tokens per answer. Adding scoring targets does not increase provider-call cost because targets are scored locally against the same answers.

Example estimate:

```text
Total estimated cost: $18.1136
openai / gpt-5-mini: $4.1158
anthropic / claude-sonnet-5: $6.2144
gemini / gemini-3.5-flash-lite: $5.6842
perplexity / sonar: $2.0992
```

OpenAI and Anthropic web search estimates assume one low-mode search call per prompt run when `--web-search on` is used. Actual cost summaries use the recorded tool-call count when providers return it. Claude may perform up to five searches per answer, so actual cost can exceed that planning assumption. Gemini 3.5 Flash-Lite pricing includes 5,000 free Google Search requests per month shared across Gemini 3.x models, then charges per individual search query; the planning estimate uses the post-allowance marginal rate. Perplexity Sonar includes a request fee, so its cost is not token-only.

## Monthly Comparability

The default monthly suite has 120 prompts:

- 84 stable prompts locked for at least six months.
- 36 dynamic prompts updated at most monthly.

Reports show both:

- `Overall KPI`: all 120 prompts.
- `Unchanged KPI`: stable prompts only.

If Overall improves but Unchanged does not, do not claim a strict like-for-like GEO improvement.

## Anti-Gaming Controls

- Freeze `prompt_set_hash` before running.
- Lock 84 stable prompts for at least six months.
- Keep source evidence on every dynamic prompt.
- Run `validate-prompts` before any provider call.
- Use fixed run counts per prompt.
- Retry only technical failures, never low-scoring answers.
- Report both Overall and Unchanged views.

## Monthly Compare

```bash
./geo-bench compare --from 2026-08 --to 2026-09
```
