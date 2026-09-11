"""Offline cited-domain reports built from saved benchmark evidence."""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from html import escape
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from .scoring import PRODUCT_URL_MARKERS, extract_raw_citation_urls, extract_urls


POSITIVE_RECOMMENDATION_CLASSES = {"best", "strong", "conditional"}
SOURCE_TYPE_ORDER = {"PingCAP": 0, "Competitor": 1, "Other": 2}


def normalize_domain(url: str) -> str | None:
    """Return a stable hostname for an HTTP(S) citation."""
    try:
        parsed = urlsplit(url)
    except ValueError:
        return None
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        return None
    domain = parsed.hostname.lower().rstrip(".")
    return domain[4:] if domain.startswith("www.") else domain


def normalize_citation_url(url: str) -> str | None:
    """Normalize common host variants while retaining the cited page path."""
    try:
        parsed = urlsplit(url)
    except ValueError:
        return None
    domain = normalize_domain(url)
    if not domain:
        return None
    port = parsed.port
    netloc = domain if port is None else f"{domain}:{port}"
    return urlunsplit(
        (parsed.scheme.lower(), netloc, parsed.path or "/", parsed.query, "")
    )


def source_type_for_url(url: str) -> str:
    """Classify a citation as PingCAP-owned, competitor-owned, or other."""
    lower = url.lower()
    if any(marker in lower for marker in PRODUCT_URL_MARKERS.get("TiDB", [])):
        return "PingCAP"
    for product, markers in PRODUCT_URL_MARKERS.items():
        if product != "TiDB" and any(marker in lower for marker in markers):
            return "Competitor"
    return "Other"


