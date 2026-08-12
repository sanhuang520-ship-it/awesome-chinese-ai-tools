#!/usr/bin/env python3
"""Validate the committed compatibility evidence against repository contents."""

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "compatibility.json"
NAME_RE = re.compile(r"^name:\s*([^\n]+)$", re.MULTILINE)


def fail(message: str) -> None:
    print(f"compatibility check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def repository_skills() -> list[str]:
    names = []
    for skill_file in sorted((ROOT / "skills").glob("*/SKILL.md")):
        match = NAME_RE.search(skill_file.read_text(encoding="utf-8"))
        if not match:
            fail(f"missing name frontmatter: {skill_file.relative_to(ROOT)}")
        name = match.group(1).strip().strip('"\'')
        if name != skill_file.parent.name:
            fail(f"frontmatter name {name!r} differs from directory {skill_file.parent.name!r}")
        names.append(name)
    return names


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    actual = repository_skills()
    recorded = data.get("skills", [])
    if recorded != actual:
        fail(f"recorded skills differ from repository: recorded={recorded}, actual={actual}")

    expected_count = len(actual)
    discovery_count = data["results"]["discovery"].get("count")
    identical_count = data["results"]["codexInstall"].get("identicalCount")
    if discovery_count != expected_count:
        fail(f"discovery count is {discovery_count}, expected {expected_count}")
    if identical_count != expected_count:
        fail(f"Codex identical count is {identical_count}, expected {expected_count}")

    allowed = {"verified", "failed", "partial", "not-tested"}
    for key, result in data.get("results", {}).items():
        if result.get("status") not in allowed:
            fail(f"unknown status for {key}: {result.get('status')!r}")

    print(f"compatibility data OK: {expected_count} repository skills")


if __name__ == "__main__":
    main()
