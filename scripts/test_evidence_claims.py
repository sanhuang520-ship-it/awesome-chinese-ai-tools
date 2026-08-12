#!/usr/bin/env python3

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = [
    ROOT / "README.md",
    ROOT / "SKILLS.md",
    ROOT / "index.html",
    ROOT / "blog" / "skill-pitfalls.md",
]


class EvidenceClaimsTest(unittest.TestCase):
    def test_installation_evidence_is_not_called_official_or_activation(self):
        combined = "\n".join(path.read_text(encoding="utf-8") for path in PUBLIC_FILES)
        forbidden = [
            "这个官方 CLI",
            "用官方 CLI 实测",
            "Claude Code 读的是 `~/.claude/skills/`",
            "装好后重启 Claude Code，**无需手动调用**",
        ]
        for claim in forbidden:
            with self.subTest(claim=claim):
                self.assertNotIn(claim, combined)

    def test_unknown_clients_remain_explicitly_unverified(self):
        compatibility = (ROOT / "COMPATIBILITY.md").read_text(encoding="utf-8")
        self.assertIn("| Claude Code | ⏳ 待测 |", compatibility)
        self.assertIn("| Cursor | ⏳ 待测 |", compatibility)


if __name__ == "__main__":
    unittest.main()
