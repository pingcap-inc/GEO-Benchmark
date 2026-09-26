"""Shared URL ownership and display-key classification."""
from __future__ import annotations

from urllib.parse import urlsplit


CODE_HOSTS = {"github.com", "gitlab.com", "huggingface.co"}

PINGCAP_CODE_ORGS = {"pingcap", "pingcap-inc", "tidbcloud"}

COMPETITOR_CODE_ORGS = {
    "chroma-core": "Chroma",
    "clickhouse": "ClickHouse",
    "cockroachdb": "CockroachDB",
    "elastic": "Elasticsearch",
    "milvus-io": "Milvus",
    "mongodb": "MongoDB",
    "neondatabase": "Neon",
    "pgvector": "pgvector",
    "pinecone-io": "Pinecone",
    "planetscale": "PlanetScale",
    "qdrant": "Qdrant",
    "redis": "Redis",
    "starrocks": "StarRocks",
    "supabase": "Supabase",
    "timescale": "TimescaleDB",
    "vespa-engine": "Vespa",
    "vitessio": "Vitess",
    "weaviate": "Weaviate",
    "yugabyte": "YugabyteDB",
}

PINGCAP_BASE_DOMAINS = {
    "pingcap.com",
    "pingcap.co.jp",
    "tidbcloud.com",
    "tidb.io",
    "tidb.net",
    "mem9.ai",
    "drive9.ai",
}

PINGCAP_EXACT_HOSTS = {"tidbcloudzerobrowser.vercel.app"}


def hostname_for_url(url: str) -> str | None:
    try:
        host = urlsplit(url).hostname
    except ValueError:
        return None
    if not host:
        return None
    host = host.lower().rstrip(".")
    return host[4:] if host.startswith("www.") else host


def is_host_or_subdomain(host: str, base_domain: str) -> bool:
    host = host.lower().rstrip(".")
    base_domain = base_domain.lower().rstrip(".")
    return host == base_domain or host.endswith("." + base_domain)


def code_host_org(url: str) -> tuple[str, str] | None:
    """Return the code-host hostname and first path segment, when present."""
    try:
        parsed = urlsplit(url)
    except ValueError:
        return None
    host = hostname_for_url(url)
    if host not in CODE_HOSTS:
        return None
    segments = [segment for segment in parsed.path.split("/") if segment]
    if not segments:
        return host, ""
    return host, segments[0].lower()


def code_host_product(url: str) -> str | None:
    parsed = code_host_org(url)
    if not parsed:
        return None
    _, org = parsed
    if org in PINGCAP_CODE_ORGS:
        return "TiDB"
    return COMPETITOR_CODE_ORGS.get(org)


def citation_display_key(url: str) -> str | None:
    """Group code-host citations by organization and other citations by host."""
    host = hostname_for_url(url)
    if not host:
        return None
    parsed = code_host_org(url)
    if parsed and parsed[1]:
        return f"{parsed[0]}/{parsed[1]}"
    return host


def is_pingcap_owned_url(url: str) -> bool:
    host = hostname_for_url(url)
    if not host:
        return False
    if host in PINGCAP_EXACT_HOSTS:
        return True
    if any(is_host_or_subdomain(host, base) for base in PINGCAP_BASE_DOMAINS):
        return True
    parsed = code_host_org(url)
    return bool(parsed and parsed[1] in PINGCAP_CODE_ORGS)


def code_host_source_type(url: str) -> str | None:
    """Classify code-host URLs; return None for non-code-host URLs."""
    parsed = code_host_org(url)
    if not parsed:
        return None
    _, org = parsed
    if org in PINGCAP_CODE_ORGS:
        return "PingCAP"
    if org in COMPETITOR_CODE_ORGS:
        return "Competitor"
    return "Other"
