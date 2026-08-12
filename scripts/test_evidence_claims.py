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

    def test_first_party_tool_copy_avoids_unmeasured_superlatives(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        tools = (ROOT / "data" / "tools.json").read_text(encoding="utf-8")
        forbidden = ["国内最好用", "效果最佳", "国内最强", "效果最准", "减少 70%", "完全免费，无限次"]
        for claim in forbidden:
            with self.subTest(claim=claim):
                self.assertNotIn(claim, index + tools)

    def test_commercial_terms_are_presented_as_unverified_history(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        tools = (ROOT / "data" / "tools.json").read_text(encoding="utf-8")
        self.assertIn('"status": "unverified-snapshot"', tools)
        self.assertIn("链接存活不代表商业条款仍有效", tools)
        self.assertIn("这里是发现线索，不是实时价格库", index)
        self.assertIn("不会验证价格、额度、地区或账号资格", index)
        self.assertNotIn("t.priceFree", index)
        self.assertNotIn("t.pricePro", index)

    def test_tool_descriptions_avoid_unmeasured_ranking_language(self):
        tools = (ROOT / "data" / "tools.json").read_text(encoding="utf-8")
        forbidden = ["顶级", "最大", "最稳定", "最自然", "远超", "神器", "当天可上线", "无限生成"]
        for claim in forbidden:
            with self.subTest(claim=claim):
                self.assertNotIn(claim, tools)

    def test_retired_editorial_scores_do_not_drive_the_frontend(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        tools = (ROOT / "data" / "tools.json").read_text(encoding="utf-8")
        self.assertIn('"status": "retired"', tools)
        self.assertIn("不再用于前端徽章、评分、筛选或排序", tools)
        forbidden = ["t.stars", "t.rec", "t.hot", "onlyRec", "onlyHot", "编辑精选", "按精选程度和热度排序"]
        for claim in forbidden:
            with self.subTest(claim=claim):
                self.assertNotIn(claim, index)

    def test_skill_install_counts_are_not_called_actual_usage(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        skills = (ROOT / "data" / "skills.json").read_text(encoding="utf-8")
        self.assertIn("不等于独立用户或实际使用次数", index)
        self.assertIn('"status": "retired"', skills)
        self.assertNotIn("星数远低于实际使用量", index)
        self.assertNotIn("s.rec && !s.ours", index)


if __name__ == "__main__":
    unittest.main()
