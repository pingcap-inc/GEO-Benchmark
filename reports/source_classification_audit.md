# September 2026 Gemini source-classification audit

Scope: `gemini-3.5-flash-lite`, web search on, 219 saved answers, source-authority version changed from `2026-09-24` to `2026-09-25-path-aware`.

This audit uses only the saved September cited-domain exports and answer-review evidence. Counts are unique cited answers and may overlap because one answer can cite more than one source type. No provider calls were made.

## Cited-answer classification

| Source type | Before | After | Change |
| --- | ---: | ---: | ---: |
| PingCAP | 165 | 166 | +1 |
| Competitor | 73 | 73 | 0 |
| Other | 182 | 179 | -3 |

The changes come from classifying `zero.tidbcloud.com` and `tidbcloudzerobrowser.vercel.app` as PingCAP-owned while preserving unrelated `*.vercel.app` hosts as Other. Code-host citations are now classified from their first path segment and displayed separately as `github.com/<org>` (and equivalently for GitLab or Hugging Face), so `github.com/pingcap/*`, competitor repositories, and unrelated repositories no longer collapse into one `github.com` row.

## TiDB citation authority

The source-authority scorer now uses the same path-aware ownership helper when deciding whether a code-host URL is related to TiDB. The September visibility KPI does not move because the newly recognized TiDB Cloud hosts occur outside the non-branded visibility slice or do not alter its weighted score.

| Cluster | Before | After |
| --- | ---: | ---: |
| Overall | 13.61 | 13.61 |
| AI Agent Infrastructure | 12.28 | 12.28 |
| Competitive Comparisons | 33.75 | 33.75 |
| Deployment & Cloud | N/A | N/A |
| Enterprise & Compliance | 0.00 | 0.00 |
| Hybrid Search & RAG | 4.09 | 4.09 |
| MCP & Developer Tooling | 2.81 | 2.81 |
| MySQL Scale & Migration | 28.98 | 28.98 |
| Observability | N/A | N/A |
| Scale & Architecture | 23.33 | 23.33 |
| TiDB Brand & Definitions | N/A | N/A |
