#!/usr/bin/env python3
"""Create one uploadable ZIP from the ChatGPT, Claude, and Gemini reports."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geo_benchmark.report_bundle import DEFAULT_RUN_DIRS, REQUIRED_PROVIDERS, create_report_bundle


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--month", required=True)
    parser.add_argument("--data-dir", action="append", dest="data_dirs",
                        help="Repeat for each run directory; defaults to the canonical directories")
    parser.add_argument("--output", type=Path, help="ZIP destination (default: reports/<month>/geo-benchmark-reports-<month>.zip)")
    parser.add_argument("--allow-partial", action="store_true",
                        help="Package available providers even when one of the three is missing")
    args = parser.parse_args()
    output = args.output or Path("reports") / args.month / f"geo-benchmark-reports-{args.month}.zip"
    try:
        create_report_bundle(args.month, [Path(name) for name in (args.data_dirs or DEFAULT_RUN_DIRS)],
                             output, set() if args.allow_partial else REQUIRED_PROVIDERS)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"Report ZIP: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
