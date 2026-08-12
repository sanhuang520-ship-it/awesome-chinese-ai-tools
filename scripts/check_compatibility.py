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

    activation = data["results"]["codexActivation"]
    verified_skills = activation.get("verifiedSkills", [])
    unknown = sorted(set(verified_skills) - set(actual))
    if unknown:
        fail(f"activation evidence references unknown skills: {unknown}")
    if verified_skills and activation.get("status") not in {"partial", "verified"}:
        fail("activation evidence exists but its status is not partial or verified")
    cases = activation.get("cases", [])
    if len(cases) != len(verified_skills):
        fail("every verified activation skill must have one case")
    expected_cases = [f"cases/{skill}-codex.md" for skill in verified_skills]
    if cases != expected_cases:
        fail(f"activation cases must map to verified skills in order: expected={expected_cases}")
    skill_results = activation.get("skillResults", {})
    if set(skill_results) != set(verified_skills):
        fail("skillResults must cover every verified activation skill exactly once")
    allowed_outcomes = {"completed", "waiting-input", "bounded-retest"}
    for skill, result in skill_results.items():
        if result.get("outcome") not in allowed_outcomes:
            fail(f"unknown task outcome for {skill}: {result.get('outcome')!r}")
        if result.get("case") != f"cases/{skill}-codex.md":
            fail(f"skillResults case does not match skill name: {skill}")
        if not result.get("labelZh") or not result.get("summaryZh"):
            fail(f"skillResults lacks public Chinese summary: {skill}")

    client_version = activation.get("clientVersion", "")
    display_version = client_version.removeprefix("codex-cli ")
    if data.get("clients", {}).get("codex") != f"Codex CLI {display_version}":
        fail("Codex client summary and activation clientVersion differ")

    examples = (ROOT / "EXAMPLES.md").read_text(encoding="utf-8")
    case_index = (ROOT / "cases" / "README.md").read_text(encoding="utf-8")
    for skill, case in zip(verified_skills, cases):
        if not (ROOT / case).is_file():
            fail(f"activation case does not exist: {case}")
        relative_case = case.removeprefix("cases/")
        if f"cases/{relative_case}" not in examples:
            fail(f"EXAMPLES.md does not link activation case for {skill}")
        if f"({relative_case})" not in case_index:
            fail(f"cases/README.md does not link activation case for {skill}")
        case_body = (ROOT / case).read_text(encoding="utf-8")
        if f"Codex CLI `{display_version}`" not in case_body:
            fail(f"activation case client version differs for {skill}")

    allowed = {"verified", "failed", "partial", "not-tested"}
    for key, result in data.get("results", {}).items():
        if result.get("status") not in allowed:
            fail(f"unknown status for {key}: {result.get('status')!r}")

    print(f"compatibility data OK: {expected_count} repository skills")


if __name__ == "__main__":
    main()
