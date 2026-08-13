#!/usr/bin/env python3
"""Generate canonical Executive KPI tables from committed scored outputs.

The script only supports four explicit views:

- anthropic-on
- openai-on
- anthropic-off
- openai-off

It reads committed `scored_answers.jsonl` files only. It does not read raw answers
and does not call provider APIs. This keeps team reruns consistent and prevents
accidental provider blending.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from geo_benchmark.scoring import aggregate_scores


VIEWS = {
    "anthropic-on": {
        "title": "Anthropic Web-On",
        "provider": "anthropic",
        "mode": "on",
        "path": ("geo-benchmark-websearch-on",),
        "expected_model": None,
    },
    "openai-on": {
        "title": "OpenAI Web-On",
        "provider": "openai",
        "mode": "on",
        "path": ("geo-benchmark-websearch-on",),
        "expected_model": "gpt-5-mini-2025-08-07",
    },
    "anthropic-off": {
        "title": "Anthropic Web-Off",
        "provider": "anthropic",
        "mode": "off",
        "path": ("geo-benchmark",),
        "expected_model": None,
    },
    "openai-off": {
        "title": "OpenAI Web-Off",
        "provider": "openai",
        "mode": "off",
        "path": ("geo-benchmark-openai",),
        "expected_model": None,
    },
}

DEFAULT_VIEW_ORDER = ["anthropic-on", "openai-on", "anthropic-off", "openai-off"]
TARGETS = ["CockroachDB", "TiDB", "YugabyteDB", "Neon", "Supabase", "PlanetScale"]
EXPECTED_TARGET_ROWS = 720
EXPECTED_PROMPTS = 120


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", default="2026-08")
    parser.add_argument(
        "--view",
        choices=["all", *VIEWS.keys()],
        default="all",
        help="Choose one canonical provider/mode view, or all four.",
    )
    parser.add_argument(
        "--comparison",
        choices=["all", "anthropic", "openai", "none"],
        default="all",
        help="Include provider-specific web-on vs web-off comparison sections.",
    )
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    selected = DEFAULT_VIEW_ORDER if args.view == "all" else [args.view]
    output = Path(args.output) if args.output else ROOT / "docs" / f"geo-benchmark-{args.month}-canonical-kpi.md"

    lines = [
        f"# GEO Benchmark {args.month} Canonical KPI",
        "",
        "Generated from committed scored outputs only. No raw answers are read and no provider APIs are called.",
        "",
        "Regenerate all four canonical views:",
        "",
        "```bash",
        f"python3 scripts/generate-canonical-kpi-report.py --month {args.month}",
        "```",
        "",
        "Generate one view:",
        "",
        "```bash",
        f"python3 scripts/generate-canonical-kpi-report.py --month {args.month} --view anthropic-on",
        "```",
        "",
        "Valid views: `anthropic-on`, `openai-on`, `anthropic-off`, `openai-off`.",
        "Valid comparisons: `anthropic`, `openai`, `all`, `none`.",
        "",
        "Guardrail: do not manually blend providers for executive readouts.",
        "",
        "## Input Audit",
        "",
        input_audit_table(args.month),
        "",
    ]

    for view in selected:
        spec = VIEWS[view]
        rows = load_view(args.month, spec)
        validate_view(view, spec, rows)
        lines.extend(
            [
                f"## {spec['title']}",
                "",
                f"View: `{view}`",
                f"Provider: `{spec['provider']}`",
                f"Web search mode: `{spec['mode']}`",
                f"Target-answer rows: `{len(rows)}`",
                "",
                executive_table(rows),
                "",
            ]
        )

    if args.comparison != "none":
        lines.extend(["## Provider On/Off Comparisons", ""])
        if args.comparison in {"all", "anthropic"}:
            lines.extend(comparison_section(args.month, "anthropic"))
        if args.comparison in {"all", "openai"}:
            lines.extend(comparison_section(args.month, "openai"))
        lines.extend(tidb_aeo_actions(args.month))

    output.write_text("\n".join(lines), encoding="utf-8")
    try:
        display_path = output.relative_to(ROOT)
    except ValueError:
        display_path = output
    print(f"Wrote {display_path}")
    return 0


def load_view(month: str, spec: dict[str, Any]) -> list[dict[str, Any]]:
    data_dir = ROOT.joinpath(*spec["path"])
    path = data_dir / "runs" / month / "scored_answers.jsonl"
    if not path.exists():
        raise SystemExit(f"Missing scored output: {path}")
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("model_surface") == spec["provider"] and row.get("web_search_mode", "off") == spec["mode"]:
            rows.append(row)
    return rows


def validate_view(view: str, spec: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    if len(rows) != EXPECTED_TARGET_ROWS:
        raise SystemExit(f"{view} expected {EXPECTED_TARGET_ROWS} target-answer rows, got {len(rows)}")
    prompts = {row["prompt_id"] for row in rows}
    if len(prompts) != EXPECTED_PROMPTS:
        raise SystemExit(f"{view} expected {EXPECTED_PROMPTS} prompts, got {len(prompts)}")
    targets = {row["target"] for row in rows}
    if targets != set(TARGETS):
        raise SystemExit(f"{view} target mismatch: {sorted(targets)}")
    expected_model = spec.get("expected_model")
    if expected_model:
        models = {row.get("model_name") for row in rows}
        if models != {expected_model}:
            raise SystemExit(f"{view} expected model {expected_model}, got {sorted(models)}")


def input_audit_table(month: str) -> str:
    lines = [
        "| View | Target-Answer Rows | Prompt Count | Model Distribution | Web Search Calls | Note |",
        "| --- | ---: | ---: | --- | ---: | --- |",
    ]
    for view in DEFAULT_VIEW_ORDER:
        spec = VIEWS[view]
        rows = load_view(month, spec)
        validate_view(view, spec, rows)
        model_counts = Counter(row.get("model_name") for row in rows)
        answer_ids = {}
        for row in rows:
            answer_ids.setdefault(row["answer_id"], row)
        answer_model_counts = Counter(row.get("model_name") for row in answer_ids.values())
        model_text = ", ".join(f"{model}: {count // 6} answers" for model, count in sorted(model_counts.items()))
        if len(answer_model_counts) > 1:
            model_text = ", ".join(f"{model}: {count} answers" for model, count in sorted(answer_model_counts.items()))
        note = "same model"
        if view == "openai-off" and len(answer_model_counts) > 1:
            note = "mixed fallback baseline; not strict same-model"
        elif view == "openai-on":
            note = "corrected same-model web-on"
        lines.append(
            f"| `{view}` | {len(rows)} | {len({row['prompt_id'] for row in rows})} | "
            f"{model_text} | {sum(int(row.get('web_search_requests') or 0) for row in answer_ids.values())} | {note} |"
        )
    return "\n".join(lines)


def executive_table(rows: list[dict[str, Any]]) -> str:
    targets = aggregate_scores(rows)["targets"]
    lines = [
        "| Target | Answer Share | Citation Authority | Recommendation Rate | Stable Answer Share | Stable Recommendation Rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for target in TARGETS:
        overall = targets[target]["overall"]
        stable = targets[target]["unchanged"]
        lines.append(
            f"| {target} | {overall['answer_share']:.2f} | {overall['citation_authority']:.2f} | "
            f"{overall['qualified_recommendation_rate']:.2f} | {stable['answer_share']:.2f} | "
            f"{stable['qualified_recommendation_rate']:.2f} |"
        )
    return "\n".join(lines)


def comparison_section(month: str, provider: str) -> list[str]:
    off_view = f"{provider}-off"
    on_view = f"{provider}-on"
    off_rows = load_view(month, VIEWS[off_view])
    on_rows = load_view(month, VIEWS[on_view])
    validate_view(off_view, VIEWS[off_view], off_rows)
    validate_view(on_view, VIEWS[on_view], on_rows)
    title = "Anthropic" if provider == "anthropic" else "OpenAI"
    subtitle = f"{title} Web-On vs Web-Off"
    note: list[str] = []
    if provider == "openai":
        off_models = {row.get("model_name") for row in off_rows}
        on_models = {row.get("model_name") for row in on_rows}
        if len(off_models) > 1 or off_models != on_models:
            subtitle += " (Off Baseline Uses Fallback)"
            note = [
                "",
                "Note: OpenAI web-on is all `gpt-5-mini-2025-08-07`, but OpenAI web-off contains 103 `gpt-5-mini-2025-08-07` answers and 17 `gpt-4o-mini-2024-07-18` fallback answers. Treat this as the current published baseline comparison, not a strict same-model comparison.",
            ]
    return [
        f"### {subtitle}",
        *note,
        "",
        "#### Overall",
        "",
        comparison_table(off_rows, on_rows, "overall"),
        "",
        "#### Stable Prompts",
        "",
        comparison_table(off_rows, on_rows, "unchanged"),
        "",
        "#### TiDB By Prompt Type",
        "",
        prompt_type_table(off_rows, on_rows, "TiDB"),
        "",
    ]


def comparison_table(off_rows: list[dict[str, Any]], on_rows: list[dict[str, Any]], slice_name: str) -> str:
    off = aggregate_scores(off_rows)["targets"]
    on = aggregate_scores(on_rows)["targets"]
    lines = [
        "| Target | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for target in TARGETS:
        old = off[target][slice_name]
        new = on[target][slice_name]
        lines.append(
            f"| {target} | {old['answer_share']:.2f} | {new['answer_share']:.2f} | {metric_delta(old['answer_share'], new['answer_share'])} | "
            f"{old['citation_authority']:.2f} | {new['citation_authority']:.2f} | {metric_delta(old['citation_authority'], new['citation_authority'])} | "
            f"{old['qualified_recommendation_rate']:.2f} | {new['qualified_recommendation_rate']:.2f} | "
            f"{metric_delta(old['qualified_recommendation_rate'], new['qualified_recommendation_rate'])} |"
        )
    return "\n".join(lines)


def prompt_type_table(off_rows: list[dict[str, Any]], on_rows: list[dict[str, Any]], target: str) -> str:
    off = aggregate_scores(off_rows)["targets"][target]["by_prompt_type"]
    on = aggregate_scores(on_rows)["targets"][target]["by_prompt_type"]
    lines = [
        "| Prompt Type | Off Answer Share | On Answer Share | Delta | Off Citation Authority | On Citation Authority | Delta | Off Recommendation Rate | On Recommendation Rate | Delta |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for prompt_type in sorted(off):
        old = off[prompt_type]
        new = on[prompt_type]
        lines.append(
            f"| {prompt_type} | {old['answer_share']:.2f} | {new['answer_share']:.2f} | {metric_delta(old['answer_share'], new['answer_share'])} | "
            f"{old['citation_authority']:.2f} | {new['citation_authority']:.2f} | {metric_delta(old['citation_authority'], new['citation_authority'])} | "
            f"{old['qualified_recommendation_rate']:.2f} | {new['qualified_recommendation_rate']:.2f} | "
            f"{metric_delta(old['qualified_recommendation_rate'], new['qualified_recommendation_rate'])} |"
        )
    return "\n".join(lines)


def metric_delta(old: float, new: float) -> str:
    return f"{new - old:+.2f}"


def tidb_aeo_actions(month: str) -> list[str]:
    provider_rows = {
        "Anthropic": {
            "off": load_view(month, VIEWS["anthropic-off"]),
            "on": load_view(month, VIEWS["anthropic-on"]),
        },
        "OpenAI": {
            "off": load_view(month, VIEWS["openai-off"]),
            "on": load_view(month, VIEWS["openai-on"]),
        },
    }
    provider_summaries = {
        provider: {
            mode: aggregate_scores(rows)["targets"]
            for mode, rows in modes.items()
        }
        for provider, modes in provider_rows.items()
    }
    tidb_on = {
        provider: summaries["on"]["TiDB"]["overall"]
        for provider, summaries in provider_summaries.items()
    }
    tidb_off = {
        provider: summaries["off"]["TiDB"]["overall"]
        for provider, summaries in provider_summaries.items()
    }
    deltas = {
        provider: {
            metric: tidb_on[provider][metric] - tidb_off[provider][metric]
            for metric in ["answer_share", "citation_authority", "qualified_recommendation_rate"]
        }
        for provider in provider_summaries
    }
    provider_priority = min(
        provider_summaries,
        key=lambda provider: tidb_on[provider]["answer_share"],
    )
    strongest_provider = max(
        provider_summaries,
        key=lambda provider: tidb_on[provider]["answer_share"],
    )
    weak_prompt = weakest_prompt_type(provider_summaries[provider_priority]["on"])
    largest_competitor_gap = competitor_gap(provider_summaries[provider_priority]["on"])
    citation_priority = min(
        provider_summaries,
        key=lambda provider: tidb_on[provider]["citation_authority"],
    )
    recommendation_priority = min(
        provider_summaries,
        key=lambda provider: tidb_on[provider]["qualified_recommendation_rate"],
    )

    return [
        "## Suggested Next Steps For TiDB AEO",
        "",
        "This section is regenerated from the latest scored outputs every time the canonical KPI report is generated.",
        "",
        f"1. Prioritize {provider_priority} visibility.",
        f"In {provider_priority} web-on, TiDB Answer Share is {tidb_on[provider_priority]['answer_share']:.2f}. The largest visible competitor gap is vs {largest_competitor_gap['target']} at {largest_competitor_gap['gap']:.2f} points. Build pages and snippets that answer the exact buying pains where TiDB should be first: scale-out SQL, MySQL compatibility, HTAP, operational analytics, AI application data, and vector search over fresh operational data.",
        "",
        f"2. Fix the weakest TiDB prompt type: `{weak_prompt['prompt_type']}`.",
        f"In {provider_priority} web-on, `{weak_prompt['prompt_type']}` has TiDB Answer Share {weak_prompt['answer_share']:.2f}, Citation Authority {weak_prompt['citation_authority']:.2f}, and Recommendation Rate {weak_prompt['recommendation_rate']:.2f}. Create use-case pages, docs examples, and comparison content specifically for this query family.",
        "",
        f"3. Raise {citation_priority} citation authority.",
        f"TiDB Citation Authority in {citation_priority} web-on is {tidb_on[citation_priority]['citation_authority']:.2f}. Publish citation-ready assets with current dates, official docs links, architecture diagrams, schema examples, customer proof, and clear claims that answer engines can quote directly.",
        "",
        f"4. Improve {recommendation_priority} recommendation language.",
        f"TiDB Recommendation Rate in {recommendation_priority} moved from {tidb_off[recommendation_priority]['qualified_recommendation_rate']:.2f} off to {tidb_on[recommendation_priority]['qualified_recommendation_rate']:.2f} on, a delta of {deltas[recommendation_priority]['qualified_recommendation_rate']:+.2f}. Add explicit 'choose TiDB when...' and 'when not to choose TiDB...' sections so models can recommend it conditionally instead of merely listing it.",
        "",
        f"5. Preserve what is working in {strongest_provider}.",
        f"{strongest_provider} web-on gives TiDB the strongest Answer Share at {tidb_on[strongest_provider]['answer_share']:.2f}. Use this as a pattern source: inspect high-scoring prompt types, then replicate that evidence structure and wording across lower-performing pages and provider surfaces.",
        "",
    ]


def weakest_prompt_type(targets: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for prompt_type, metrics in targets["TiDB"]["by_prompt_type"].items():
        score = (
            metrics["answer_share"]
            + metrics["citation_authority"]
            + metrics["qualified_recommendation_rate"]
        ) / 3
        rows.append(
            {
                "prompt_type": prompt_type,
                "score": score,
                "answer_share": metrics["answer_share"],
                "citation_authority": metrics["citation_authority"],
                "recommendation_rate": metrics["qualified_recommendation_rate"],
            }
        )
    return min(rows, key=lambda row: row["score"])


def competitor_gap(targets: dict[str, Any]) -> dict[str, Any]:
    tidb = targets["TiDB"]["overall"]["answer_share"]
    gaps = []
    for target in TARGETS:
        if target == "TiDB":
            continue
        gap = targets[target]["overall"]["answer_share"] - tidb
        gaps.append({"target": target, "gap": gap})
    return max(gaps, key=lambda row: row["gap"])


if __name__ == "__main__":
    raise SystemExit(main())
