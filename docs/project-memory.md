# Project Memory

This file records repository-specific working conventions for future updates.

## Canonical Local Paths

Primary workspace for editing, running, and analysis:

```text
/Users/macbookair/Documents/TiDB Vibe
```

Canonical clean publication repository for GitHub sync:

```text
/private/tmp/geo-benchmark-upload-20260806
```

GitHub repository:

```text
https://github.com/ardelleFan/GEO-Benchmark
```

## Sync Rule

Use the primary workspace for all editing and benchmark runs. Use the clean publication repository only for audited GitHub uploads.

Do not create a new publication directory unless the canonical directory is missing or unusable. If the directory is missing, recreate it at the same path and push to the same GitHub repository.

## Publication Scope

Upload only:

- Benchmark code.
- English documentation.
- Configuration files.
- Prompt sets.
- Latest scored/report artifacts.

Do not upload:

- `.env.local` or secret-bearing files.
- Raw provider transcripts.
- Retry backups and aborted-run snapshots.
- Temporary scraped HTML.
- Local slide decks, handoff bundles, or visual output folders.

## Pre-Push Checks

Run these checks in the publication repository before pushing:

```bash
python3 -m unittest tests/test_geo_benchmark.py
env PYTHONPYCACHEPREFIX=/private/tmp/geo-upload-pycache python3 -m py_compile geo_benchmark/*.py
rg -n "[\\p{Han}]" .
git diff --check
```

The Chinese-character scan should return no matches for published content.
