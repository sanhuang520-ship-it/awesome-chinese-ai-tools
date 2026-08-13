#!/usr/bin/env python3
"""Validate one privacy-scrubbed skills CLI installation observation."""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SENSITIVE = (
    ("API key-like value", re.compile(r"\b(?:sk|ghp|github_pat)_[A-Za-z0-9_-]{8,}\b", re.I)),
    ("email address", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
    ("private macOS/Linux path", re.compile(r"/(?:Users|home)/[^/\s]+/")),
    ("private Windows path", re.compile(r"\b[A-Z]:\\Users\\[^\\\s]+\\", re.I)),
)


def fail(errors, message):
    errors.append(message)


def validate(report):
    errors = []
    required = {"schemaVersion", "id", "recordedAt", "sourceType", "environment", "command", "skill", "result", "paths", "boundaries", "privacy"}
    allowed = required | {"observed"}
    if not isinstance(report, dict):
        return ["$: must be an object"]
    if required - set(report):
        fail(errors, "$: missing fields: " + ", ".join(sorted(required - set(report))))
    if set(report) - allowed:
        fail(errors, "$: unknown fields: " + ", ".join(sorted(set(report) - allowed)))
    if report.get("schemaVersion") != 1:
        fail(errors, "schemaVersion: must equal 1")
    if not isinstance(report.get("id"), str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]{7,127}", report["id"]):
        fail(errors, "id: must be 8-128 lowercase URL-safe characters")
    if report.get("sourceType") not in {"repository-self-test", "community-report"}:
        fail(errors, "sourceType: expected repository-self-test or community-report")
    try:
        if datetime.fromisoformat(str(report.get("recordedAt", "")).replace("Z", "+00:00")).tzinfo is None:
            fail(errors, "recordedAt: timezone offset is required")
    except ValueError:
        fail(errors, "recordedAt: must be an ISO 8601 date-time")
    environment = report.get("environment")
    required_environment = {"os", "terminal", "nodeVersion", "skillsVersion"}
    if not isinstance(environment, dict) or set(environment) != required_environment:
        fail(errors, "environment: must contain only os, terminal, nodeVersion, skillsVersion")
    elif any(not isinstance(value, str) or not value.strip() for value in environment.values()):
        fail(errors, "environment: values must be non-empty strings")
    for key in ("command", "skill"):
        if not isinstance(report.get(key), str) or not report[key].strip():
            fail(errors, f"{key}: must be a non-empty string")
    if report.get("result") not in {"installed", "failed", "blocked", "unknown"}:
        fail(errors, "result: expected installed, failed, blocked, or unknown")
    paths = report.get("paths")
    if not isinstance(paths, list) or not paths:
        fail(errors, "paths: must be a non-empty array")
    else:
        for index, path in enumerate(paths):
            if not isinstance(path, dict) or set(path) != {"path", "type", "exists"}:
                fail(errors, f"paths[{index}]: must contain only path, type, exists")
                continue
            if not isinstance(path["path"], str) or not path["path"].strip():
                fail(errors, f"paths[{index}].path: must be non-empty")
            if path["type"] not in {"directory", "file", "symlink", "junction", "unknown"}:
                fail(errors, f"paths[{index}].type: invalid value")
            if not isinstance(path["exists"], bool):
                fail(errors, f"paths[{index}].exists: must be boolean")
    for field, required_nonempty in (("boundaries", True), ("observed", False)):
        values = report.get(field, [])
        if field in report and (not isinstance(values, list) or (required_nonempty and not values) or any(not isinstance(x, str) or not x.strip() for x in values)):
            fail(errors, f"{field}: must be {'a non-empty ' if required_nonempty else 'an '}array of non-empty strings")
    privacy = report.get("privacy")
    if privacy != {"scrubbed": True, "containsSensitiveData": False}:
        fail(errors, "privacy: must confirm scrubbed=true and containsSensitiveData=false")
    public_text = json.dumps(report, ensure_ascii=False)
    for label, pattern in SENSITIVE:
        if pattern.search(public_text):
            fail(errors, f"privacy scan: found {label}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"installation report invalid: {exc}", file=sys.stderr)
        return 1
    errors = validate(report)
    if errors:
        print("installation report invalid:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"installation report OK: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
