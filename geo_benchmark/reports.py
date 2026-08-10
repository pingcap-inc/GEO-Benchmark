from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .io_utils import ensure_dir, write_json


PROMPT_TYPE_ORDER = ["pain_point", "database_type", "ai_infra", "case_selection"]
TARGET_DISPLAY_ORDER = ["CockroachDB", "TiDB", "YugabyteDB", "Neon", "Supabase", "PlanetScale"]


def write_reports(
    report_dir: Path,
    month: str,
    summary: dict[str, Any],
    scored_answers: list[dict[str, Any]],
    cost_summary: dict[str, Any] | None,
) -> None:
    ensure_dir(report_dir)
    cleanup_legacy_single_target_files(report_dir)
    write_json(report_dir / "kpi_summary.json", summary)
    if cost_summary:
        write_json(report_dir / "cost_summary.json", cost_summary)
    write_markdown(report_dir / "llm-report.md", month, summary, cost_summary, scored_answers)
    write_target_summary_csv(report_dir / "target-kpi-summary.csv", summary)
    write_csv(report_dir / "scored_answers.csv", scored_answers)
    for target, target_summary in summary.get("targets", {}).items():
        safe_target = target.lower().replace(" ", "-")
        write_breakdown_csv(report_dir / f"model-breakdown-{safe_target}.csv", target_summary.get("by_model", {}))
        write_breakdown_csv(report_dir / f"use-case-breakdown-{safe_target}.csv", target_summary.get("by_use_case", {}))
        write_breakdown_csv(report_dir / f"prompt-type-breakdown-{safe_target}.csv", target_summary.get("by_prompt_type", {}))


def cleanup_legacy_single_target_files(report_dir: Path) -> None:
    for name in [
        "model-breakdown.csv",
        "use-case-breakdown.csv",
        "prompt-type-breakdown.csv",
        "executive-summary.md",
        "database-comparison.md",
        "audit-samples.md",
    ]:
        path = report_dir / name
        if path.exists():
            path.unlink()


