# Publication Notes

This repository upload contains the benchmark code, documentation, configuration, prompt sets, and latest scored/report artifacts for the 2026-08 runs.

This revision also includes the guarded monthly workflow:

- `geo-bench validate-prompts`: hard-fail prompt policy validation.
- `scripts/run-benchmark-workflow.sh`: validate, run with configured fallback, score, report, and run local checks.
- `--web-search off|on` and `WEB_SEARCH=on`: optional low-mode provider web search for OpenAI and Anthropic.

Included result artifacts:

- `geo-benchmark/reports/2026-08/`: Anthropic report tables and machine-readable summaries.
- `geo-benchmark/runs/2026-08/scored_answers.jsonl`: Anthropic scored rows.
- `geo-benchmark-openai/reports/2026-08/`: OpenAI report tables and machine-readable summaries.
- `geo-benchmark-openai/runs/2026-08/scored_answers.jsonl`: OpenAI scored rows.

Canonical prompt source:

- `geo-benchmark/prompts/2026-08/prompts.json`

Provider-specific directories do not include duplicate prompt files.

Raw provider transcripts are intentionally not included in this public upload because some model answers contain non-English text and the publication requirement is English-only repository content. The included scored rows and reports are sufficient to reproduce KPI tables and gap analysis from the latest scoring pass.

Local-only files excluded from publication:

- `.env.local` and other secret-bearing environment files.
- Retry backups and aborted-run raw answer snapshots.
- Temporary scraped HTML and local visual/output artifacts.
