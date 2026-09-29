#!/usr/bin/env python3
"""Capture an owner-only GitHub Traffic snapshot without persisting credentials."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import ssl
import sys
from pathlib import Path
from urllib.request import Request, urlopen


REPOSITORY = "sanhuang520-ship-it/awesome-chinese-ai-tools"
API = f"https://api.github.com/repos/{REPOSITORY}"


def ssl_context():
    cafile = os.environ.get("SSL_CERT_FILE")
    if not cafile:
        try:
            import certifi
            cafile = certifi.where()
        except ImportError:
            cafile = None
    return ssl.create_default_context(cafile=cafile)


def github_get(path: str, token: str):
    request = Request(
        API + path,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "awesome-chinese-ai-tools-maintenance",
        },
    )
    with urlopen(request, timeout=20, context=ssl_context()) as response:
        return json.load(response)


def build_snapshot(get, recorded_at: str) -> dict:
    repository = get("")
    views = get("/traffic/views")
    clones = get("/traffic/clones")
    referrers = get("/traffic/popular/referrers")
    paths = get("/traffic/popular/paths")
    return {
        "recordedAt": recorded_at,
        "source": "GitHub owner Traffic API and public repository API",
        "windowDays": 14,
        "windowType": "rolling; exact first day is controlled by GitHub and may contain days with zero events",
        "repository": REPOSITORY,
        "repositoryMetrics": {
            "stars": repository["stargazers_count"],
            "forks": repository["forks_count"],
            "openIssues": repository["open_issues_count"],
            "subscribers": repository["subscribers_count"],
        },
        "traffic": {
            "views": views["count"],
            "uniqueVisitors": views["uniques"],
            "clones": clones["count"],
            "uniqueCloners": clones["uniques"],
            "topReferrers": [
                {"name": item["referrer"], "views": item["count"], "uniqueVisitors": item["uniques"]}
                for item in referrers
            ],
            "topPaths": [
                {"path": item["path"], "title": item["title"], "views": item["count"], "uniqueVisitors": item["uniques"]}
                for item in paths
            ],
        },
        "privacy": "Only aggregate counts and public path/referrer labels are stored; no token, IP address or visitor identity is written.",
        "notes": "Observation only, not attribution evidence. GitHub's rolling window can overlap earlier snapshots. Clone counts may include CLI installs, automation, CI, repeated machines or other non-human activity and must not be called users. Referrer and path tables are partial top lists. Stars are cumulative while traffic is windowed, so this snapshot cannot be used as a Star conversion rate or prove that one edit caused growth.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Save an aggregate GitHub Traffic snapshot")
    parser.add_argument("--output", type=Path, help="JSON output path; default metrics/YYYY-MM-DD-traffic-owner.json")
    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("capture error: GITHUB_TOKEN is required and is never written to output", file=sys.stderr)
        return 2
    now = dt.datetime.now().astimezone().replace(microsecond=0)
    output = args.output or Path("metrics") / f"{now.date().isoformat()}-traffic-owner.json"
    try:
        snapshot = build_snapshot(lambda path: github_get(path, token), now.isoformat())
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"capture error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(f"traffic snapshot written: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
