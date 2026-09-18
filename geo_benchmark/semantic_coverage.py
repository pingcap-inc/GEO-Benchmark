"""Explain semantic decision coverage without changing accuracy denominators."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

EXPORT_FIELDS = [
    "semantic_coverage_disposition", "semantic_coverage_status",
    "semantic_coverage_reason", "semantic_selected_facts",
    "semantic_not_applicable_facts", "semantic_pending_fact_ids",
]
REASONS = {
    "scored": "At least one selected fact has a correct/incorrect decision; other claims may remain unchecked.",
    "comparison_metric_only": "Excluded from semantic fact judging by the approved mapping, regardless of topic cluster.",
    "review_required": "No ready fact produced a decision; mapped facts or review items await approval.",
    "not_enough_information": "The judge evaluated selected facts but could not reach a correct/incorrect decision.",
    "judge_unavailable": "At least one selected fact could not be evaluated; no decisive score is available.",
    "not_applicable": "All evaluated facts were not applicable to this answer.",
    "disabled": "Semantic judging was disabled for this answer.",
    "unmapped": "No fact mapping was selected for this non-branded answer.",
    "not_targeted": "The semantic judge does not evaluate this target.",
    "coverage_gap": "Missing or inconsistent judging evidence; inspect the mapping and saved result.",
    "not_recorded": "This saved row does not contain enough evidence to explain the missing score.",
}


def export_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Read saved evidence, never infer a disposition from a topic/legacy score."""
    payload = row.get("semantic_fact_judge") or {}
    disposition = payload.get("coverage_disposition", row.get("semantic_coverage_disposition", ""))
    selected = payload.get("selected_facts", row.get("semantic_selected_facts", ""))
    not_applicable = payload.get("not_applicable_facts", row.get("semantic_not_applicable_facts", 0))
    unavailable = payload.get("unavailable_facts", row.get("semantic_unavailable_facts", 0))
    inconclusive = payload.get("not_enough_information_facts", row.get("semantic_not_enough_information_facts", 0))
    accuracy = payload.get("accuracy", row.get("semantic_fact_accuracy"))
    mode = payload.get("mode", row.get("run_metadata", {}).get("fact_judge_mode", row.get("fact_judge_mode")))
    branded = row.get("target_in_prompt") in (True, "True", "true", 1)
    pending = payload.get("pending_fact_ids", row.get("semantic_pending_fact_ids", []))
    if isinstance(pending, (list, tuple)):
        pending = "|".join(pending)
    if row.get("target", "TiDB") != "TiDB":
        status = "not_targeted"
    elif mode == "off":
        status = "disabled"
    elif accuracy not in (None, ""):
        status = "scored"
    elif disposition == "comparison_metric_only":
        status = "comparison_metric_only"
    elif int(unavailable or 0):
        status = "judge_unavailable"
    elif int(inconclusive or 0):
        status = "not_enough_information"
    elif int(not_applicable or 0):
        status = "not_applicable"
    elif disposition == "review_required" and not int(selected or 0):
        status = "review_required"
    elif disposition == "unmapped" and not branded:
        status = "unmapped"
    elif disposition:
        status = "coverage_gap"
    else:
        status = "not_recorded"
    return {
        "semantic_coverage_disposition": disposition,
        "semantic_coverage_status": status,
        "semantic_coverage_reason": REASONS[status],
        "semantic_selected_facts": selected,
        "semantic_not_applicable_facts": not_applicable,
        "semantic_pending_fact_ids": pending,
    }


def write_coverage_report(report_dir: Path, rows: list[dict[str, Any]]) -> None:
    """Write every branded answer and a reconciled, provider-aware review queue."""
    records = []
    for row in rows:
        if row.get("target", "TiDB") != "TiDB" or row.get("target_in_prompt") not in (True, "True", "true", 1):
            continue
        records.append({
            **{key: row.get(key, "") for key in ("answer_id", "prompt_id", "model_surface", "prompt_type", "group")},
            **export_fields(row),
        })
    fields = ["answer_id", "prompt_id", "model_surface", "prompt_type", "group", *EXPORT_FIELDS]
    with (report_dir / "semantic-coverage-audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    counts = Counter(row["semantic_coverage_status"] for row in records)
    providers = sorted({row["model_surface"] for row in records})
    summary = {
        "branded_answers": len(records),
        "decisive_answers": counts.get("scored", 0),
        "status_counts": dict(sorted(counts.items())),
        "by_provider": {
            provider: dict(Counter(row["semantic_coverage_status"] for row in records if row["model_surface"] == provider))
            for provider in providers
        },
        "prompt_ids_by_status": {
            status: sorted({row["prompt_id"] for row in records if row["semantic_coverage_status"] == status})
            for status in sorted(counts)
        },
        "unexplained_answers": counts.get("coverage_gap", 0) + counts.get("not_recorded", 0),
    }
    (report_dir / "semantic-coverage-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    lines = ["", "## Semantic Coverage Audit", "",
             "Decision coverage is not processing coverage. Comparison-only mappings can occur in any topic cluster. "
             "A legacy checked-fact count does not establish semantic eligibility.", "",
             "| Outcome | Branded answers | Explanation |", "| --- | ---: | --- |"]
    lines += [f"| {status} | {count} | {REASONS[status]} |" for status, count in sorted(counts.items())]
    lines += ["", f"Reconciled total: {sum(counts.values())}/{len(records)} branded answers. "
              "See `semantic-coverage-audit.csv` for exact prompt/provider IDs and pending fact IDs. "
              "Scored answers may still have pending review items. Existing accuracy and coverage denominators are unchanged.", ""]
    with (report_dir / "llm-report.md").open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
