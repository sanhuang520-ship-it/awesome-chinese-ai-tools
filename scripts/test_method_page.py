#!/usr/bin/env python3

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "method" / "index.html"


class MethodPageTest(unittest.TestCase):
    def setUp(self):
        self.body = PAGE.read_text(encoding="utf-8")

    def test_four_evidence_layers_are_distinct(self):
        for label in ("L1 · DISCOVERY", "L2 · INSTALL", "L3 · ACTIVATE", "L4 · DELIVER"):
            self.assertEqual(1, self.body.count(label))
        for claim in ("发现 ≠ 安装", "安装 ≠ 触发", "触发 ≠ 完成"):
            self.assertIn(claim, self.body)

    def test_failure_classification_keeps_environment_errors_separate(self):
        for phrase in ("平台或账户阻断", "不能</strong>记成 Skill 失败", "待用户输入", "缩小复测不能抹掉原失败"):
            self.assertIn(phrase, self.body)

    def test_method_links_to_current_evidence_artifacts(self):
        for path in ("../compatibility/", "../reproduce/", "../retest/", "../QUALITY.md"):
            self.assertIn(f'href="{path}"', self.body)

    def test_structured_data_is_valid_and_contains_faq(self):
        match = re.search(r'<script type="application/ld\+json">(.*?)</script>', self.body, re.S)
        self.assertIsNotNone(match)
        data = json.loads(match.group(1))
        types = {item["@type"] for item in data["@graph"]}
        self.assertEqual({"TechArticle", "FAQPage"}, types)


if __name__ == "__main__":
    unittest.main()
