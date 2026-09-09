"""Controlled scope checks. Preview is keyless; --live explicitly enables paid calls."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .cli import load_env_files
from .fact_judge import JudgeSettings, SemanticFactJudge
from .io_utils import stable_hash


CASES = [
    {"case": "core_only", "question": "What is TiDB Cloud Zero?",
     "answer": "TiDB Cloud Zero provisions an on-demand temporary TiDB database for experimentation and AI agents.", "expected": "correct"},
    {"case": "unrequested_preview_omitted", "question": "What is TiDB Cloud Zero?",
     "answer": "TiDB Cloud Zero provisions a temporary TiDB database without signup for trying applications.", "expected": "correct"},
    {"case": "requested_maturity_answered", "question": "Is TiDB Cloud Zero generally available or in public preview?",
     "answer": "TiDB Cloud Zero is in public preview.", "expected": "correct"},
    {"case": "requested_maturity_missing", "question": "Is TiDB Cloud Zero generally available or in public preview?",
     "answer": "It provisions a temporary database for experimentation.", "expected": "not_enough_information"},
    {"case": "volunteered_false_maturity", "question": "What is TiDB Cloud Zero?",
     "answer": "TiDB Cloud Zero provisions temporary TiDB databases. It is generally available.", "expected": "incorrect"},
    {"case": "false_core_claim", "question": "What is TiDB Cloud Zero?",
     "answer": "TiDB Cloud Zero gives you a permanent database from creation, with no claim step needed.", "expected": "incorrect"},
    {"case": "plan_does_not_require_maturity", "question": "What is TiDB Cloud Zero?",
     "answer": "TiDB Cloud Zero provisions temporary TiDB databases for experimentation. Claiming one converts it to a persistent Starter instance with its schema and data.", "expected": "correct"},
    {"case": "unclear_core", "question": "What is TiDB Cloud Zero?",
     "answer": "It is a cloud product for developers.", "expected": "not_enough_information"},
]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Make paid OpenAI judge calls for these eight fixed cases.")
    parser.add_argument("--data-dir", default="geo-benchmark-qualifier-check")
    args = parser.parse_args(argv)
    if not args.live:
        print(json.dumps({"mode": "preview", "api_calls": 0, "cases": CASES}, indent=2))
        return 0
    load_env_files([Path.cwd(), Path(__file__).resolve().parents[1]])
    if not os.getenv("OPENAI_API_KEY"):
        parser.error("Set OPENAI_API_KEY in .env.local before using --live.")
    judge = SemanticFactJudge(Path(args.data_dir), "2026-09", JudgeSettings(mode="live", retries=0))
    if judge.facts["tidb_cloud_zero"].get("status") != "READY_FOR_JUDGE":
        parser.error("Cloud Zero must be READY_FOR_JUDGE to run these checks.")
    results = []
    for case in CASES:
        result = judge.judge_answer(
            {"prompt_id": "stable_branddef_022", "prompt_text": case["question"]},
            case["answer"], stable_hash(case["answer"]),
        )
        verdict = next((r for r in result["results"] if r["fact_id"] == "tidb_cloud_zero"), {})
        results.append({**case, "actual": verdict.get("verdict"),
                        "matched": verdict.get("verdict") == case["expected"], "judgment": verdict})
        judge.flush_cache()
    print(json.dumps({"mode": "live", "api_calls": judge.usage.calls,
                      "cache_hits": judge.usage.cache_hits, "results": results}, indent=2))
    return 0 if all(r["matched"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
