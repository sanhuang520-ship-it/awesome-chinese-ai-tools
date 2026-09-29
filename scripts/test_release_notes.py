#!/usr/bin/env python3
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ReleaseNotesTest(unittest.TestCase):
    def setUp(self):
        self.body = (ROOT / ".github" / "releases" / "v1.2.0.md").read_text(encoding="utf-8")
        self.snapshot = json.loads((ROOT / "metrics" / "2026-08-13-v1.2.0.json").read_text(encoding="utf-8"))

    def test_release_notes_match_frozen_compatibility_counts(self):
        for phrase in ("10 项完成", "1 项按流程等待必要输入", "2 项大任务失败后缩小复测", "初次 4 条通过、2 条失败", "旧失败保留"):
            self.assertIn(phrase, self.body)
        self.assertEqual(10, self.snapshot["evidenceBoundary"]["compatibilityOutcomes"]["completed"])
        self.assertEqual(2, self.snapshot["evidenceBoundary"]["prospectiveRetests"]["initialFailures"])

    def test_release_notes_keep_client_security_and_growth_boundaries(self):
        for phrase in ("Claude Code 与 Cursor", "不是安全认证", "不是准确率", "Stars 仍为 7", "不能把本版本表述为已经带来 Star 增长"):
            self.assertIn(phrase, self.body)

    def test_release_notes_identify_immutable_tag_and_verification(self):
        for phrase in ("207 项单元测试", "36 个测试模块", "44 个公开 HTML 页面", "ab44cd965d4167e6efb3849876ab5efef670f978"):
            self.assertIn(phrase, self.body)

if __name__ == "__main__":
    unittest.main()
