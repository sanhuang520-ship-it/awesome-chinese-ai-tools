#!/usr/bin/env python3
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ChineseAgentSkillsPageTest(unittest.TestCase):
    def setUp(self):
        self.body = (ROOT / "chinese-agent-skills" / "index.html").read_text(encoding="utf-8")
        skills = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))["skills"]
        self.entries = len(skills)
        self.repos = len({
            "/".join(item["url"].split("github.com/")[1].split("/")[:2]).lower()
            for item in skills
            if "github.com/" in item.get("url", "")
        })

    def test_search_terms_are_used_as_truthful_positioning(self):
        # 这一页是纯手写静态页（没有生成脚本），数字必须跟 data/skills.json 对得上。
        # 现算不写死：写死的话每次增删 Skill 都要回来改测试，而且改的是抄写不是验证。
        for phrase in ("Chinese Agent Skills", "Chinese AI Skills", str(self.entries),
                       f"{self.repos} source repositories", "13 first-party Skills"):
            self.assertIn(phrase, self.body)

    def test_install_evidence_and_contribution_paths_are_actionable(self):
        for phrase in ("npx skills add", "../try-agent-skills/", "../audit-skill/", "../method/", "../fix-agent-skill/", "../contribute/"):
            self.assertIn(phrase, self.body)

    def test_cross_client_and_accuracy_boundaries_are_explicit(self):
        for phrase in ("Claude Code and Cursor task-level compatibility are still untested", "not an overall accuracy rate", "cross-client guarantee"):
            self.assertIn(phrase, self.body)

    def test_metadata_and_structured_data_are_complete(self):
        for token in ('rel="canonical"', 'hreflang="zh-CN"', 'property="og:title"', 'name="twitter:card"'):
            self.assertIn(token, self.body)
        payload = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', self.body, re.S).group(1))
        self.assertEqual("CollectionPage", payload["@type"])
        self.assertEqual(self.entries, payload["mainEntity"]["numberOfItems"])

if __name__ == "__main__":
    unittest.main()
