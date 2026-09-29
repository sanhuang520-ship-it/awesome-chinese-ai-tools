#!/usr/bin/env python3
"""Validate one machine-readable compatibility report without third-party packages.

The published JSON Schema is the interchange contract. This checker enforces the
same required shape plus repository-specific skill, consistency and privacy rules.
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "compatibility-result.schema.json"

TOP_FIELDS = {
    "schemaVersion", "id", "recordedAt", "sourceType", "client", "skill",
    "task", "environment", "activation", "completion", "observed",
    "evidence", "boundaries", "privacy", "caseUrl",
}
REQUIRED_FIELDS = TOP_FIELDS - {"evidence", "caseUrl"}
CLIENT_FIELDS = {"name", "version", "os", "details"}
TASK_FIELDS = {"verbatim", "namedSkill"}
ENVIRONMENT_FIELDS = {"status", "error"}
ACTIVATION_FIELDS = {"status", "evidence"}
COMPLETION_FIELDS = {"status", "summary"}
PRIVACY_FIELDS = {"scrubbed", "containsSensitiveData"}
EVIDENCE_FIELDS = {"kind", "value"}

ENUMS = {
    "sourceType": {"repository-self-test", "community-report"},
    "client.name": {"codex", "claude-code", "cursor", "other"},
    "task.namedSkill": {"yes", "no", "unknown"},
    "environment.status": {"ok", "blocked", "unknown"},
    "activation.status": {"verified", "not-triggered", "unknown"},
    "completion.status": {"completed", "partial", "waiting-input", "failed", "not-run", "unknown"},
    "evidence.kind": {"log", "output", "link", "note"},
}

SENSITIVE_PATTERNS = (
    ("API key-like value", re.compile(r"\b(?:sk|ghp|github_pat)_[A-Za-z0-9_-]{8,}\b", re.I)),
    ("Bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._~-]{8,}", re.I)),
    ("email address", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
    ("private macOS/Linux path", re.compile(r"/(?:Users|home)/[^/\s]+/")),
    ("private Windows path", re.compile(r"\b[A-Z]:\\Users\\[^\\\s]+\\", re.I)),
)


def repository_skills() -> set[str]:
    data = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))
    return {item["name"] for item in data["skills"] if item.get("ours")}


def _object(value, path: str, allowed: set[str], required: set[str], errors: list[str]):
    if not isinstance(value, dict):
        errors.append(f"{path}: must be an object")
        return {}
    missing = sorted(required - set(value))
    extra = sorted(set(value) - allowed)
    if missing:
        errors.append(f"{path}: missing fields: {', '.join(missing)}")
    if extra:
        errors.append(f"{path}: unknown fields: {', '.join(extra)}")
    return value


def _text(value, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: must be a non-empty string")


def _enum(value, path: str, errors: list[str]) -> None:
    if value not in ENUMS[path]:
        errors.append(f"{path}: expected one of {', '.join(sorted(ENUMS[path]))}")


def _text_list(value, path: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{path}: must be a non-empty array")
        return
    for index, item in enumerate(value):
        _text(item, f"{path}[{index}]", errors)


def _all_public_text(report: dict) -> str:
    return json.dumps(report, ensure_ascii=False)


def validate(report: object) -> list[str]:
    errors: list[str] = []
    report = _object(report, "$", TOP_FIELDS, REQUIRED_FIELDS, errors)
    if not report:
        return errors

    if report.get("schemaVersion") != 1:
        errors.append("schemaVersion: must equal 1")
    if not isinstance(report.get("id"), str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]{7,127}", report["id"]):
        errors.append("id: must be 8-128 lowercase URL-safe characters")
    _enum(report.get("sourceType"), "sourceType", errors)

    recorded_at = report.get("recordedAt")
    _text(recorded_at, "recordedAt", errors)
    if isinstance(recorded_at, str) and recorded_at.strip():
        try:
            parsed = datetime.fromisoformat(recorded_at.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                errors.append("recordedAt: timezone offset is required")
        except ValueError:
            errors.append("recordedAt: must be an ISO 8601 date-time")

    client = _object(report.get("client"), "client", CLIENT_FIELDS, {"name", "version", "os"}, errors)
    _enum(client.get("name"), "client.name", errors)
    _text(client.get("version"), "client.version", errors)
    _text(client.get("os"), "client.os", errors)
    if "details" in client:
        _text(client["details"], "client.details", errors)

    skill = report.get("skill")
    _text(skill, "skill", errors)
    if isinstance(skill, str) and skill not in repository_skills():
        errors.append(f"skill: {skill!r} is not one of this repository's maintained skills")

    task = _object(report.get("task"), "task", TASK_FIELDS, TASK_FIELDS, errors)
    _text(task.get("verbatim"), "task.verbatim", errors)
    _enum(task.get("namedSkill"), "task.namedSkill", errors)

    environment = _object(report.get("environment"), "environment", ENVIRONMENT_FIELDS, {"status"}, errors)
    _enum(environment.get("status"), "environment.status", errors)
    if "error" in environment:
        _text(environment["error"], "environment.error", errors)

    activation = _object(report.get("activation"), "activation", ACTIVATION_FIELDS, ACTIVATION_FIELDS, errors)
    _enum(activation.get("status"), "activation.status", errors)
    _text(activation.get("evidence"), "activation.evidence", errors)

    completion = _object(report.get("completion"), "completion", COMPLETION_FIELDS, COMPLETION_FIELDS, errors)
    _enum(completion.get("status"), "completion.status", errors)
    _text(completion.get("summary"), "completion.summary", errors)

    _text_list(report.get("observed"), "observed", errors)
    _text_list(report.get("boundaries"), "boundaries", errors)

    evidence = report.get("evidence", [])
    if not isinstance(evidence, list):
        errors.append("evidence: must be an array")
    else:
        for index, item in enumerate(evidence):
            item = _object(item, f"evidence[{index}]", EVIDENCE_FIELDS, EVIDENCE_FIELDS, errors)
            _enum(item.get("kind"), "evidence.kind", errors)
            _text(item.get("value"), f"evidence[{index}].value", errors)
            if item.get("kind") == "link" and isinstance(item.get("value"), str):
                url = urlparse(item["value"])
                if url.scheme not in {"http", "https"} or not url.netloc:
                    errors.append(f"evidence[{index}].value: link must use http or https")

    privacy = _object(report.get("privacy"), "privacy", PRIVACY_FIELDS, PRIVACY_FIELDS, errors)
    if privacy.get("scrubbed") is not True:
        errors.append("privacy.scrubbed: must be true before publication")
    if privacy.get("containsSensitiveData") is not False:
        errors.append("privacy.containsSensitiveData: must be false before publication")

    if "caseUrl" in report:
        url = urlparse(report["caseUrl"]) if isinstance(report["caseUrl"], str) else None
        if not url or url.scheme not in {"http", "https"} or not url.netloc:
            errors.append("caseUrl: must use http or https")

    if environment.get("status") == "blocked":
        if activation.get("status") != "unknown":
            errors.append("environment blocked: activation.status must be unknown")
        if completion.get("status") != "not-run":
            errors.append("environment blocked: completion.status must be not-run")
        if not environment.get("error"):
            errors.append("environment blocked: environment.error is required")
    elif completion.get("status") == "not-run":
        errors.append("completion.status not-run requires environment.status blocked")

    public_text = _all_public_text(report)
    for label, pattern in SENSITIVE_PATTERNS:
        if pattern.search(public_text):
            errors.append(f"privacy scan: found {label}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate one compatibility report")
    parser.add_argument("report", type=Path, help="path to a JSON report")
    args = parser.parse_args()

    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"compatibility report invalid: {exc}", file=sys.stderr)
        return 1

    errors = validate(report)
    if errors:
        print("compatibility report invalid:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"compatibility report OK: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
