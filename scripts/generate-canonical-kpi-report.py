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


if __name__ == "__main__":
    raise SystemExit(main())
