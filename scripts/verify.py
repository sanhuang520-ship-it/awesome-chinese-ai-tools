#!/usr/bin/env python3
"""Run the repository's local, network-free verification suite."""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TEST_MODULES = sorted(path.stem for path in SCRIPTS.glob("test_*.py"))


def run(label: str, command: list[str], cwd: Path = ROOT) -> None:
    print(f"\n== {label} ==", flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def main() -> None:
    run("public metadata sync check", [sys.executable, "scripts/sync_public_metadata.py", "."])
    run("third-party catalog claims", [sys.executable, "scripts/check_catalog_claims.py"])
    run("compatibility data", [sys.executable, "scripts/check_compatibility.py"])
    run("submitted compatibility reports", [sys.executable, "scripts/check_compatibility_reports.py"])
    run("quality data", [sys.executable, "scripts/check_quality.py"])
    run("crawlable static catalog", [sys.executable, "scripts/render_static_catalog.py", "--check"])
    run("published internal links", [sys.executable, "scripts/check_internal_links.py"])
    run("unit tests", [sys.executable, "-m", "unittest", *TEST_MODULES], cwd=SCRIPTS)
    print(f"\nverification OK: {len(TEST_MODULES)} test modules")


if __name__ == "__main__":
    main()