def write_markdown(
    path: Path,
    month: str,
    summary: dict[str, Any],
    cost_summary: dict[str, Any] | None,
    scored_answers: list[dict[str, Any]],
) -> None:
    providers = sorted({row.get("model_surface", "unknown") for row in scored_answers})
    lines = [
        f"# GEO Benchmark LLM Report - {month}",
        "",
        f"Providers: {', '.join(providers) if providers else 'none'}",
        f"Web search mode: {cost_summary.get('web_search_mode', 'off') if cost_summary else 'off'}",
        f"Raw answers: {len({row.get('answer_id') for row in scored_answers})}",
        f"Scored target-answer rows: {len(scored_answers)}",
        "",
    ]
    if any(row.get("model_surface") == "mock" for row in scored_answers):
        lines.extend(
            [
                "> Warning: this report includes mock provider output. Use it only as a pipeline smoke test, not as a market benchmark.",
                "",
            ]
        )
    lines.extend(["## Executive KPI", ""])
    lines.extend(executive_kpi_table(summary))
    lines.extend(
        [
            "",
            "Overall columns use all prompts for the month. Stable columns use only stable prompts and are the strict comparable view.",
            "",
            "## Prompt-Type Breakdown",
            "",
        ]
    )
    lines.extend(prompt_type_metric_tables(summary))

    target_order = report_target_order(summary)
    first_target = target_order[0] if target_order else None
    first_summary = summary["targets"][first_target] if first_target else summary
    overall = first_summary["overall"]
    unchanged = first_summary["unchanged"]
    lines.extend(
        [
            "",
            "## Coverage",
            "",
            f"- Overall prompts per target: {overall['prompt_count']}",
            f"- Overall target-answer rows per target: {overall['answer_count']}",
            f"- Unchanged prompts per target: {unchanged['prompt_count']}",
            f"- Unchanged target-answer rows per target: {unchanged['answer_count']}",
            "",
            "## Quality Signals",
            "",
            f"- Average source authority shown below is target-specific in `target-kpi-summary.csv`.",
            "",
        ]
    )
    competitive_lines = ["## Competitive", ""]
    for target in summary.get("target_order", []):
        competitive = summary["targets"][target].get("competitive") or {}
        if not competitive:
            continue
        competitive_lines.extend(
            [
                f"### {target}",
                "",
                f"- Valid comparison answers: {competitive.get('valid_comparison_answers', 0)}",
                f"- Target win rate: {competitive.get('target_win_rate', 0)}%",
                f"- Winner counts: {competitive.get('winner_counts', {})}",
                "",
            ]
        )
    if len(competitive_lines) > 2:
        lines.extend(competitive_lines)
    if cost_summary:
        lines.extend(
            [
                "## Cost",
                "",
                f"- Estimated cost: ${cost_summary.get('total_estimated_cost_usd', 0)}",
                f"- Pricing version: {cost_summary.get('pricing_version')}",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def executive_kpi_table(summary: dict[str, Any]) -> list[str]:
    lines = [
        "| Target | Answer Share | Citation Authority | Recommendation Rate | Stable Answer Share | Stable Recommendation Rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for target in report_target_order(summary):
        metrics = summary["targets"][target]
        lines.append(
            "| "
            + " | ".join(
                [
                    target,
                    fmt(metrics["overall"].get("answer_share")),
                    fmt(metrics["overall"].get("citation_authority")),
                    fmt(metrics["overall"].get("qualified_recommendation_rate")),
                    fmt(metrics["unchanged"].get("answer_share")),
                    fmt(metrics["unchanged"].get("qualified_recommendation_rate")),
                ]
            )
            + " |"
        )
    return lines


def report_target_order(summary: dict[str, Any]) -> list[str]:
    present = set(summary.get("target_order", []))
    ordered = [target for target in TARGET_DISPLAY_ORDER if target in present]
    ordered.extend(sorted(present - set(ordered)))
    return ordered


def prompt_type_metric_tables(summary: dict[str, Any]) -> list[str]:
    tables: list[str] = []
    for title, metric_key in [
        ("Answer Share", "answer_share"),
        ("Citation Authority", "citation_authority"),
        ("Recommendation Rate", "qualified_recommendation_rate"),
    ]:
        if tables:
            tables.append("")
        tables.extend([f"### {title}", ""])
        tables.extend(prompt_type_metric_table(summary, metric_key))
    return tables


def prompt_type_metric_table(summary: dict[str, Any], metric_key: str) -> list[str]:
    target_order = report_target_order(summary)
    prompt_types = ordered_prompt_types(summary)
    lines = [
        "| Type | " + " | ".join(target_order) + " |",
        "| --- | " + " | ".join(["---:"] * len(target_order)) + " |",
    ]
    for prompt_type in prompt_types:
        cells = []
        for target in target_order:
            metrics = summary["targets"][target].get("by_prompt_type", {}).get(prompt_type, {})
            cells.append(fmt(metrics.get(metric_key)))
        lines.append(f"| `{prompt_type}` | " + " | ".join(cells) + " |")
    return lines


def prompt_type_leaders_table(summary: dict[str, Any]) -> list[str]:
    prompt_types = ordered_prompt_types(summary)
    lines = [
        "| Prompt Type | Answer Share Leader | Citation Authority Leader | Recommendation Leader |",
        "| --- | --- | --- | --- |",
    ]
    for prompt_type in prompt_types:
        metric_leaders = []
        for metric_key in ["answer_share", "citation_authority", "qualified_recommendation_rate"]:
            values: list[tuple[str, float]] = []
            for target in summary.get("target_order", []):
                value = summary["targets"][target].get("by_prompt_type", {}).get(prompt_type, {}).get(metric_key, 0)
                values.append((target, float(value)))
            leader_value = max((value for _, value in values), default=0.0)
            if leader_value == 0.0:
                metric_leaders.append("No leader (0.00)")
                continue
            leader_targets = [target for target, value in values if round(value, 2) == round(leader_value, 2)]
            metric_leaders.append(f"{', '.join(leader_targets)} ({fmt(leader_value)})")
        lines.append(f"| `{prompt_type}` | " + " | ".join(metric_leaders) + " |")
    return lines


def ordered_prompt_types(summary: dict[str, Any]) -> list[str]:
    prompt_types = {
        prompt_type
        for target in summary.get("target_order", [])
        for prompt_type in summary["targets"][target].get("by_prompt_type", {})
    }
    ordered = [prompt_type for prompt_type in PROMPT_TYPE_ORDER if prompt_type in prompt_types]
    ordered.extend(sorted(prompt_types - set(ordered)))
    return ordered


def fmt(value: Any) -> str:
    if value is None:
        return "0.00"
    return f"{float(value):.2f}"


def write_target_summary_csv(path: Path, summary: dict[str, Any]) -> None:
    fieldnames = [
        "target",
        "scope",
        "answer_share",
        "citation_authority",
        "qualified_recommendation_rate",
        "weighted_recommendation_score",
        "negative_recommendation_rate",
        "avg_source_authority",
        "avg_accuracy",
        "avg_freshness",
        "prompt_count",
        "answer_count",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for target in summary.get("target_order", []):
            for scope in ["overall", "unchanged"]:
                metrics = summary["targets"][target][scope]
                writer.writerow(
                    {
                        "target": target,
                        "scope": scope,
                        **{key: metrics.get(key) for key in fieldnames if key not in {"target", "scope"}},
                    }
                )


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = [
        "target_answer_id",
        "answer_id",
        "target",
        "month",
        "prompt_id",
        "model_surface",
        "panel",
        "prompt_type",
        "use_case",
        "target_in_prompt",
        "mentioned_target",
        "presence_score",
        "mention_position",
        "citation_authority_answer",
        "source_authority",
        "accuracy",
        "freshness",
        "recommendation_class",
        "recommendation_score",
        "competitive_winner",
        "input_tokens",
        "output_tokens",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in fieldnames})


def write_breakdown_csv(path: Path, breakdown: dict[str, Any]) -> None:
    fieldnames = [
        "segment",
        "prompt_count",
        "answer_count",
        "answer_share",
        "citation_authority",
        "qualified_recommendation_rate",
        "negative_recommendation_rate",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for segment, metrics in breakdown.items():
            writer.writerow({"segment": segment, **{key: metrics.get(key) for key in fieldnames if key != "segment"}})


def write_audit_samples(path: Path, rows: list[dict[str, Any]]) -> None:
    negative = [row for row in rows if row.get("recommendation_class") == "negative"][:20]
    low_citation = [row for row in rows if row.get("mentioned_target") and row.get("citation_authority_answer", 0) == 0][:20]
    lines = ["# Audit Samples", ""]
    lines.extend(["## Negative Recommendations", ""])
    if not negative:
        lines.append("No negative samples in this run.")
    for row in negative:
        lines.append(
            f"- `{row['target_answer_id']}` target `{row['target']}` prompt `{row['prompt_id']}` on `{row['model_surface']}`"
        )
    lines.extend(["", "## Mentioned Target Without Citation Authority", ""])
    if not low_citation:
        lines.append("No zero-citation-authority target mentions in this run.")
    for row in low_citation:
        lines.append(
            f"- `{row['target_answer_id']}` target `{row['target']}` prompt `{row['prompt_id']}` on `{row['model_surface']}`"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
