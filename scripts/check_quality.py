#!/usr/bin/env python3
"""Validate static quality and safety metadata for repository-owned skills."""

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "quality.json"
SCRIPT_SUFFIXES = {".py", ".js", ".mjs", ".cjs", ".sh", ".bash", ".zsh", ".ps1"}
TEXT_SUFFIXES = {".html", ".css", ".js", ".mjs", ".cjs"}
RUNTIME_URL_RE = re.compile(
    r"(?:\b(?:src|href)\s*=\s*['\"]https?://|"
    r"\b(?:import|export)\s+(?:[^;]*?\s+from\s+)?['\"]https?://|"
    r"<script\b[^>]*type\s*=\s*['\"]importmap['\"][^>]*>[\s\S]*?https?://|"
    r"\b(?:fetch|WebSocket|EventSource)\s*\(\s*['\"]https?://|"
    r"\burl\(\s*['\"]?https?://)",
    re.I,
)


def fail(message: str) -> None:
    print(f"quality check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def classify_files(root: Path) -> str:
    extras = [path.relative_to(root) for path in root.rglob("*") if path.is_file() and path.name != "SKILL.md"]
    if not extras:
        return "instructions-only"
    if all(path.parts[0] == "references" for path in extras):
        return "instructions+references"
    if all(path.parts[0] == "design-md" and path.name == "DESIGN.md" for path in extras):
        return "instructions+templates"
    names = {path.as_posix() for path in extras}
    if names == {"demo.html", "themes.css"}:
        return "instructions+local demo assets"
    if extras and all(path.suffix.lower() == ".html" for path in extras):
        return "instructions+browser demos"
    return "unclassified"


def runtime_network_evidence(root: Path) -> list[str]:
    evidence = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if RUNTIME_URL_RE.search(path.read_text(encoding="utf-8")):
            evidence.append(path.relative_to(root).as_posix())
    return sorted(evidence)


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    actual = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    recorded = set(data["skills"])
    if actual != recorded:
        fail(f"skill set differs: missing={sorted(actual-recorded)}, extra={sorted(recorded-actual)}")

    for name, item in data["skills"].items():
        root = ROOT / "skills" / name
        skill_file = root / "SKILL.md"
        skill_text = skill_file.read_text(encoding="utf-8")
        frontmatter = re.match(r"^---\n(.*?)\n---\n", skill_text, re.S)
        if not frontmatter:
            fail(f"{name}: missing YAML frontmatter")
        recorded_name = re.search(r"^name:\s*['\"]?([^'\"\n]+)", frontmatter.group(1), re.M)
        if not recorded_name or recorded_name.group(1).strip() != name:
            fail(f"{name}: frontmatter name does not match directory")

        symlinks = [path.relative_to(ROOT).as_posix() for path in root.rglob("*") if path.is_symlink()]
        if symlinks:
            fail(f"{name}: symbolic links require manual review: {symlinks}")

        missing_refs = []
        for link in re.findall(r"\[[^]]*\]\(([^)]+)\)", skill_text):
            if re.match(r"^[a-z]+://", link) or link.startswith("#"):
                continue
            target = (root / link).resolve()
            if not target.exists() or root.resolve() not in (target, *target.parents):
                missing_refs.append(link)
        if missing_refs:
            fail(f"{name}: missing or escaping local references: {missing_refs}")

        scripts = [
            path.relative_to(ROOT).as_posix()
            for path in root.rglob("*")
            if path.is_file() and path.suffix.lower() in SCRIPT_SUFFIXES
        ]
        if bool(scripts) != bool(item["executableScripts"]):
            fail(f"{name}: executableScripts={item['executableScripts']}, discovered={scripts}")

        actual_files = classify_files(root)
        if item.get("files") != actual_files:
            fail(f"{name}: files={item.get('files')!r}, discovered={actual_files!r}")

        runtime_evidence = runtime_network_evidence(root)
        if bool(item.get("runtimeNetwork")) != bool(runtime_evidence):
            fail(f"{name}: runtimeNetwork={item.get('runtimeNetwork')}, discovered={runtime_evidence}")
        if runtime_evidence and (not item.get("networkDetail") or not item.get("networkDetailZh")):
            fail(f"{name}: runtime network evidence requires English and Chinese details")

    guofeng = data["skills"]["guofeng-threejs"]
    demos = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "skills" / "guofeng-threejs").glob("*.html"))
    if guofeng["runtimeNetwork"] and "https://unpkg.com/three@0.170.0/" not in demos:
        fail("guofeng-threejs network dependency evidence is no longer present")

    print(f"quality data OK: {len(actual)} repository-owned skills; names, file layouts, local refs, symlinks, scripts and runtime network checked")


if __name__ == "__main__":
    main()
