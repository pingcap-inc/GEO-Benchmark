import csv
import tempfile
import unittest
from pathlib import Path

from geo_benchmark.cli import load_prompts
from geo_benchmark.reports import cluster_coverage_warnings, write_cluster_coverage_csv
from geo_benchmark.scoring import cluster_coverage, product_in_prompt


class ClusterCoverageTests(unittest.TestCase):
    def test_september_tidb_low_coverage_clusters_match_effective_metadata(self):
        root = Path(__file__).resolve().parents[1] / "geo-benchmark"
        prompts = load_prompts(root, "2026-09")
        rows = [
            {
                "prompt_id": prompt["prompt_id"],
                "prompt_type": prompt["prompt_type"],
                "target_in_prompt": product_in_prompt(prompt, "TiDB"),
            }
            for prompt in prompts
        ]
        coverage = cluster_coverage(rows, 3)
        low = {
            cluster: values["non_branded_prompt_count"]
            for cluster, values in coverage.items()
            if values["below_minimum"]
        }
        self.assertEqual(
            low,
            {
                "Competitive Comparisons": 1,
                "Deployment & Cloud": 0,
                "Enterprise & Compliance": 2,
                "Observability": 0,
                "TiDB Brand & Definitions": 0,
            },
        )

    def test_warnings_explain_zero_and_below_minimum_coverage(self):
        summary = {
            "target_order": ["TiDB"],
            "targets": {
                "TiDB": {
                    "cluster_coverage": {
                        "Deployment & Cloud": {
                            "non_branded_prompt_count": 0,
                            "minimum_non_branded_prompts": 3,
                            "below_minimum": True,
                        },
                        "Enterprise & Compliance": {
                            "non_branded_prompt_count": 2,
                            "minimum_non_branded_prompts": 3,
                            "below_minimum": True,
                        },
                    }
                }
            },
        }
        warnings = cluster_coverage_warnings(summary)
        self.assertIn("visibility KPIs are N/A by design", warnings[0])
        self.assertIn("below the configured minimum of 3", warnings[1])

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cluster-coverage.csv"
            write_cluster_coverage_csv(path, summary)
            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["non_branded_prompt_count"], "0")


if __name__ == "__main__":
    unittest.main()
