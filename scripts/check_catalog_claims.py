#!/usr/bin/env python3
"""Reject unstable or unverified claims in public third-party Skill summaries."""

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "skills.json"

RULES = {
    "dynamic Star ranking": re.compile(
        r"(?:目前|当前|now|currently).{0,18}(?:star|stars|星).{0,18}(?:最高|第一|top|highest)"
        r"|(?:star|stars|星).{0,18}(?:最高|第一|top|highest)"
        r"|(?:最高|第一|top|highest).{0,18}(?:star|stars|星)",
        re.I,
    ),
    "embedded Star total": re.compile(
        r"(?:\d[\d,.]*|[一二三四五六七八九十百千万]+)\s*(?:万|千|[kKmM])?\s*[+＋]?\s*(?:star|stars|星|⭐)",
        re.I,
    ),
    "install-versus-Star comparison": re.compile(
        r"(?:安装|下载|installs?|downloads?).{0,28}(?:star|stars|星|⭐)"
        r"|(?:star|stars|星|⭐).{0,28}(?:安装|下载|installs?|downloads?)",
        re.I,
    ),
    "numeric outcome claim": re.compile(
        r"(?:准确率|成功率|检测率|AI\s*率|提升|降低|减少|从|accuracy|success rate|detection rate|reduce[ds]?|improve[ds]?)"
        r".{0,28}\d+(?:\.\d+)?\s*%"
        r"|\d+(?:\.\d+)?\s*%.{0,28}(?:准确率|成功率|检测率|AI\s*率|提升|降低|减少|降至|降到|accuracy|success rate|detection rate)",
        re.I,
    ),
}


def find_claim_violations(data: dict) -> list[str]:
    violations = []
    for skill in data.get("skills", []):
        if skill.get("ours"):
            continue
        for field in ("desc", "descEn"):
            value = skill.get(field, "")
            for label, pattern in RULES.items():
                if pattern.search(value):
                    violations.append(f"{skill.get('name', '<unnamed>')}.{field}: {label}")
    return violations


def main() -> int:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    violations = find_claim_violations(data)
    if violations:
        print("catalog claim check failed:", file=sys.stderr)
        for violation in violations:
            print(f"- {violation}", file=sys.stderr)
        print(
            "Rewrite as a stable capability summary. If an upstream outcome case matters, "
            "attribute it and state that this repository did not independently reproduce it.",
            file=sys.stderr,
        )
        return 1
    print(f"catalog claims OK: {len(data.get('skills', []))} Skill entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
