#!/usr/bin/env python3
"""Capture a reproducible public GitHub repository-search baseline."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import ssl
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


REPOSITORY = "sanhuang520-ship-it/awesome-chinese-ai-tools"
API = "https://api.github.com"
QUERIES = (
    "中文 agent skills",
    "chinese agent skills",
    "codex skills chinese",
    "中文 AI skills",
    "awesome chinese ai tools",
)
PAGE_SIZE = 20


def ssl_context():
    cafile = os.environ.get("SSL_CERT_FILE")
    if not cafile:
        try:
            import certifi
            cafile = certifi.where()
        except ImportError:
            cafile = None
    return ssl.create_default_context(cafile=cafile)


def github_search(query: str) -> dict:
    params = urlencode({"q": query, "sort": "best-match", "order": "desc", "per_page": PAGE_SIZE})
    request = Request(
        f"{API}/search/repositories?{params}",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "awesome-chinese-ai-tools-search-baseline",
        },
    )
    with urlopen(request, timeout=20, context=ssl_context()) as response:
        return json.load(response)


def build_snapshot(search, repository: dict, recorded_at: str) -> dict:
    results = []
    for query in QUERIES:
        response = search(query)
        rank = next(
            (index for index, item in enumerate(response.get("items", []), start=1)
             if item.get("full_name") == REPOSITORY),
            None,
        )
        results.append({
            "query": query,
            "totalResults": response.get("total_count", 0),
            "targetRankInTop20": rank,
        })
    return {
        "recordedAt": recorded_at,
        "source": "GitHub public repository search API",
        "repository": REPOSITORY,
        "method": {
            "sort": "best-match",
            "order": "desc",
            "pageSize": PAGE_SIZE,
            "authentication": "anonymous",
            "scope": "repository search only",
        },
        "queries": results,
        "repositoryMetrics": {
            "stars": repository["stargazers_count"],
            "forks": repository["forks_count"],
        },
        "notes": "Observation only, not attribution evidence. GitHub search rankings and result totals can change with indexing, repository activity, Stars, query interpretation and other unknown factors. A later rank change cannot be attributed to one README phrase, and a top-20 absence does not mean the repository is absent from all results. This baseline does not promise discovery or Star growth.",
    }


def github_repository() -> dict:
    request = Request(
        f"{API}/repos/{REPOSITORY}",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "awesome-chinese-ai-tools-search-baseline",
        },
    )
    with urlopen(request, timeout=20, context=ssl_context()) as response:
        return json.load(response)


def main() -> int:
    parser = argparse.ArgumentParser(description="Save a public GitHub repository-search baseline")
    parser.add_argument("--output", type=Path, help="JSON output path; default metrics/YYYY-MM-DD-github-search.json")
    args = parser.parse_args()
    now = dt.datetime.now().astimezone().replace(microsecond=0)
    output = args.output or Path("metrics") / f"{now.date().isoformat()}-github-search.json"
    try:
        snapshot = build_snapshot(github_search, github_repository(), now.isoformat())
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"search capture error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(f"GitHub search snapshot written: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
