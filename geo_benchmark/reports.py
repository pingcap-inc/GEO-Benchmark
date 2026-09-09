from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .io_utils import ensure_dir, write_json
from .review_report import write_review_report


PROMPT_TYPE_ORDER = ["pain_point", "database_type", "ai_infra", "case_selection"]
TARGET_DISPLAY_ORDER = ["CockroachDB", "TiDB", "YugabyteDB", "Neon", "Supabase", "PlanetScale"]


def write_reports(
    report_dir: Path,
    month: str,
    summary: dict[str, Any],
    scored_answers: list[dict[str, Any]],
    cost_summary: dict[str, Any] | None,
    raw_answers: list[dict[str, Any]] | None = None,
    fact_base: dict[str, Any] | None = None,
) -> None:
    ensure_dir(report_dir)
    cleanup_legacy_single_target_files(report_dir)
    write_json(report_dir / "kpi_summary.json", summary)
    if cost_summary:
        write_json(report_dir / "cost_summary.json", cost_summary)
    write_markdown(report_dir / "llm-report.md", month, summary, cost_summary, scored_answers)
    write_target_summary_csv(report_dir / "target-kpi-summary.csv", summary)
    write_csv(report_dir / "scored_answers.csv", scored_answers)
    write_review_report(report_dir, month, scored_answers, raw_answers or [], fact_base)
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
    branded_table = branded_accuracy_table(summary)
    if branded_table:
        lines.extend(["", "## Branded Accuracy", ""])
        lines.extend(branded_table)
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

    lines.extend(
        [
            "",
            "## Coverage",
            "",
            "| Target | Non-branded prompts | Branded prompts | Target-answer rows |",
            "| --- | ---: | ---: | ---: |",
            *[
                f"| {target} | {summary['targets'][target]['overall']['prompt_count']} | "
                f"{summary['targets'][target]['overall'].get('branded_prompt_count', 0)} | "
                f"{summary['targets'][target]['overall']['answer_count']} |"
                for target in report_target_order(summary)
            ],
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
                f"- Fact judge mode: {cost_summary.get('fact_judge', {}).get('mode', 'off')}",
                f"- Fact judge estimated cost: {format_cost(cost_summary.get('fact_judge', {}).get('estimated_cost_usd', 0))}",
                f"- Combined provider and judge cost: {format_cost(cost_summary.get('combined_total_estimated_cost_usd', cost_summary.get('total_estimated_cost_usd', 0)))}",
                "",
            ]
        )
    metadata = summary.get("run_metadata", {})
    if metadata:
        lines.extend(
            [
                "## Run Metadata",
                "",
                f"- Prompt set hash: `{metadata.get('prompt_set_hash')}`",
                f"- Legacy facts version: `{metadata.get('legacy_facts_version')}`",
                f"- Semantic fact-base version: `{metadata.get('fact_base_version')}`",
                f"- Source-authority version: `{metadata.get('source_authority_version')}`",
                f"- Models config hash: `{metadata.get('models_config_hash')}`",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def executive_kpi_table(summary: dict[str, Any]) -> list[str]:
    lines = [
        "| Target | Consideration Rate | Mention Rate | Prominence Score | Citation Authority | Recommendation Rate | Comparison Win Rate | Stable Consideration Rate | Stable Mention Rate | Stable Prominence Score | Stable Recommendation Rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for target in report_target_order(summary):
        metrics = summary["targets"][target]
        lines.append(
            "| "
            + " | ".join(
                [
                    target,
                    fmt_optional(metrics["overall"].get("consideration_rate")),
                    fmt_optional(metrics["overall"].get("mention_rate")),
                    fmt(metric_value(metrics["overall"], "prominence_score", "answer_share")),
                    fmt(metrics["overall"].get("citation_authority")),
                    fmt(metrics["overall"].get("qualified_recommendation_rate")),
                    fmt_optional(metrics.get("competitive", {}).get("target_win_rate")),
                    fmt_optional(metrics["unchanged"].get("consideration_rate")),
                    fmt_optional(metrics["unchanged"].get("mention_rate")),
                    fmt(metric_value(metrics["unchanged"], "prominence_score", "answer_share")),
                    fmt(metrics["unchanged"].get("qualified_recommendation_rate")),
                ]
            )
            + " |"
        )
    return lines


def format_cost(value: Any) -> str:
    return "Unknown (missing pricing)" if value is None else f"${value}"


def branded_accuracy_table(summary: dict[str, Any]) -> list[str]:
    rows = []
    for target in report_target_order(summary):
        metrics = summary["targets"][target]["overall"]
        if not metrics.get("branded_prompt_count"):
            continue
        rows.append(
            "| "
            + " | ".join(
                [
                    target,
                    str(metrics.get("branded_prompt_count", 0)),
                    fmt_optional(metrics.get("brand_accuracy")),
                    fmt_percentage(metrics.get("brand_accuracy_coverage")),
                    fmt_optional(metrics.get("semantic_brand_accuracy")),
                    fmt_percentage(metrics.get("semantic_brand_accuracy_coverage")),
                    str(metrics.get("semantic_brand_unavailable_facts", 0)),
                ]
            )
            + " |"
        )
    if not rows:
        return []
    return [
        "| Target | Prompts | Legacy accuracy | Legacy coverage | Semantic accuracy | Semantic decision coverage | Judge unavailable |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        *rows,
        "",
        "Semantic results are written alongside legacy substring scores; they do not replace the official metric during shadow mode.",
    ]


def report_target_order(summary: dict[str, Any]) -> list[str]:
    present = set(summary.get("target_order", []))
    ordered = [target for target in TARGET_DISPLAY_ORDER if target in present]
    ordered.extend(sorted(present - set(ordered)))
    return ordered


def prompt_type_metric_tables(summary: dict[str, Any]) -> list[str]:
    tables: list[str] = []
    for title, metric_key in [
        ("Consideration Rate", "consideration_rate"),
        ("Mention Rate", "mention_rate"),
        ("Prominence Score", "prominence_score"),
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
            formatter = fmt_optional if metric_key in {"consideration_rate", "mention_rate"} else fmt
            value = (
                metric_value(metrics, "prominence_score", "answer_share")
                if metric_key == "prominence_score"
                else metrics.get(metric_key)
            )
            cells.append(formatter(value))
        lines.append(f"| `{prompt_type}` | " + " | ".join(cells) + " |")
    return lines


def prompt_type_leaders_table(summary: dict[str, Any]) -> list[str]:
    prompt_types = ordered_prompt_types(summary)
    lines = [
        "| Prompt Type | Prominence Leader | Citation Authority Leader | Recommendation Leader |",
        "| --- | --- | --- | --- |",
    ]
    for prompt_type in prompt_types:
        metric_leaders = []
        for metric_key in ["prominence_score", "citation_authority", "qualified_recommendation_rate"]:
            values: list[tuple[str, float]] = []
            for target in summary.get("target_order", []):
                metrics = summary["targets"][target].get("by_prompt_type", {}).get(prompt_type, {})
                value = metric_value(metrics, metric_key, "answer_share") if metric_key == "prominence_score" else metrics.get(metric_key, 0)
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


def fmt_optional(value: Any) -> str:
    if value is None:
        return "N/A"
    return f"{float(value):.2f}"


def fmt_percentage(value: Any) -> str:
    if value is None:
        return "N/A"
    return f"{float(value) * 100:.2f}%"


def metric_value(metrics: dict[str, Any], key: str, fallback: str) -> Any:
    """Read a renamed metric while supporting summaries from older runs."""
    value = metrics.get(key)
    return metrics.get(fallback) if value is None else value


def write_target_summary_csv(path: Path, summary: dict[str, Any]) -> None:
    fieldnames = [
        "target",
        "scope",
        "mention_rate",
        "prominence_score",
        "answer_share",
        "consideration_rate",
        "consideration_coverage",
        "consideration_prompt_count",
        "consideration_answer_count",
        "avg_fan_out_queries",
        "citation_authority",
        "qualified_recommendation_rate",
        "comparison_win_rate",
        "valid_comparison_answers",
        "weighted_recommendation_score",
        "negative_recommendation_rate",
        "avg_source_authority",
        "avg_accuracy",
        "branded_prompt_count",
        "brand_accuracy",
        "brand_accuracy_coverage",
        "brand_citation_rate",
        "semantic_brand_accuracy",
        "semantic_brand_accuracy_coverage",
        "semantic_brand_selected_facts",
        "semantic_brand_unavailable_facts",
        "semantic_brand_not_enough_information_facts",
        "avg_freshness",
        "prompt_count",
        "answer_count",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for target in summary.get("target_order", []):
            for scope in ["overall", "unchanged"]:
                metrics = summary["targets"][target][scope]
                competitive = summary["targets"][target].get("competitive", {})
                writer.writerow(
                    {
                        "target": target,
                        "scope": scope,
                        **{key: metrics.get(key) for key in fieldnames if key not in {"target", "scope"}},
                        "prominence_score": metric_value(metrics, "prominence_score", "answer_share"),
                        "comparison_win_rate": competitive.get("target_win_rate") if scope == "overall" else None,
                        "valid_comparison_answers": competitive.get("valid_comparison_answers") if scope == "overall" else None,
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
        "group",
        "use_case",
        "target_in_prompt",
        "fan_out_queries",
        "fan_out_query_count",
        "fan_out_status",
        "consideration_eligible",
        "considered_in_fan_out",
        "mentioned_target",
        "presence_score",
        "mention_position",
        "citation_authority_answer",
        "source_authority",
        "accuracy",
        "accuracy_checked_facts",
        "accuracy_correct_facts",
        "semantic_fact_accuracy",
        "semantic_checked_facts",
        "semantic_correct_facts",
        "semantic_incorrect_facts",
        "semantic_not_enough_information_facts",
        "semantic_unavailable_facts",
        "freshness",
        "recommendation_class",
        "recommendation_score",
        "competitive_winner",
        "comparison_products",
        "input_tokens",
        "output_tokens",
        "prompt_set_hash",
        "legacy_facts_version",
        "fact_base_version",
        "source_authority_version",
        "models_config_hash",
        "fact_judge_mode",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            output = {key: row.get(key) for key in fieldnames}
            metadata = row.get("run_metadata", {})
            for key in [
                "prompt_set_hash",
                "legacy_facts_version",
                "fact_base_version",
                "source_authority_version",
                "models_config_hash",
                "fact_judge_mode",
            ]:
                output[key] = metadata.get(key)
            writer.writerow(output)


def write_breakdown_csv(path: Path, breakdown: dict[str, Any]) -> None:
    fieldnames = [
        "segment",
        "prompt_count",
        "answer_count",
        "mention_rate",
        "prominence_score",
        "answer_share",
        "consideration_rate",
        "consideration_coverage",
        "consideration_answer_count",
        "citation_authority",
        "qualified_recommendation_rate",
        "negative_recommendation_rate",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for segment, metrics in breakdown.items():
            writer.writerow(
                {
                    "segment": segment,
                    **{key: metrics.get(key) for key in fieldnames if key != "segment"},
                    "prominence_score": metric_value(metrics, "prominence_score", "answer_share"),
                }
            )


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
