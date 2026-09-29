#!/usr/bin/env python3
"""Compare public GitHub repository fields with the committed profile."""

from __future__ import annotations

import json
import ssl
import sys
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "data" / "repository-profile.json"


def ssl_context() -> ssl.SSLContext:
    cafile = None
    try:
        import certifi

        cafile = certifi.where()
    except ImportError:
        pass
    return ssl.create_default_context(cafile=cafile)


def compare_profile(expected: dict, actual: dict) -> list[str]:
    failures = []
    if actual.get("full_name") != expected.get("repository"):
        failures.append("repository")
    for field in ("description", "homepage"):
        if actual.get(field) != expected.get(field):
            failures.append(field)
    if sorted(actual.get("topics", [])) != sorted(expected.get("topics", [])):
        failures.append("topics")
    return failures


def fetch_repository(repository: str) -> dict:
    request = Request(
        f"https://api.github.com/repos/{repository}",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "awesome-chinese-ai-tools-profile-check",
        },
    )
    with urlopen(request, timeout=20, context=ssl_context()) as response:
        return json.load(response)


def main() -> int:
    expected = json.loads(PROFILE.read_text(encoding="utf-8"))
    try:
        actual = fetch_repository(expected["repository"])
    except Exception as exc:
        print(f"repository profile check error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    failures = compare_profile(expected, actual)
    if failures:
        print("repository profile drift: " + ", ".join(failures), file=sys.stderr)
        return 1
    print(f"repository profile OK: {expected['repository']} ({len(expected['topics'])} topics)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
