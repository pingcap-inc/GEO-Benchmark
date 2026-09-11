# Monthly Prompt Research

The prompt research workflow proposes up to 20 questions for human review after a benchmark run. It never edits the approved `prompts.json` file.

## Signal policy

Candidates must map to an approved seed theme and appear in at least two of three signal groups:

1. **Internal:** aggregated GSC, site-search, sales, support, survey, or community questions supplied in a monthly CSV.
2. **External:** People Also Ask and Google Trends collected through DataForSEO, plus Semrush keyword metrics.
3. **Model observed:** fan-out queries captured in the completed benchmark's `raw_answers.jsonl`.

Semrush, People Also Ask, and Trends all count as one external group. Multiple external tools do not satisfy the two-group requirement by themselves. Relevance is a human-controlled in-scope/out-of-scope gate and is not part of the numeric ranking.

The priority score is:

```text
50% cross-source support + 30% buyer intent + 20% coverage gap
```

The deterministic classifier records whether intent is decision, evaluation, or education. Coverage is compared with the current month's approved prompts. The output explains its evidence so reviewers can change or reject the recommendation.

## Credentials

Add these values to `.env.local`; do not commit them:

```text
SEMRUSH_API_KEY=
DATAFORSEO_LOGIN=
DATAFORSEO_PASSWORD=
```

DataForSEO uses the API login and password shown in its API Access dashboard, not a single API key. The workflow calls Google Organic Live Advanced for People Also Ask and Google Trends Explore Live for 12-month interest data. Semrush Version 4 keyword metrics supplies volume, intent, difficulty, SERP features, and its 12-month trend array.

## Approved seed queries

The default seed list is `geo-benchmark/config/prompt_research_seeds.csv`. It contains short search queries derived from the approved monitoring topics, their theme, branded/non-branded class, matching phrases, and review status. Only rows with `status=approved` are queried.

Edit and review this file when the monitored market changes. Keep branded and non-branded seeds separate so TiDB terminology does not manufacture non-branded discovery demand.

## Internal signals

The first invocation creates this template when it does not exist:

```text
<data-dir>/prompt-research/<month>/internal_signals.csv
```

Schema:

```csv
query,source,frequency,notes
database for persistent AI agent memory,gsc,12,Aggregated query theme
```

Supply aggregated, non-sensitive themes. Do not include customer names, email addresses, account details, raw sales transcripts, or other personal information. Unmapped rows are reported as warnings instead of being forced into an unrelated theme.

## Run it

Run the benchmark and prompt research together:

```bash
MONTH=2026-09 PROVIDERS=openai,anthropic,gemini,perplexity WEB_SEARCH=on \
PROMPT_RESEARCH=on ./scripts/run-benchmark-workflow.sh
```

Run research again from an existing completed run:

```bash
./geo-bench --data-dir geo-benchmark research-prompts --month 2026-09
```

External responses are cached. A normal rerun reuses the cache and does not spend new API units. Use `--refresh` only when a fresh paid collection is intended. Use `--max-seeds 3` for a small paid canary.

Use only cached data and make no external calls:

```bash
./geo-bench --data-dir geo-benchmark research-prompts --month 2026-09 --offline
```

Individual sources can be disabled with `--skip-paa`, `--skip-trends`, or `--skip-semrush`.

## Outputs

Files are written under `<data-dir>/reports/<month>/prompt-research/`:

- `top_20_prompt_candidates.csv`: ranked review queue with proposed prompt, theme, classification, evidence, score, and review fields.
- `prompt_research_evidence.csv`: normalized audit trail for every usable internal, external, and fan-out signal.
- `prompt_research_summary.json`: coverage, warning, policy, and API-usage metadata.
- `prompt-research.md`: concise human-readable review report.
- `raw/`: cached external API responses.

These files are gitignored because they can contain internal query text and paid API response data. A sanitized, approved prompt can be added through the normal prompt-review process after a reviewer marks it approved.

The command may produce fewer than 20 candidates when fewer than 20 questions meet the two-group rule, scope mapping, deduplication, and coverage checks. It does not fill the list with unsupported generated questions.
