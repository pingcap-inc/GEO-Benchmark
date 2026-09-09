import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from geo_benchmark.reports import write_reports


class ReviewReportTests(unittest.TestCase):
    def test_saved_evidence_join_and_safe_offline_rendering(self):
        raw = [
            {'answer_id': 'a', 'prompt_id': 'same', 'prompt_text': 'Question A',
             'raw_answer': '<script>alert(1)</script> full answer', 'status': 'ok',
             'raw_citations': ['https://example.com/a', 'javascript:alert(1)'],
             'fan_out_queries': ['query A']},
            {'answer_id': 'b', 'prompt_id': 'same', 'prompt_text': 'Question B',
             'status': 'error', 'error': 'Timed out'},
        ]
        scored = [{'answer_id': 'a', 'target': 'TiDB', 'target_in_prompt': True,
                   'semantic_fact_judge': {'coverage_disposition': 'fact_covered',
                     'results': [{'fact_id': 'f', 'verdict': 'correct', 'reason': 'Reason A'}]}},
                  {'answer_id': 'a', 'target': 'Other', 'target_in_prompt': False},
                  {'answer_id': 'missing', 'prompt_id': 'missing', 'target': 'TiDB'}]
        with tempfile.TemporaryDirectory() as tmp, patch('socket.socket', side_effect=AssertionError('Network forbidden')):
            root = Path(tmp)
            write_reports(root, '2026-09', {}, scored, {}, raw,
                          {'facts': [{'fact_id': 'f', 'canonical_truth': 'Reference truth'}]})
            html = (root / 'answer-review.html').read_text()
            md = (root / 'answer-review.md').read_text()
            self.assertIn('&lt;script&gt;', html)
            self.assertNotIn('<script>', html)
            self.assertNotIn('href="javascript:', html)
            self.assertIn('href="https://example.com/a"', html)
            self.assertEqual(html.count('<article>'), 3)
            first, second, third = html.split('<article>')[1:]
            self.assertIn('Reason A', first)
            self.assertIn('Scoring for Other', first)
            self.assertNotIn('Reason A', second)
            self.assertIn('Timed out', second)
            self.assertIn('raw evidence missing', third)
            for text in ['Reference truth', 'query A', 'full answer', 'Question A', 'Question B']:
                self.assertIn(text, md)

    def test_missing_raw_and_no_judge_are_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_reports(Path(tmp), '2026-09', {}, [{'answer_id': 'a', 'target': 'TiDB'}], None)
            text = (Path(tmp) / 'answer-review.html').read_text()
            self.assertIn('No answer recorded', text)
            self.assertIn('No fact verdict recorded', text)


if __name__ == '__main__':
    unittest.main()
