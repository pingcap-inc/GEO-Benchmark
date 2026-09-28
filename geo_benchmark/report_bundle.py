"""Package saved benchmark reports from multiple model runs into one ZIP."""

from __future__ import annotations

import csv
import json
import zipfile
from pathlib import Path

DEFAULT_RUN_DIRS = (
    "geo-benchmark", "geo-benchmark-openai", "geo-benchmark-gemini",
    "geo-benchmark-websearch-on",
)
REQUIRED_PROVIDERS = {"openai", "anthropic", "gemini"}


def create_report_bundle(
    month: str,
    roots: list[Path],
    output: Path,
    required_providers: set[str] = REQUIRED_PROVIDERS,
) -> Path:
    """Build an archive only after all requested providers have scored results."""
    runs = []
    for root in roots:
        report_dir = root / "reports" / month
        scored_path = report_dir / "scored_answers.csv"
        summary_path = report_dir / "kpi_summary.json"
        if not scored_path.is_file() or not summary_path.is_file():
            continue
        for required_file in ("llm-report.md", "target-kpi-summary.csv"):
            if not (report_dir / required_file).is_file():
                raise ValueError(f"{report_dir}: missing {required_file}; regenerate this report first")
        with scored_path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            continue
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        providers = sorted({row["model_surface"] for row in rows})
        targets = set(summary.get("targets", {}))
        if not targets:
            raise ValueError(f"{summary_path}: no scored targets")
        if {row["target"] for row in rows} != targets:
            raise ValueError(f"{scored_path}: scored targets differ from the KPI summary")
        cost_path = report_dir / "cost_summary.json"
        cost = json.loads(cost_path.read_text(encoding="utf-8")) if cost_path.is_file() else {}
        mode = cost.get("web_search_mode", "unknown")
        runs.append((root, report_dir, providers, targets, mode, rows))

    found = {provider for _, _, providers, _, _, _ in runs for provider in providers}
    missing = required_providers - found
    if missing:
        raise ValueError(
            f"Missing scored reports for {', '.join(sorted(missing))} in {month}; "
            "no ZIP was created. Run or rescore those providers first."
        )
    if not runs:
        raise ValueError(f"No scored reports found for {month}; no ZIP was created")
    target_sets = {frozenset(targets) for _, _, _, targets, _, _ in runs}
    if len(target_sets) != 1:
        raise ValueError("Run reports have different competitor sets; rescore all providers first")
    names = [root.name for root, *_ in runs]
    if len(names) != len(set(names)):
        raise ValueError("Run directory names must be distinct in the ZIP")

    index = [
        f"# GEO benchmark reports: {month}", "",
        "Start with each run's `llm-report.md` and `target-kpi-summary.csv`.",
        "`scored_answers.csv` contains answer-level scores; `raw_answers.jsonl`",
        "contains full model responses when available. Each run is kept in its",
        "own directory so search-on and search-off results remain distinct.", "",
        "| Run directory | Providers | Search | Targets | Scored answers |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    manifest = {"month": month, "targets": sorted(next(iter(target_sets))), "runs": []}
    for root, _, providers, targets, mode, rows in runs:
        count = len({row["answer_id"] for row in rows})
        index.append(f"| {root.name} | {', '.join(providers)} | {mode} | {len(targets)} | {count} |")
        manifest["runs"].append({"directory": root.name, "providers": providers,
                                 "web_search_mode": mode, "targets": len(targets),
                                 "scored_answers": count})
    index.extend(["", "Generated from saved scores; no provider calls were made.", ""])

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("README.md", "\n".join(index))
            archive.writestr("manifest.json", json.dumps(manifest, indent=2) + "\n")
            for root, report_dir, _, _, _, _ in runs:
                for path in sorted(report_dir.iterdir()):
                    if path.is_file() and path.suffix.lower() in {".csv", ".json", ".md", ".html"}:
                        archive.write(path, f"{root.name}/reports/{month}/{path.name}")
                raw = root / "runs" / month / "raw_answers.jsonl"
                if raw.is_file():
                    archive.write(raw, f"{root.name}/runs/{month}/raw_answers.jsonl")
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    return output
