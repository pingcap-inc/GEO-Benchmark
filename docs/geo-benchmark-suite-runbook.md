# GEO Benchmark Suite Runbook

## One-Command Run

Use the guarded workflow wrapper for a no-cost end-to-end check:

```bash
DATA_DIR=geo-benchmark-dry-run MONTH=2026-09 PROVIDERS=mock RUNS=1 FACT_JUDGE=mock ./scripts/run-benchmark-workflow.sh
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
5. Scores Consideration Rate, Mention Rate, Prominence Score, Citation Authority, Recommendation Rate, and Comparison Win Rate.
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
| Gemini | `groundingMetadata.webSearchQueries` | Captured when `--web-search on` enables Google Search grounding; grounding redirect URLs are resolved to their destination domains for citation scoring |
| Perplexity Sonar | `search_results` contains result pages, but no executed query field | Marked `not_exposed` |

Consideration is scored per target-answer row. A target is considered when one of its configured product aliases appears in at least one captured query. The aggregate rate is intent-weighted in the same way as Prominence Score. It uses only non-branded rows and only providers where query capture is observable. `consideration_coverage` reports the fraction of non-branded answer rows in that denominator, so unsupported or missing data cannot silently become a zero.

Existing raw rows have no fan-out fields and remain outside the consideration denominator. Re-collect with `--web-search on` to populate the metric. Provider response schemas: [OpenAI web search](https://developers.openai.com/api/docs/guides/tools-web-search), [Anthropic web search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool), [Gemini Google Search grounding](https://ai.google.dev/gemini-api/docs/generate-content/google-search), and [Perplexity Sonar](https://docs.perplexity.ai/docs/sonar/models/sonar).

## Real Providers

The `mock` provider is free and useful for pipeline validation, but it is not a market benchmark. Before running real providers, configure API keys:

```bash
export OPENAI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
export GEMINI_API_KEY="..."
export PERPLEXITY_API_KEY="..."
```

## Semantic Fact Judge

The semantic judge is opt-in and remains a shadow metric:

```bash
# Keyless end-to-end judge test
DATA_DIR=geo-benchmark-dry-run MONTH=2026-09 PROVIDERS=mock FACT_JUDGE=mock ./scripts/run-benchmark-workflow.sh

# Live OpenAI judge over existing answers
./geo-bench --data-dir geo-benchmark score \
  --month 2026-09 \
  --fact-judge live \
  --fact-judge-provider openai \
  --fact-judge-model gpt-5-mini
