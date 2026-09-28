#!/usr/bin/env python3
"""Rescore saved provider answers offline after changing the target cohort.

Refuse to modify any report if a requested provider's raw answers are missing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geo_benchmark.cli import score_and_report
from geo_benchmark.io_utils import read_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--month", required=True)
    parser.add_argument("--data-dir", action="append", dest="data_dirs",
                        help="Repeat for each saved run directory; defaults to the four canonical directories")
    parser.add_argument("--require-providers", default="openai,anthropic,gemini")
    args = parser.parse_args()
    roots = [Path(name) for name in (args.data_dirs or [
        "geo-benchmark", "geo-benchmark-openai", "geo-benchmark-gemini",
        "geo-benchmark-websearch-on",
    ])]
    required = set(args.require_providers.split(",")) - {""}
    plan = []
    found = set()
    for root in roots:
        path = root / "runs" / args.month / "raw_answers.jsonl"
        if not path.is_file():
            continue
        raw = read_jsonl(path)
        if not raw:
            continue
        modes = {row.get("web_search_mode", "off") for row in raw}
        if len(modes) != 1 or not modes <= {"on", "off"}:
            parser.error(f"{path}: mixed or unsupported web search modes {modes}; split the run first")
        providers = {row.get("model_surface") for row in raw if row.get("status") == "ok"}
        found.update(providers)
        plan.append((root, modes.pop(), providers, len(raw)))
    missing = required - found
    if missing:
        parser.error(f"missing saved successful raw answers for: {', '.join(sorted(missing))}. "
                     "Restore raw_answers.jsonl in the run directories before rescoring; no reports were changed")
    if not plan:
        parser.error("no saved raw answers found; no reports were changed")
    for root, mode, providers, count in plan:
        print(f"Scoring {root}: {count} saved answers, {mode=}, providers={sorted(providers)}", flush=True)
        scored, _, _ = score_and_report(root, args.month, web_search_mode=mode)
        print(f"Wrote {len(scored)} target-answer rows to {root / 'reports' / args.month}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
