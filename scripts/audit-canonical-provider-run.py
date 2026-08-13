#!/usr/bin/env python3
"""Audit a canonical provider run after raw collection, scoring, and reporting."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


TARGETS = {"CockroachDB", "TiDB", "YugabyteDB", "Neon", "Supabase", "PlanetScale"}
EXPECTED_ANSWERS = 120
EXPECTED_TARGET_ROWS = EXPECTED_ANSWERS * len(TARGETS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", required=True)
    parser.add_argument("--view", required=True)
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--web-search", choices=["on", "off"], required=True)
    parser.add_argument("--expected-model", required=True)
    args = parser.parse_args()

    root = Path(args.data_dir)
    raw_path = root / "runs" / args.month / "raw_answers.jsonl"
    scored_path = root / "runs" / args.month / "scored_answers.jsonl"
    report_path = root / "reports" / args.month / "llm-report.md"

    require_file(raw_path)
    require_file(scored_path)
    require_file(report_path)

    raw_rows = [
        row
        for row in read_jsonl(raw_path)
        if row.get("model_surface") == args.provider and row.get("web_search_mode", "off") == args.web_search
    ]
    scored_rows = [
        row
        for row in read_jsonl(scored_path)
        if row.get("model_surface") == args.provider and row.get("web_search_mode", "off") == args.web_search
    ]

    ok_raw = [row for row in raw_rows if row.get("status") == "ok"]
    error_raw = [row for row in raw_rows if row.get("status") != "ok"]

    failures: list[str] = []
    if len(raw_rows) != EXPECTED_ANSWERS:
        failures.append(f"expected {EXPECTED_ANSWERS} raw answers, got {len(raw_rows)}")
    if len(ok_raw) != EXPECTED_ANSWERS:
        failures.append(f"expected {EXPECTED_ANSWERS} ok raw answers, got {len(ok_raw)}")
    if error_raw:
        failures.append(f"found {len(error_raw)} raw error rows")
    if len(scored_rows) != EXPECTED_TARGET_ROWS:
        failures.append(f"expected {EXPECTED_TARGET_ROWS} scored target rows, got {len(scored_rows)}")

    raw_models = Counter(row.get("model_name") for row in ok_raw)
    scored_models = Counter(row.get("model_name") for row in scored_rows)
    if set(raw_models) != {args.expected_model}:
        failures.append(f"raw model mismatch: expected {args.expected_model}, got {dict(raw_models)}")
    if set(scored_models) != {args.expected_model}:
        failures.append(f"scored model mismatch: expected {args.expected_model}, got {dict(scored_models)}")

    prompt_ids = {row.get("prompt_id") for row in ok_raw}
    if len(prompt_ids) != EXPECTED_ANSWERS:
        failures.append(f"expected {EXPECTED_ANSWERS} unique prompts, got {len(prompt_ids)}")

    scored_targets = {row.get("target") for row in scored_rows}
    if scored_targets != TARGETS:
        failures.append(f"target mismatch: expected {sorted(TARGETS)}, got {sorted(scored_targets)}")

    groups: dict[str, list[dict[str, object]]] = {}
    for row in scored_rows:
        groups.setdefault(str(row.get("answer_id")), []).append(row)
    bad_groups = [answer_id for answer_id, rows in groups.items() if len(rows) != len(TARGETS)]
    if bad_groups:
        failures.append(f"{len(bad_groups)} scored answer groups do not have {len(TARGETS)} targets")

    web_search_calls = sum(int(row.get("web_search_requests") or 0) for row in ok_raw)
    if args.web_search == "off" and web_search_calls != 0:
        failures.append(f"web-search-off expected 0 web search calls, got {web_search_calls}")
    if args.web_search == "on" and web_search_calls <= 0:
        failures.append("web-search-on expected positive web search calls")

    print(f"Audit view: {args.view}")
    print(f"Raw answers: {len(raw_rows)}; ok: {len(ok_raw)}; errors: {len(error_raw)}")
    print(f"Scored target rows: {len(scored_rows)}")
    print(f"Raw models: {dict(raw_models)}")
    print(f"Scored models: {dict(scored_models)}")
    print(f"Web search calls: {web_search_calls}")
    print(f"Report: {report_path}")

    if failures:
        print("Audit failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Audit passed.")
    return 0


def require_file(path: Path) -> None:
    if not path.exists():
        raise SystemExit(
            f"Missing required file: {path}\n"
            "Raw answers are not committed to the repo. Run "
            "`VIEW=<view> ./scripts/run-canonical-provider-benchmark.sh` first."
        )


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


if __name__ == "__main__":
    raise SystemExit(main())