```

Only `READY_FOR_JUDGE` facts are evaluated. `REVIEW_REQUIRED` facts remain
visible but unscored. General definition questions require the core capability;
maturity, plan, region, version, and access qualifiers activate only when the
question asks or the answer makes a specific claim. Judge failures are recorded
as `judge_unavailable`, not as inaccurate answers. Successful judgments are
cached by answer, prompt, fact-base version, model, and qualifier scope.

### Monthly fact coverage workflow

The coverage CSV is a generated review artifact, not another manually authored
prompt list. It joins each branded prompt to the fact or review IDs that the
semantic judge should use.

```bash
./geo-bench --data-dir geo-benchmark prepare-fact-coverage --month 2026-10
./geo-bench --data-dir geo-benchmark validate-fact-coverage --month 2026-10
```

Preparation finds the newest earlier coverage CSV by default. A reviewer can
select a specific source with `--from-month`. A mapping is reused only when its
prompt ID and exact prompt text are unchanged. New or edited branded prompts are
written with `mapping_status=needs_review`; non-branded prompts are excluded.

For each pending row, the reviewer must select one disposition, add the required
fact or review IDs, update the note if useful, and set `mapping_status=approved`:

| Disposition | Meaning | ID rule |
| --- | --- | --- |
| `fact_covered` | Approved facts can score the answer | One or more `READY_FOR_JUDGE` fact IDs |
| `review_required` | Product truth is still held behind a fact-base review | One or more fact or review-queue IDs |
| `comparison_metric_only` | The prompt is evaluated by comparison metrics | No IDs |

Both the wrapper workflow and direct `run --fact-judge mock|live` validate this
file before provider collection. Missing, stale, duplicate, unknown, or pending
mappings stop the run with the affected prompt IDs.

Approval must be explicit: a blank or missing `mapping_status` is not approved.
The previously reviewed September mappings have been migrated to explicit
`approved` values without changing their fact assignments.

Saved judgments are invalidated when the fact-base content, question text,
answer, or judge-contract version changes, even if the fact-base schema label
stays the same. Unknown judge-model pricing is reported as unknown, not zero;
the combined cost is also unknown until that pricing is configured.

### Recovering unavailable live fact judgments

The OpenAI judge requests a strict JSON schema and allows 4,000 output tokens.
The larger allowance is a ceiling, not a guaranteed usage amount; monitor the
reported judge cost. See the [OpenAI structured outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses).

Each new live verdict includes `response_diagnostics` with per-attempt response
status, response ID, available token usage, incomplete reason, and a bounded
500-character output preview. These are saved locally in scored answers (and
in the cache for successful judgments). Request headers and full API payloads
are not stored. Output-limit, empty-output, refusal, invalid-JSON, and invalid-schema
failures remain `judge_unavailable`, not inaccurate. Refusals are not retried;
other response failures respect `--fact-judge-retries`.

After updating the code, re-score the existing five-answer canary:

```bash
./geo-bench --data-dir geo-benchmark-live-canary score \
  --month 2026-09 --targets TiDB --web-search off \
  --fact-judge live --fact-judge-provider openai \
  --fact-judge-model gpt-5-mini --fact-judge-retries 1
```

This does not collect answers again. It preserves the raw answers, reuses valid
cached verdicts, and retries judgments that were unavailable. It replaces scored
outputs and reports; copy those first if you need to retain the prior report.
For a ZIP-based installation, preserve `.env.local` and the entire
`geo-benchmark-live-canary` directory when moving to a new checkout.

### Conditional qualifier validation

The system-level scope policy overrides per-fact correctness checklists. Runtime
judge input is built from canonical truth, correctness/contradiction examples,
and applicability instead of the legacy concatenated `judge_prompt`. Correctness
examples are not a mandatory checklist. For Cloud Zero, a temporary database
experience is the core; preview status, exact lifetime, signup details, and the
Starter claim flow need not all appear in a general definition. Missing an asked
qualifier is `not_enough_information`; explicit false claims are `incorrect`.
Activating plan checks does not automatically require maturity or other dimensions.

This is an evaluation-policy change. The new cache contract invalidates prior
judgments, including successful ones; re-scoring the five-answer canary will
make up to three fresh fact judgments, without regenerating answers.

Preview eight fixed examples without keys:

```bash
python3 -m geo_benchmark.qualifier_eval
```

Run the same examples against the real judge (paid OpenAI calls, no answer generation):

```bash
python3 -m geo_benchmark.qualifier_eval --live
```

The live command prints each expected verdict, actual verdict, explanation, and
match status, and exits unsuccessfully if any case disagrees or is unavailable.
Expected verdicts are not sent to the judge. Results are cached in the separate
`geo-benchmark-qualifier-check` run directory. These are policy fixtures based on
the current candidate fact base, not independent product verification. Revisit
the expectations when product truth changes. Keyless tests check the instruction
wiring and cache invalidation; they do not prove semantic judge compliance.

### Activation stages

| Stage | Credentials | Required checks |
| --- | --- | --- |
| Unit | None | Coverage mapping, review gates, qualifier activation, parsing, caching, and calculations |
| Mock end to end | None | Prompt collection through semantic reports with deterministic verdicts |
| Failure handling | Missing or invalid test key | Authentication, malformed output, retries, and `judge_unavailable` |
| Live canary | Real key | Correct, incorrect, incomplete, availability, volunteered-claim, review-gated, and comparison cases |
| Shadow benchmark | Real key | Literal and semantic results side by side, with cost and latency |
| Activation gate | Human review | Approve a stratified sample and resolve disagreements before replacing the official score |

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
