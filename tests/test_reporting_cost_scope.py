import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from geo_benchmark.cli import (
    load_previous_cost_summary,
    load_prompts,
    main,
    planned_cost,
    prepare,
)
from geo_benchmark.costs import estimate_actual_cost, estimate_planned_cost
from geo_benchmark.defaults import DEFAULT_MODELS, DEFAULT_PRICING
from geo_benchmark.io_utils import read_json, write_json
from geo_benchmark.scoring import aggregate_slice, score_answer
from geo_benchmark.reports import comparison_win_rate_text, fmt, format_cost


class ReportingCostScopeTests(unittest.TestCase):
    def test_comparison_rate_prints_denominator_and_low_sample_flag(self):
        self.assertEqual(
            comparison_win_rate_text({"target_win_rate": 50, "valid_comparison_answers": 4}),
            "50.00% (n = 4) — low sample",
        )
        self.assertEqual(
            comparison_win_rate_text({"target_win_rate": 45.45, "valid_comparison_answers": 11}),
            "45.45% (n = 11)",
        )

    def test_cost_history_carries_forward_from_latest_prior_month(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_json(
                root / "reports/2026-08/cost_summary.json",
                {
                    "providers": [
                        {
                            "provider": "gemini",
                            "requests": 2,
                            "output_tokens": 900,
                            "web_search_requests": 3,
                        }
                    ]
                },
            )
            history = load_previous_cost_summary(root, "2026-09")
        self.assertEqual(history["providers"][0]["provider"], "gemini")
        self.assertEqual(history["providers"][0]["web_search_requests"], 3)

    def test_filtered_run_and_estimate_use_same_selected_prompts_without_network(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()), patch(
            'socket.socket', side_effect=AssertionError('Network forbidden')
        ):
            prepare(Path(tmp), '2026-09', 10, 0.3, force=False)
            ids = ','.join(p['prompt_id'] for p in load_prompts(Path(tmp), '2026-09')[:2])
            self.assertEqual(main(['--data-dir', tmp, 'run', '--month', '2026-09',
                '--providers', 'mock', '--targets', 'TiDB', '--runs', '1',
                '--only-prompt-ids', ids, '--no-fallback']), 0)
            report = Path(tmp) / 'reports/2026-09'
            estimate = read_json(report / 'planned_cost_summary.json')
            self.assertEqual(estimate['prompt_count'], 2)
            self.assertEqual(estimate['providers'][0]['requests'], 2)
            self.assertEqual(read_json(report / 'cost_summary.json')['planned'], estimate)
            text = (report / 'llm-report.md').read_text()
            self.assertIn('2 prompts × 1 runs', text)
            self.assertIn('subset of the month', text)
            self.assertEqual(main(['--data-dir', tmp, 'estimate-cost', '--month', '2026-09',
                '--providers', 'openai', '--runs', '2', '--only-prompt-ids', ids]), 0)
            estimate = read_json(report / 'planned_cost_summary.json')
            self.assertEqual(estimate['providers'][0]['requests'], 4)
            empty = planned_cost(Path(tmp), '2026-09', ['mock'], 1, 700, prompt_ids=set())
            self.assertEqual(empty['prompt_count'], 0)

    def test_real_zero_differs_from_no_eligible_observations(self):
        prompt = {'prompt_id': 'p', 'prompt_text': 'Database for applications?',
                  'intent_weight': 1, 'qualified_recommendation_opportunity': False}
        raw = {'answer_id': 'a', 'raw_answer': 'PostgreSQL is an option.', 'prompt_id': 'p',
               'run_id': 'r', 'month': '2026-09', 'model_surface': 'mock', 'model_name': 'mock'}
        row = score_answer(raw, prompt, {}, {'targets': {}}, 'TiDB')
        measured = aggregate_slice([row])
        self.assertEqual(measured['mention_rate'], 0)
        self.assertEqual(measured['prominence_score'], 0)
        self.assertEqual(measured['visibility_answer_count'], 1)
        self.assertIsNone(measured['qualified_recommendation_rate'])
        self.assertIsNone(aggregate_slice([])['mention_rate'])
        self.assertEqual(fmt(None), 'N/A')
        self.assertEqual(fmt(0), '0.00')

    def test_unknown_pricing_never_looks_free_and_model_versions_resolve(self):
        usage = [{'status': 'ok', 'model_surface': 'openai', 'model_name': 'unpriced',
                  'input_tokens': 100, 'output_tokens': 100}]
        self.assertIsNone(estimate_actual_cost(usage, {'models': {}})['total_estimated_cost_usd'])
        planned = estimate_planned_cost([{'prompt_text': 'test'}], ['openai'], 1,
            {'openai': {'model': 'unpriced'}}, {'models': {}}, 100)
        self.assertIsNone(planned['total_estimated_cost_usd'])
        self.assertIn('Unknown', format_cost(None))
        model = DEFAULT_MODELS['openai']['model']
        usage[0]['model_name'] = model + '-2026-09-01'
        self.assertIsNotNone(estimate_actual_cost(usage, DEFAULT_PRICING)['total_estimated_cost_usd'])
