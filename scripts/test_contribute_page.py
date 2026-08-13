#!/usr/bin/env python3
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ContributePageTest(unittest.TestCase):
    def setUp(self):
        self.body = (ROOT / "contribute" / "index.html").read_text(encoding="utf-8")

    def test_three_real_tasks_have_scope_time_and_completion_gates(self):
        self.assertEqual(3, self.body.count('class="task"'))
        for phrase in ("约 15 分钟", "约 10 分钟", "完成标准", "Claude Code 或 Cursor", "Windows 或 Linux", "第三方目录条目"):
            self.assertIn(phrase, self.body)

    def test_tasks_route_to_structured_submission_paths(self):
        for template in ("compatibility-result.yml", "install-environment-result.yml", "report-problem.yml"):
            self.assertIn(template, self.body)

    def test_privacy_and_claim_boundaries_are_explicit(self):
        for phrase in ("Token、邮箱、私人路径", "成功、失败、未触发", "不外推为准确率", "贡献与 Star 完全独立"):
            self.assertIn(phrase, self.body)

    def test_structured_data_lists_exactly_three_tasks(self):
        payload = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', self.body, re.S).group(1))
        self.assertEqual(3, payload["@graph"][0]["mainEntity"]["numberOfItems"])
        self.assertEqual(3, len(payload["@graph"][0]["mainEntity"]["itemListElement"]))

if __name__ == "__main__":
    unittest.main()
