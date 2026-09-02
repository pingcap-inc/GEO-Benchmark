#!/usr/bin/env python3
"""
Convert the Core Monitoring Set (from the Google Sheet) into geo-bench prompts.json.

Input : rows.tsv  — tab-separated, one row per prompt, columns:
        rank, prompt_text, branded, cluster, funnel_stage, icp, score
Output: prompts.json          — the file geo-bench reads
        prompt_set_hash.txt    — fingerprint proving the set has not changed
        prompts_review.csv     — flat view for eyeballing the tagging in Sheets

Usage:
    python3 build_prompts.py
    python3 build_prompts.py --month 2026-09 --out-dir geo-benchmark/prompts/2026-09
"""

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------- tagging rules

# Short codes used in prompt_id. Frozen: changing these breaks month-over-month
# comparison, because prompt_id is the join key across runs.
CLUSTER_CODES = {
    "AI Agent Infrastructure": "agentinfra",
    "Hybrid Search & RAG": "hybridrag",
    "Competitive Comparisons": "compcomp",
    "MySQL Scale & Migration": "mysqlscale",
    "MCP & Developer Tooling": "mcptooling",
    "Scale & Architecture": "scalearch",
    "Deployment & Cloud": "deploycloud",
    "Enterprise & Compliance": "entcomp",
    "Observability": "observ",
    "TiDB Brand & Definitions": "branddef",
}

# Products launched or renamed in the last year. Questions naming these run
# against the real ChatGPT and Gemini apps, because testing showed the developer
# API and the real app contradict each other on new names.
# Example: asked what TiDB Cloud Zero is, the API described it correctly while
# the real app said it was probably a feature of TiDB Cloud Starter.
RECENT_PRODUCTS = [
    "cloud zero",
    "cloud starter",
    "cloud essential",
    "cloud premium",
    "tidb x",
    "mem9",
    "drive9",              # retired name, kept so old-name questions still route correctly
    "tidb cloud filesystem",  # current name for drive9
]

# Phrasings that make a question a head-to-head comparison.
COMPARISON_MARKERS = [
    r"\bvs\.?\b",
    r"\bversus\b",
    r"\bcompare[ds]?\b",
    r"\bwhich is better\b",
    r"\binstead of\b",
    r"\breplace\b",
    r"\balternative to\b",
]

FUNNEL_WEIGHT = {"Decision": 3, "Consideration": 2, "Awareness": 2}


def classify_group(prompt_text: str, branded: str) -> str:
    """discovery | accuracy | comparison

    Non-branded questions measure whether we are found, so they are discovery.
    Branded questions split on whether they set us against a named rival.
    """
    if branded.strip().lower() == "non-branded":
        return "discovery"
    lower = prompt_text.lower()
    if any(re.search(p, lower) for p in COMPARISON_MARKERS):
        return "comparison"
    return "accuracy"


def classify_surface(prompt_text: str) -> str:
    """api | product

    Only questions naming a recently launched or renamed product need the real
    apps. Established components (TiKV, TiFlash, hybrid search) agreed across
    both surfaces in testing, so they stay on the cheaper developer API.
    """
    lower = prompt_text.lower()
    return "product" if any(p in lower for p in RECENT_PRODUCTS) else "api"


def stable_hash(payload) -> str:
    """Fingerprint of the exact prompt set. Changes if any prompt changes."""
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


# ---------------------------------------------------------------- build

def build(rows, month: str):
    prompts = []
    per_cluster = Counter()
    seen_text = {}

    for rank, text, branded, cluster, funnel, icp, score in rows:
        text = text.strip()
        cluster = cluster.strip()
        funnel = funnel.strip()

        if cluster not in CLUSTER_CODES:
            raise SystemExit(f"Unknown cluster on row {rank}: {cluster!r}")
        if funnel not in FUNNEL_WEIGHT:
            raise SystemExit(f"Unknown funnel stage on row {rank}: {funnel!r}")

        # Duplicate detection: same wording twice would double-count in scoring.
        key = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
        if key in seen_text:
            print(f"  ! duplicate wording: row {rank} matches row {seen_text[key]}")
        else:
            seen_text[key] = rank

        code = CLUSTER_CODES[cluster]
        per_cluster[code] += 1
        prompt_id = f"stable_{code}_{per_cluster[code]:03d}"

        group = classify_group(text, branded)
        surface = classify_surface(text)

        prompts.append({
            "prompt_id": prompt_id,
            "prompt_text": text,
            "prompt_type": cluster,
            "group": group,
            "surface": surface,
            "brand_class": "non_branded" if group == "discovery" else "branded",
            "funnel_stage": funnel.lower(),
            "persona": icp.strip(),
            "region": "US",
            "use_case": code,
            "intent_weight": FUNNEL_WEIGHT[funnel],
            "qualified_recommendation_opportunity": group != "accuracy",
            "competitors": [],
            "panel": "stable",
            "priority_score": int(score),
            "source": {
                "source_type": "manual_curated",
                "validation_status": "case_pattern_validated",
                "source_evidence_urls": [
                    "https://docs.google.com/spreadsheets/d/"
                    "12tyuVZkSQeK4mlSjrVn5abpOKdj7pyEHTSyCc0-3MoA"
                ],
                "collected_at": f"{month}-01",
                "sheet_rank": int(rank),
            },
        })

    return prompts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", default="2026-09")
    ap.add_argument("--tsv", default="rows.tsv")
    ap.add_argument("--out-dir", default=".")
    args = ap.parse_args()

    rows = []
    with open(args.tsv, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 7:
                raise SystemExit(f"Expected 7 columns, got {len(parts)}: {line[:80]}")
            rows.append(parts)

    print(f"Read {len(rows)} rows from {args.tsv}\n")
    prompts = build(rows, args.month)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    (out / "prompts.json").write_text(json.dumps(prompts, indent=2) + "\n")
    (out / "prompt_set_hash.txt").write_text(stable_hash(prompts) + "\n")

    with open(out / "prompts_review.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["prompt_id", "group", "surface", "cluster", "funnel_stage",
                    "intent_weight", "persona", "score", "prompt_text"])
        for p in prompts:
            w.writerow([p["prompt_id"], p["group"], p["surface"], p["prompt_type"],
                        p["funnel_stage"], p["intent_weight"], p["persona"],
                        p["priority_score"], p["prompt_text"]])

    # ------------------------------------------------------------ summary
    g = Counter(p["group"] for p in prompts)
    s = Counter(p["surface"] for p in prompts)
    fs = Counter(p["funnel_stage"] for p in prompts)

    print("Groups:")
    for k in ("discovery", "accuracy", "comparison"):
        print(f"  {k:12} {g[k]:4}")
    print("\nSurface:")
    for k in ("api", "product"):
        print(f"  {k:12} {s[k]:4}")
    print("\nFunnel stage:")
    for k, v in fs.most_common():
        print(f"  {k:14} {v:4}")
    print("\nCluster:")
    for cluster, code in CLUSTER_CODES.items():
        n = sum(1 for p in prompts if p["prompt_type"] == cluster)
        print(f"  {cluster:28} {n:4}")

    runs, platforms = 5, 4
    print(f"\nMonthly volume: {len(prompts)} x {platforms} platforms x {runs} runs "
          f"= {len(prompts)*platforms*runs:,} answers")
    print(f"\nWrote {out/'prompts.json'}")
    print(f"Wrote {out/'prompt_set_hash.txt'}")
    print(f"Wrote {out/'prompts_review.csv'}  <- open this in Sheets to check tagging")


if __name__ == "__main__":
    main()
