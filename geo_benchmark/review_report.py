"""Offline, escaped review reports built only from saved benchmark evidence."""
from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


def write_review_report(
    report_dir: Path, month: str, scored: list[dict[str, Any]],
    raw: list[dict[str, Any]], fact_base: dict[str, Any] | None = None,
) -> None:
    facts = {f['fact_id']: f for f in (fact_base or {}).get('facts', [])}
    scores: dict[str, list[dict[str, Any]]] = {}
    for row in scored:
        scores.setdefault(row.get('answer_id', ''), []).append(row)
    # Include failed collection attempts too; never join on prompt ID alone.
    records = list(raw)
    seen = {r.get('answer_id') for r in raw}
    records.extend({'answer_id': key, 'prompt_id': rows[0].get('prompt_id'),
                    'status': 'raw evidence missing'}
                   for key, rows in scores.items() if key not in seen)
    html = []
    md = [f'# Answer review — {month}', '',
          'Saved evidence only. No API calls are made to create this report.', '',
          'Visibility scores use questions that do not name the target. Semantic judgments cover selected facts only, not every claim in an answer. They remain shadow scores.', '',
          'Fact references below come from the configuration at report generation time; they are not a historical snapshot of what the judge received.', '']

    def heading(value: str, level: int = 3) -> None:
        html.append(f'<h{level}>{escape(value)}</h{level}>')
        md.extend(['#' * level + ' ' + value, ''])

    def block(label: str, value: Any) -> None:
        text = str(value if value is not None else 'Not recorded')
        html.append(f'<p><strong>{escape(label)}</strong></p><pre>{escape(text)}</pre>')
        # Use a fence longer than any embedded run to preserve model output literally.
        fence = '`' * max(3, max((len(x) for x in text.split() if set(x) == {'`'}), default=0) + 1)
        while fence in text:
            fence += '`'
        md.extend([f'**{label}**', '', fence + 'text', text, fence, ''])

    def links(label: str, urls: list[Any]) -> None:
        heading(label, 4)
        if not urls:
            block('Status', 'None recorded')
        for item in urls:
            url = str(item.get('url', item) if isinstance(item, dict) else item)
            try:
                safe_link = urlsplit(url).scheme in {'https', 'http'}
            except ValueError:
                safe_link = False
            if safe_link:
                html.append(f'<p><a href="{escape(url, quote=True)}" rel="noreferrer">{escape(url)}</a></p>')
            else:
                html.append(f'<pre>{escape(url)}</pre>')
            md.extend([url, ''])

    heading(f'{len(records)} saved answers', 2)
    for index, answer in enumerate(records, 1):
        html.append('<article>')
        heading(f"{index}. {answer.get('prompt_id', 'Unknown prompt')}", 2)
        block('Question', answer.get('prompt_text', 'Question text unavailable in saved raw evidence'))
        block('Run details', '\n'.join(f'{k}: {answer.get(k, "Not recorded")}' for k in
              ['answer_id', 'model_surface', 'model_name', 'run_index', 'timestamp', 'status', 'web_search_mode']))
        block('Full answer', answer.get('raw_answer', 'No answer recorded'))
        if answer.get('error'):
            block('Collection error', answer['error'])
        links('Answer citations (recorded, not independently verified)', answer.get('raw_citations', []))
        block('Search activity', f"Capture status: {answer.get('fan_out_status', 'Not recorded')}\nSearch requests: {answer.get('web_search_requests', 'Not recorded')}")
        block('Fan-out queries exposed by the provider', '\n'.join(answer.get('fan_out_queries', [])) or 'None recorded')
        for row in scores.get(answer.get('answer_id', ''), []):
            heading(f"Scoring for {row.get('target', 'Unknown target')}")
            block('Visibility eligibility', 'Excluded: the question names this target.' if row.get('target_in_prompt') else 'Included: the question does not name this target.')
            labels = {'mentioned_target': 'Target mentioned', 'mention_position': 'Mention position',
                      'presence_score': 'Prominence contribution (0–1)', 'considered_in_fan_out': 'Target in search queries',
                      'recommendation_class': 'Recommendation', 'citation_authority_answer': 'Citation authority',
                      'accuracy': 'Legacy accuracy', 'semantic_fact_accuracy': 'Semantic fact accuracy (0–1)'}
            block('Recorded scores', '\n'.join(f'{label}: {row[k] if row.get(k) is not None else "Not scored / unavailable"}' for k, label in labels.items()))
            block('Score guide', 'A value of 1 on a 0–1 scale means the maximum score. Semantic accuracy is a shadow score for the selected facts only. Not scored / unavailable does not mean incorrect.')
            judge = row.get('semantic_fact_judge') or {}
            block('Semantic coverage', f"Mode: {judge.get('mode', 'off / not recorded')}\nDisposition: {judge.get('coverage_disposition', 'Not recorded')}\nSelected facts: {judge.get('selected_facts', 0)}\nFact-base version: {judge.get('fact_base_version', 'Not recorded')}")
            if not judge.get('results'):
                block('Judge decision', 'No fact verdict recorded. Review-required facts await approval; comparison-only questions use comparison scoring; unmapped questions have no selected fact mapping.')
            for result in judge.get('results', []):
                heading(f"{result.get('fact_id')} — {result.get('verdict')}", 4)
                block('Judge explanation (as saved)', result.get('reason'))
                if len(str(result.get('reason', ''))) >= 500:
                    block('Audit note', 'This saved explanation may have been shortened by the scorer. Missing text cannot be recovered from this report.')
                block('Answer excerpt (as saved)', result.get('answer_excerpt'))
                block('Qualifier checks', f"Activated: {result.get('qualifier_check_activated')}\nDimensions: {', '.join(result.get('qualifier_dimensions', [])) or 'None recorded'}\nCached: {result.get('cached', False)}")
                fact = facts.get(result.get('fact_id'), {})
                block('Fact reference at report generation', fact.get('canonical_truth', 'Not available'))
                if fact:
                    block('Correctness examples (not a required checklist)', fact.get('correct_when'))
                    block('Contradiction examples', fact.get('incorrect_when'))
                    block('Fact review status', f"{fact.get('status')} · verified {fact.get('verified_on')} · review by {fact.get('review_by')}")
                    links('Fact reference sources', fact.get('source_urls', []))
            block('Human review checklist', 'Does the answer address the question? Do the citations support its claims? Does each judge verdict follow the relevant fact and qualifier rule? Record corrections separately; this file does not change scores.')
        if not scores.get(answer.get('answer_id', '')):
            block('Scoring', 'No scored row available for this answer.')
        html.append('</article>')
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / 'answer-review.md').write_text('\n'.join(md), encoding='utf-8')
    intro = ''.join(f'<p>{escape(p)}</p>' for p in md[2:8] if p)
    (report_dir / 'answer-review.html').write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>GEO Benchmark answer review</title><style>'
        'body{font:16px/1.6 system-ui,sans-serif;color:#172b3a;background:#f4f6f8;max-width:1050px;margin:40px auto;padding:0 24px}'
        'article{background:white;border:1px solid #d6dde3;border-radius:12px;padding:28px;margin:24px 0}'
        'h1,h2{color:#87120c}h4{margin-bottom:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit;margin-top:0}'
        'a{color:#10487b;overflow-wrap:anywhere}@media print{body{background:white;margin:0}article{break-before:page;border:0;padding:0}}'
        '</style><h1>GEO Benchmark answer review — ' + escape(month) + '</h1>' + intro + ''.join(html) + '</html>', encoding='utf-8')
