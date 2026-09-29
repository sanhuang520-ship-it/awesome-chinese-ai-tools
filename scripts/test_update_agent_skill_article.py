#!/usr/bin/env python3
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class UpdateAgentSkillArticleTest(unittest.TestCase):
    def setUp(self):
        self.body = (ROOT / "update-agent-skill" / "index.html").read_text(encoding="utf-8")

    def test_command_preconditions_and_full_folder_verification_are_visible(self):
        for phrase in (
            "npx --yes skills@1.5.22 update -p -y",
            "test -f skills-lock.json",
            "diff -qr skills/&lt;name&gt; .agents/skills/&lt;name&gt;",
            "13/13 完整文件夹一致",
        ):
            self.assertIn(phrase, self.body)

    def test_evidence_boundaries_reject_global_and_activation_claims(self):
        for phrase in ("没有运行全局", "无锁文件更新", "自动触发", "不是保留下来的旧版 CLI 安装现场"):
            self.assertIn(phrase, self.body)
        self.assertNotIn("自动更新所有", self.body)

    def test_social_and_faq_metadata_are_complete(self):
        for token in ('rel="canonical"', 'property="og:title"', 'property="og:image"', 'name="twitter:card"'):
            self.assertIn(token, self.body)
        payload = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', self.body, re.S).group(1))
        self.assertEqual(3, len(payload["@graph"][1]["mainEntity"]))


if __name__ == "__main__":
    unittest.main()
