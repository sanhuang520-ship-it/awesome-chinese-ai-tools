#!/usr/bin/env python3
"""Read-only check that the stable tag also has a matching public GitHub Release."""

from __future__ import annotations

import json
import ssl
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "sanhuang520-ship-it/awesome-chinese-ai-tools"
TAG = "v1.2.0"
EXPECTED_COMMIT = "ab44cd965d4167e6efb3849876ab5efef670f978"
API = f"https://api.github.com/repos/{REPOSITORY}"


def ssl_context() -> ssl.SSLContext:
    cafile = None
    try:
        import certifi
        cafile = certifi.where()
    except ImportError:
        pass
    return ssl.create_default_context(cafile=cafile)


def github_get(path: str):
    request = Request(
        API + path,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "awesome-chinese-ai-tools-release-check",
        },
    )
    with urlopen(request, timeout=20, context=ssl_context()) as response:
        return json.load(response)


def validate_release(release: dict, tag_ref: dict) -> list[str]:
    failures = []
    if release.get("tag_name") != TAG:
        failures.append("release tag")
    if release.get("draft"):
        failures.append("release is draft")
    if release.get("prerelease"):
        failures.append("release is prerelease")
    if release.get("name") != "v1.2.0 — 可复现证据、安全审计与双语发现":
        failures.append("release name")
    body = release.get("body", "")
    for phrase in ("10 项完成", "旧失败保留", "Claude Code 与 Cursor", "不是安全认证", "Stars 仍为 7"):
        if phrase not in body:
            failures.append(f"release body missing: {phrase}")
    tag_object = tag_ref.get("object", {})
    if tag_object.get("type") != "tag":
        failures.append("tag is not annotated")
    if tag_object.get("sha") == EXPECTED_COMMIT:
        failures.append("tag ref unexpectedly points directly to commit")
    return failures


def main() -> int:
    try:
        release = github_get(f"/releases/tags/{TAG}")
        tag_ref = github_get(f"/git/ref/tags/{TAG}")
    except HTTPError as exc:
        if exc.code == 404:
            print(f"GitHub Release {TAG} is not published", file=sys.stderr)
            return 1
        print(f"release check HTTP error: {exc.code}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"release check error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    failures = validate_release(release, tag_ref)
    if failures:
        print("release check failed: " + "; ".join(failures), file=sys.stderr)
        return 1
    print(f"GitHub Release OK: {release['html_url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
