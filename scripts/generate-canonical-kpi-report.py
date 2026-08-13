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
    return [
        f"### {title} Web-On vs Web-Off",
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
    anthropic_off = aggregate_scores(load_view(month, VIEWS["anthropic-off"]))["targets"]["TiDB"]
    anthropic_on = aggregate_scores(load_view(month, VIEWS["anthropic-on"]))["targets"]["TiDB"]
    openai_off = aggregate_scores(load_view(month, VIEWS["openai-off"]))["targets"]["TiDB"]
    openai_on = aggregate_scores(load_view(month, VIEWS["openai-on"]))["targets"]["TiDB"]

    return [
        "## Suggested Next Steps For TiDB AEO",
        "",
        "1. Strengthen OpenAI-facing discoverability for pain-point and database-type queries.",
        f"OpenAI web-on lowers TiDB Answer Share in `pain_point` and `database_type` prompts, while Anthropic web-on improves TiDB strongly. Build concise public pages that map buyer pains to TiDB-fit language: scale-out SQL, MySQL compatibility, HTAP, operational analytics, AI application data, and vector search with transactional data.",
        "",
        "2. Create citation-ready comparison and use-case pages.",
        f"TiDB Citation Authority is much stronger in Anthropic web-on ({anthropic_on['overall']['citation_authority']:.2f}) than OpenAI web-on ({openai_on['overall']['citation_authority']:.2f}). Publish pages with clear claims, current dates, source links, schema examples, and comparison tables for TiDB vs CockroachDB, YugabyteDB, Aurora, Neon, Supabase, and PlanetScale.",
        "",
        "3. Improve recommendation language around exact-fit scenarios.",
        f"Anthropic Recommendation Rate moves from {anthropic_off['overall']['qualified_recommendation_rate']:.2f} to {anthropic_on['overall']['qualified_recommendation_rate']:.2f}, but OpenAI moves from {openai_off['overall']['qualified_recommendation_rate']:.2f} to {openai_on['overall']['qualified_recommendation_rate']:.2f}. Add explicit 'choose TiDB when...' sections for real-time operational analytics, high-write transactional workloads, MySQL scale-out, and hybrid transactional plus analytical workloads.",
        "",
        "4. Add serverless AI positioning without forcing PostgreSQL framing.",
        "For AI infrastructure prompts, TiDB still trails Neon and Supabase in OpenAI. Create TiDB Serverless AI pages and examples around agent state, RAG over fresh operational data, vector search with SQL filters, and transactional metadata at scale.",
        "",
        "5. Make customer proof easier for answer engines to quote.",
        "Package customer stories into structured, crawlable pages with industry, workload, before/after pain, architecture, measurable outcome, and links to docs. The benchmark case-selection prompts reward concrete use-case proof more than generic product messaging.",
        "",
    ]


if __name__ == "__main__":
    raise SystemExit(main())