def build_cited_domain_details(
    raw_answers: list[dict[str, Any]],
    scored_answers: list[dict[str, Any]],
    prompts: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Build one record per answer and cited domain.

    The answer-domain grain prevents target scoring rows and repeated URLs from
    multiplying a citation. Prompt metadata is joined by prompt_id; scoring
    outcomes are joined by answer_id.
    """
    prompt_by_id = {row.get("prompt_id"): row for row in prompts or []}
    scores_by_answer: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scored_answers:
        scores_by_answer[str(row.get("answer_id", ""))].append(row)

    details: list[dict[str, Any]] = []
    for raw in raw_answers:
        if raw.get("status") != "ok":
            continue
        answer_id = str(raw.get("answer_id", ""))
        scores = scores_by_answer.get(answer_id, [])
        first_score = scores[0] if scores else {}
        prompt_id = str(raw.get("prompt_id", first_score.get("prompt_id", "")))
        prompt = prompt_by_id.get(prompt_id, {})
        answer = str(raw.get("raw_answer", ""))

        mentioned_products = sorted(
            {
                str(row.get("target"))
                for row in scores
                if row.get("target") and row.get("mentioned_target")
            }
        )
        recommended_products = {
            str(row.get("target"))
            for row in scores
            if row.get("target")
            and row.get("recommendation_class") in POSITIVE_RECOMMENDATION_CLASSES
        }
        recommended_products.update(
            str(row.get("competitive_winner"))
            for row in scores
            if row.get("competitive_winner")
        )

        urls = sorted(
            {
                normalized
                for url in (
                    extract_urls(answer)
                    + extract_raw_citation_urls(raw.get("raw_citations", []))
                )
                if (normalized := normalize_citation_url(url))
            }
        )
        urls_by_domain: dict[str, list[str]] = defaultdict(list)
        type_by_domain: dict[str, str] = {}
        for url in urls:
            domain = normalize_domain(url)
            if not domain:
                continue
            urls_by_domain[domain].append(url)
            candidate_type = source_type_for_url(url)
            current_type = type_by_domain.get(domain)
            if current_type is None or SOURCE_TYPE_ORDER[candidate_type] < SOURCE_TYPE_ORDER[current_type]:
                type_by_domain[domain] = candidate_type

        declared_brand_class = str(prompt.get("brand_class", "")).strip().lower()
        if declared_brand_class not in {"branded", "non_branded"}:
            declared_brand_class = (
                "branded" if any(row.get("target_in_prompt") for row in scores) else "non_branded"
            )

        for domain in sorted(urls_by_domain):
            details.append(
                {
                    "domain": domain,
                    "source_type": type_by_domain[domain],
                    "answer_id": answer_id,
                    "prompt_id": prompt_id,
                    "prompt_text": prompt.get("prompt_text") or raw.get("prompt_text", ""),
                    "brand_class": declared_brand_class,
                    "group": prompt.get("group") or first_score.get("group") or "unknown",
                    "prompt_type": prompt.get("prompt_type")
                    or first_score.get("prompt_type")
                    or "unknown",
                    "use_case": prompt.get("use_case")
                    or first_score.get("use_case")
                    or "unknown",
                    "panel": prompt.get("panel") or first_score.get("panel") or "unknown",
                    "model_surface": raw.get("model_surface")
                    or first_score.get("model_surface")
                    or "unknown",
                    "run_index": raw.get("run_index"),
                    "tidb_appeared": "TiDB" in mentioned_products,
                    "mentioned_products": mentioned_products,
                    "recommended_products": sorted(recommended_products),
                    "citation_urls": sorted(set(urls_by_domain[domain])),
                }
            )
    return details


def aggregate_cited_domains(details: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Aggregate answer-domain records, ranking primarily by unique prompts."""
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in details:
        buckets[row["domain"]].append(row)

    summary: list[dict[str, Any]] = []
    for domain, rows in buckets.items():
        prompt_ids = {str(row["prompt_id"]) for row in rows}
        tidb_prompt_ids = {
            str(row["prompt_id"]) for row in rows if row.get("tidb_appeared")
        }
        recommendation_prompts: dict[str, set[str]] = defaultdict(set)
        for row in rows:
            for product in row.get("recommended_products", []):
                recommendation_prompts[str(product)].add(str(row["prompt_id"]))
        recommendation_counts = {
            product: len(ids)
            for product, ids in sorted(
                recommendation_prompts.items(), key=lambda item: (-len(item[1]), item[0])
            )
        }
        summary.append(
            {
                "domain": domain,
                "source_type": min(
                    (str(row["source_type"]) for row in rows),
                    key=lambda value: SOURCE_TYPE_ORDER.get(value, 99),
                ),
                "prompt_count": len(prompt_ids),
                "cited_answer_count": len({str(row["answer_id"]) for row in rows}),
                "tidb_appeared_prompt_count": len(tidb_prompt_ids),
                "recommended_products": recommendation_counts,
                "providers": sorted({str(row["model_surface"]) for row in rows}),
                "brand_classes": sorted({str(row["brand_class"]) for row in rows}),
                "groups": sorted({str(row["group"]) for row in rows}),
                "prompt_types": sorted({str(row["prompt_type"]) for row in rows}),
                "panels": sorted({str(row["panel"]) for row in rows}),
            }
        )
    return sorted(
        summary,
        key=lambda row: (-row["prompt_count"], -row["cited_answer_count"], row["domain"]),
    )


def write_cited_domain_report(
    report_dir: Path,
    month: str,
    raw_answers: list[dict[str, Any]],
    scored_answers: list[dict[str, Any]],
    prompts: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Write CSV exports and a filterable offline cited-domain report."""
    report_dir.mkdir(parents=True, exist_ok=True)
    details = build_cited_domain_details(raw_answers, scored_answers, prompts)
    summary = aggregate_cited_domains(details)
    write_domain_summary_csv(report_dir / "cited-domain-summary.csv", summary)
    write_domain_details_csv(report_dir / "cited-domain-details.csv", details)
    write_domain_html(report_dir / "cited-domains.html", month, details)
    return summary


def write_domain_summary_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "domain",
        "source_type",
        "prompt_count",
        "cited_answer_count",
        "tidb_appeared_prompt_count",
        "recommended_products",
        "providers",
        "brand_classes",
        "groups",
        "prompt_types",
        "panels",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            output = dict(row)
            output["recommended_products"] = "; ".join(
                f"{product} ({count})"
                for product, count in row["recommended_products"].items()
            )
            for key in ["providers", "brand_classes", "groups", "prompt_types", "panels"]:
                output[key] = "; ".join(row[key])
            writer.writerow(output)


def write_domain_details_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "domain",
        "source_type",
        "answer_id",
        "prompt_id",
        "prompt_text",
        "brand_class",
        "group",
        "prompt_type",
        "use_case",
        "panel",
        "model_surface",
        "run_index",
        "tidb_appeared",
        "mentioned_products",
        "recommended_products",
        "citation_urls",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            output = dict(row)
            for key in ["mentioned_products", "recommended_products", "citation_urls"]:
                output[key] = " | ".join(str(value) for value in row[key])
            writer.writerow(output)


def write_domain_html(path: Path, month: str, details: list[dict[str, Any]]) -> None:
    safe_json = (
        json.dumps(details, ensure_ascii=False, separators=(",", ":"))
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )
    html = DOMAIN_HTML.replace("__MONTH__", escape(month)).replace("__SOURCE_ROWS__", safe_json)
    path.write_text(html, encoding="utf-8")


DOMAIN_HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cited domains — __MONTH__</title>
<style>
:root{--navy:#0d3152;--blue:#2c80ce;--red:#dc150b;--ink:#172b3a;--muted:#5d6974;--line:#d7dde3;--bg:#f4f6f8}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,-apple-system,sans-serif}
header{background:var(--navy);color:white;padding:30px max(24px,calc((100vw - 1400px)/2))}h1{margin:0 0 6px;font-size:28px}header p{margin:0;color:#dbe8f5}
main{max-width:1400px;margin:24px auto;padding:0 24px}.card{background:white;border:1px solid var(--line);border-radius:12px;padding:20px;margin-bottom:20px;box-shadow:0 2px 8px #0d31520d}
.filters{display:grid;grid-template-columns:repeat(5,minmax(150px,1fr));gap:10px}.filters label:first-child{grid-column:span 2}label{font-size:12px;font-weight:700;color:var(--muted)}input,select{width:100%;margin-top:5px;padding:9px;border:1px solid #aab5bf;border-radius:6px;background:white;color:var(--ink)}
.summary{display:flex;gap:28px;flex-wrap:wrap}.stat strong{display:block;font-size:24px;color:var(--navy)}.stat span{color:var(--muted)}
.table-wrap{overflow:auto;max-height:620px;border:1px solid var(--line);border-radius:8px}table{border-collapse:collapse;width:100%;min-width:950px}th,td{padding:10px 12px;border-bottom:1px solid #e7ebef;text-align:left;vertical-align:top}th{position:sticky;top:0;background:#edf3f8;color:var(--navy);z-index:1}tbody tr:hover{background:#f7fbff}.domain{font-weight:750;color:var(--navy)}
.pill{display:inline-block;padding:2px 7px;margin:1px 3px 1px 0;border-radius:99px;background:#e8eef5;white-space:nowrap}.PingCAP{background:#fde9e8;color:#87120c}.Competitor{background:#e8f1fb;color:#10487b}.Other{background:#eef0f2;color:#424d57}
.muted{color:var(--muted)}.yes{color:#0f6b3a;font-weight:700}.no{color:var(--muted)}h2{font-size:20px;margin:0 0 12px}.note{color:var(--muted);margin-top:0}.empty{padding:28px;text-align:center;color:var(--muted)}a{color:#10487b;overflow-wrap:anywhere}.detail{font-size:13px}.detail td:nth-child(4){min-width:300px}
@media(max-width:1000px){.filters{grid-template-columns:repeat(2,1fr)}}@media(max-width:600px){.filters{grid-template-columns:1fr}}
</style></head><body>
<header><h1>Cited domains</h1><p>__MONTH__ · Saved benchmark evidence · Ranked by unique prompts</p></header>
<main>
<section class="card"><div class="filters">
<label>Domain<input id="domain" type="search" placeholder="Search domains"></label>
<label>Brand class<select id="brand_class"></select></label>
<label>Group<select id="group"></select></label>
<label>Prompt type<select id="prompt_type"></select></label>
<label>Provider<select id="model_surface"></select></label>
<label>Panel<select id="panel"></select></label>
<label>Source type<select id="source_type"></select></label>
<label>Recommended<select id="recommended_product"></select></label>
<label>TiDB appeared<select id="tidb_appeared"><option value="">All</option><option value="yes">Yes</option><option value="no">No</option></select></label>
</div></section>
<section class="card"><div class="summary">
<div class="stat"><strong id="domainCount">0</strong><span>cited domains</span></div>
<div class="stat"><strong id="promptCount">0</strong><span>unique prompts</span></div>
<div class="stat"><strong id="answerCount">0</strong><span>cited answers</span></div>
</div></section>
<section class="card"><h2>Domain ranking</h2><p class="note">A domain counts once per answer and is ranked by the number of unique prompts. Product recommendations are associations observed in the same answers, not proof that a source caused the recommendation.</p><div class="table-wrap"><table><thead><tr><th>Domain</th><th>Type</th><th>Prompts</th><th>Cited answers</th><th>TiDB appeared</th><th>Recommended products</th><th>Providers</th></tr></thead><tbody id="domainRows"></tbody></table></div></section>
<section class="card"><h2>Prompt and citation details</h2><p class="note" id="detailNote"></p><div class="table-wrap"><table class="detail"><thead><tr><th>Domain</th><th>Prompt</th><th>Provider</th><th>Question</th><th>TiDB</th><th>Recommended</th><th>Cited pages</th></tr></thead><tbody id="detailRows"></tbody></table></div></section>
</main><script>
const SOURCE_ROWS=__SOURCE_ROWS__;
const fields=['brand_class','group','prompt_type','model_surface','panel','source_type'];
function node(tag,text,cls){const el=document.createElement(tag);if(text!==undefined)el.textContent=text;if(cls)el.className=cls;return el}
function values(field){return [...new Set(SOURCE_ROWS.map(row=>row[field]).filter(Boolean))].sort()}
function fillSelect(id,items){const select=document.getElementById(id);select.appendChild(new Option('All',''));for(const value of items)select.appendChild(new Option(value,value))}
for(const field of fields)fillSelect(field,values(field));
fillSelect('recommended_product',[...new Set(SOURCE_ROWS.flatMap(row=>row.recommended_products))].sort());
function selected(id){return document.getElementById(id).value}
function filteredRows(){const term=selected('domain').toLowerCase(),tidb=selected('tidb_appeared');return SOURCE_ROWS.filter(row=>(!term||row.domain.includes(term))&&fields.every(field=>!selected(field)||row[field]===selected(field))&&(!selected('recommended_product')||row.recommended_products.includes(selected('recommended_product')))&&(!tidb||(tidb==='yes')===row.tidb_appeared))}
function aggregate(rows){const map=new Map();for(const row of rows){if(!map.has(row.domain))map.set(row.domain,{domain:row.domain,source_type:row.source_type,prompts:new Set(),answers:new Set(),tidb:new Set(),providers:new Set(),recommended:new Map()});const item=map.get(row.domain);item.prompts.add(row.prompt_id);item.answers.add(row.answer_id);item.providers.add(row.model_surface);if(row.tidb_appeared)item.tidb.add(row.prompt_id);for(const product of row.recommended_products){if(!item.recommended.has(product))item.recommended.set(product,new Set());item.recommended.get(product).add(row.prompt_id)}}return [...map.values()].sort((a,b)=>b.prompts.size-a.prompts.size||b.answers.size-a.answers.size||a.domain.localeCompare(b.domain))}
function pills(values){const box=document.createElement('div');for(const value of values)box.appendChild(node('span',value,'pill'));return box}
function render(){const rows=filteredRows(),summary=aggregate(rows),body=document.getElementById('domainRows');body.replaceChildren();for(const item of summary){const tr=node('tr');tr.appendChild(node('td',item.domain,'domain'));tr.appendChild(node('td',item.source_type,'pill '+item.source_type));tr.appendChild(node('td',String(item.prompts.size)));tr.appendChild(node('td',String(item.answers.size)));tr.appendChild(node('td',item.tidb.size+' prompts',item.tidb.size?'yes':'no'));tr.appendChild(pills([...item.recommended.entries()].sort((a,b)=>b[1].size-a[1].size||a[0].localeCompare(b[0])).map(([p,ids])=>p+' ('+ids.size+')')));tr.appendChild(pills([...item.providers].sort()));body.appendChild(tr)}if(!summary.length){const td=node('td','No cited domains match these filters.','empty');td.colSpan=7;const tr=node('tr');tr.appendChild(td);body.appendChild(tr)}
document.getElementById('domainCount').textContent=summary.length;document.getElementById('promptCount').textContent=new Set(rows.map(r=>r.prompt_id)).size;document.getElementById('answerCount').textContent=new Set(rows.map(r=>r.answer_id)).size;
const detail=document.getElementById('detailRows');detail.replaceChildren();for(const row of rows.slice(0,500)){const tr=node('tr');tr.appendChild(node('td',row.domain,'domain'));tr.appendChild(node('td',row.prompt_id));tr.appendChild(node('td',row.model_surface));tr.appendChild(node('td',row.prompt_text));tr.appendChild(node('td',row.tidb_appeared?'Appeared':'Did not appear',row.tidb_appeared?'yes':'no'));tr.appendChild(pills(row.recommended_products));const links=node('td');for(const url of row.citation_urls){const a=node('a',url);a.href=url;a.target='_blank';a.rel='noreferrer';links.appendChild(a);links.appendChild(document.createElement('br'))}tr.appendChild(links);detail.appendChild(tr)}document.getElementById('detailNote').textContent=rows.length>500?'Showing the first 500 of '+rows.length+' matching answer-domain records. Use the CSV for the complete export.':rows.length+' matching answer-domain records.'}
for(const id of ['domain',...fields,'recommended_product','tidb_appeared'])document.getElementById(id).addEventListener(id==='domain'?'input':'change',render);render();
</script></body></html>'''
