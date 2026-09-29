#!/usr/bin/env python3
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AuditSkillPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = (ROOT / "audit-skill" / "index.html").read_text(encoding="utf-8")

    def test_search_metadata_and_structured_data(self):
        self.assertIn('<meta name="robots" content="index,follow">', self.body)
        self.assertIn('/awesome-chinese-ai-tools/audit-skill/', self.body)
        self.assertIn('property="og:title"', self.body)
        payload = re.search(r'<script type="application/ld\+json">(.*?)</script>', self.body, re.S)
        self.assertEqual("TechArticle", json.loads(payload.group(1))["@type"])

    def test_page_states_read_only_scope_and_limitations(self):
        for phrase in ("不执行目标 Skill", "不上传扫描内容", "不会跟随符号链接", "不是病毒查杀", "0 项命中", "不等于安全"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.body)

    def test_page_links_to_source_tests_and_security_policy(self):
        for href in ("../scripts/audit_skill.py", "../scripts/test_audit_skill.py", "../QUALITY.md", "../SECURITY.md", "../install/", "../reproduce/"):
            self.assertIn(f'href="{href}"', self.body)


if __name__ == "__main__":
    unittest.main()
