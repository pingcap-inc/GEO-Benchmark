import csv
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from geo_benchmark.report_bundle import create_report_bundle


class ReportBundleTests(unittest.TestCase):
    def test_one_archive_contains_each_provider_and_full_answers(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            roots = []
            for provider in ("openai", "anthropic", "gemini"):
                root = base / provider
                roots.append(root)
                reports = root / "reports/2026-09"
                reports.mkdir(parents=True)
                with (reports / "scored_answers.csv").open("w", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=["model_surface", "target", "answer_id"])
                    writer.writeheader()
                    writer.writerow({"model_surface": provider, "target": "TiDB", "answer_id": provider})
                (reports / "kpi_summary.json").write_text(json.dumps({"targets": {"TiDB": {}}}))
                (reports / "llm-report.md").write_text(f"# {provider}\n")
                (reports / "target-kpi-summary.csv").write_text("target,scope\nTiDB,overall\n")
                raw = root / "runs/2026-09/raw_answers.jsonl"
                raw.parent.mkdir(parents=True)
                raw.write_text(json.dumps({"raw_answer": provider}) + "\n")
            output = base / "reports/2026-09/all.zip"
            create_report_bundle("2026-09", roots, output)
            with zipfile.ZipFile(output) as archive:
                manifest = json.loads(archive.read("manifest.json"))
                self.assertEqual(len(manifest["runs"]), 3)
                self.assertEqual(manifest["targets"], ["TiDB"])
                for provider in ("openai", "anthropic", "gemini"):
                    self.assertIn(f"{provider}/reports/2026-09/llm-report.md", archive.namelist())
                    self.assertIn(f"{provider}/runs/2026-09/raw_answers.jsonl", archive.namelist())

    def test_missing_provider_does_not_write_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "all.zip"
            with self.assertRaisesRegex(ValueError, "Missing scored reports"):
                create_report_bundle("2026-09", [], output)
            self.assertFalse(output.exists())
