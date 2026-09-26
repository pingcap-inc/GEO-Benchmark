# September 2026 Gemini comparison-winner audit

Scope: `gemini-3.5-flash-lite`, web search on, 219 saved answers, prompt metadata revision `2026-09-18-review-1`.

This audit uses only the saved `scored_answers.csv` and `answer-review.md`. No provider calls were made. The TiDB comparison slice contains 51 answers: one excluded pending prompt review and 50 eligible answers.

## Baseline

| Outcome | Answers |
| --- | ---: |
| Excluded pending review | 1 |
| Eligible with a detected winner | 4 |
| Eligible with an empty winner | 46 |
| TiDB wins among valid answers | 2 |
| TiDB comparison win rate | 50.00% (n = 4), low sample |

## Audit of the 46 empty-winner answers

| Bucket | Definition | Count | Example answer IDs |
| --- | --- | ---: | --- |
| A | A clear tracked-product winner was present but missed | 3 | `9616053009c864985152172f`, `9c55612a31e74bbf60f1f8f7`, `7d02366d9455595605dd2f3a` |
| B | The winner was not one of the six configured KPI targets | 3 | `b21c1f9970810d3901704347`, `3254e7a272b870cc93ef2981`, `926ec27ecf1b4cb3301b61eb` |
| C | Conditional, tied, use-case split, or no clear winner | 40 | `4c808294b6f9da60b4619832`, `8c57626cd5f91dc3d438dca5`, `f4dc0074974912a92425fc38` |

Bucket A consisted of two TiDB wins and one CockroachDB win. Bucket B consisted of two SingleStore wins and one MySQL win. Bucket C contained 39 explicit conditional/use-case splits and one answer with no clear winner.

## After revised detection

| Outcome | Before | After |
| --- | ---: | ---: |
| Eligible answers | 50 | 50 |
| Valid detected winners | 4 | 7 |
| Conditional/use-case split | Empty winner cell | 42 |
| No clear winner | Empty winner cell | 1 |
| TiDB wins among valid answers | 2 | 2 |
| TiDB comparison win rate | 50.00% (n = 4), low sample | 28.57% (n = 7), low sample |

The denominator now includes losses to SingleStore and MySQL even though they are not configured KPI targets. Conditional and no-clear-winner outcomes remain outside the win-rate denominator. Three old winners (two TiDB and one Neon) were also corrected to conditional because their answers explicitly split the recommendation by use case; the prior detector returned before applying that hedge check.

## Hand-checked changed outcomes

| Answer ID | Prompt ID | Before | After | Evidence checked |
| --- | --- | --- | --- | --- |
| `9616053009c864985152172f` | `stable_hybridrag_015` | Empty | TiDB winner | Final recommendation says to adopt TiDB. |
| `b21c1f9970810d3901704347` | `stable_compcomp_010` | Empty | SingleStore winner | Recommendation shortlist ranks SingleStore first. |
| `3254e7a272b870cc93ef2981` | `stable_compcomp_015` | Empty | MySQL winner | Recommendation shortlist ranks MySQL first. |
| `9c55612a31e74bbf60f1f8f7` | `stable_compcomp_020` | Empty | CockroachDB winner | Recommendation shortlist ranks CockroachDB first. |
| `7d02366d9455595605dd2f3a` | `stable_deploycloud_010` | Empty | TiDB winner | TiDB Cloud Essential is explicitly marked recommended for production. |
| `926ec27ecf1b4cb3301b61eb` | `stable_branddef_034` | Empty | SingleStore winner | Recommendation shortlist ranks SingleStore first. |
| `1aa4a6bba451355604ead7c5` | `stable_hybridrag_003` | TiDB winner | Conditional | The recommendation assigns TiDB and Weaviate to different workload shapes. |
| `bf697dd8e47cb58ebeed865d` | `stable_compcomp_002` | Neon winner | Conditional | The verdict selects Neon or TiDB Cloud according to scale and workload. |
| `89c2ac944e1551609a147d51` | `stable_deploycloud_007` | TiDB winner | Conditional | The answer chooses different TiDB deployment products for different requirements. |
| `7d779dbd5e9d42e562313de5` | `stable_compcomp_026` | Empty | Conditional | The decision changes at a stated scaling threshold rather than naming an unconditional winner. |
| `4c808294b6f9da60b4619832` | `stable_compcomp_001` | Empty | Conditional | TiDB is chosen for write-heavy scale; Aurora is chosen for read-heavy AWS-native workloads. |
| `8c57626cd5f91dc3d438dca5` | `stable_hybridrag_004` | Empty | Conditional | The verdict chooses TiDB or Qdrant based on metadata and retrieval shape. |
| `f4dc0074974912a92425fc38` | `stable_compcomp_006` | Empty | Conditional | YugabyteDB is selected for PostgreSQL/multi-region needs and TiDB for MySQL/HTAP needs. |
| `4b470669f87509039a478f32` | `stable_compcomp_029` | Empty | Conditional | Neon and TiDB Cloud Zero are selected for different backend requirements. |
| `b87690d91644e22a2fbeb23f` | `stable_deploycloud_006` | Empty | Conditional | Cloud Zero and Starter are selected for disposable and persistent workloads respectively. |

## Guardrails applied

- A winner requires a unique explicit recommendation or an explicit first-ranked recommendation shortlist.
- The conditional/use-case-split check runs before legacy winner selection, so a hedged answer cannot be promoted to a win.
- Multiple explicit choices split by workload are `conditional`, even when both choices map to the TiDB brand.
- Mere mention order and ordinary comparison tables do not create winners.
- `conditional` and `no_clear_winner` are reported separately and excluded from the win-rate denominator.
