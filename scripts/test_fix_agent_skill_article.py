#!/usr/bin/env python3
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class FixAgentSkillArticleTest(unittest.TestCase):
    def setUp(self):
        self.body = (ROOT / "fix-agent-skill" / "index.html").read_text(encoding="utf-8")

    def test_evidence_chain_and_fixed_acceptance_are_visible(self):
        for phrase in ("不改题", "不降门槛", "不覆盖旧失败", "完全相同的任务", "原始失败继续保留"):
            self.assertIn(phrase, self.body)

    def test_both_before_after_cases_are_linked(self):
        for path in ("chinese-web-themes-prospective-retest-2026-08-13.md", "chinese-web-themes-remediation-retest-2026-08-13.md", "guofeng-threejs-prospective-retest-2026-08-13.md", "guofeng-threejs-remediation-retest-2026-08-13.md"):
            self.assertIn(path, self.body)
        for phrase in ("初次 3 / 4", "修复后 4 / 4", "408 个 Unicode 字符", "294 个 Unicode 字符"):
            self.assertIn(phrase, self.body)

    def test_social_and_structured_metadata_are_complete(self):
        for token in ('rel="canonical"', 'property="og:title"', 'property="og:image"', 'name="twitter:card"'):
            self.assertIn(token, self.body)
        payload = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', self.body, re.S).group(1))
        self.assertEqual("TechArticle", payload["@graph"][0]["@type"])
        self.assertEqual(3, len(payload["@graph"][1]["mainEntity"]))

    def test_claim_boundaries_are_explicit(self):
        for phrase in ("不是跨客户端保证", "安全认证", "总体准确率"):
            self.assertIn(phrase, self.body)

if __name__ == "__main__":
    unittest.main()
