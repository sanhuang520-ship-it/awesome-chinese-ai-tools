#!/usr/bin/env python3
"""Validate static quality and safety metadata for repository-owned skills."""

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "quality.json"
SCRIPT_SUFFIXES = {".py", ".js", ".mjs", ".cjs", ".sh", ".bash", ".zsh", ".ps1"}


def fail(message: str) -> None:
    print(f"quality check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    actual = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    recorded = set(data["skills"])
    if actual != recorded:
        fail(f"skill set differs: missing={sorted(actual-recorded)}, extra={sorted(recorded-actual)}")

    for name, item in data["skills"].items():
        root = ROOT / "skills" / name
        scripts = [
            path.relative_to(ROOT).as_posix()
            for path in root.rglob("*")
            if path.is_file() and path.suffix.lower() in SCRIPT_SUFFIXES
        ]
        if bool(scripts) != bool(item["executableScripts"]):
            fail(f"{name}: executableScripts={item['executableScripts']}, discovered={scripts}")

    guofeng = data["skills"]["guofeng-threejs"]
    demos = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "skills" / "guofeng-threejs").glob("*.html"))
    if guofeng["runtimeNetwork"] and "https://unpkg.com/three@0.170.0/" not in demos:
        fail("guofeng-threejs network dependency evidence is no longer present")

    print(f"quality data OK: {len(actual)} repository-owned skills")


if __name__ == "__main__":
    main()
