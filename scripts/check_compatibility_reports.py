#!/usr/bin/env python3
"""Validate every submitted compatibility report with clear per-file output."""

import json
import sys
from pathlib import Path

from check_compatibility_report import validate


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "compatibility-reports"


def check_directory(directory: Path = REPORTS) -> list[str]:
    errors = []
    paths = sorted(directory.glob("*.json"))
    for path in paths:
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: invalid JSON: {exc}")
            continue
        for error in validate(report):
            errors.append(f"{path.name}: {error}")
    return errors


def main() -> int:
    paths = sorted(REPORTS.glob("*.json"))
    errors = check_directory()
    if errors:
        print("compatibility reports invalid:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"compatibility reports OK: {len(paths)} submitted JSON file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
