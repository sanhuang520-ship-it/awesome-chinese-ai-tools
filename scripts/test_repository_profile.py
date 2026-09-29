#!/usr/bin/env python3
import json
import ssl
import unittest
from pathlib import Path

from check_repository_profile import compare_profile, ssl_context


ROOT = Path(__file__).resolve().parents[1]


class RepositoryProfileTest(unittest.TestCase):
    def setUp(self):
        self.expected = json.loads((ROOT / "data" / "repository-profile.json").read_text(encoding="utf-8"))
        self.actual = {
            "full_name": self.expected["repository"],
            "description": self.expected["description"],
            "homepage": self.expected["homepage"],
            "topics": list(reversed(self.expected["topics"])),
        }

    def test_committed_profile_is_precise_and_not_a_growth_claim(self):
        self.assertEqual(1, self.expected["schemaVersion"])
        self.assertIn("中文 Agent Skills 合集", self.expected["description"])
        # 与分享图口径一致：Claude Code 只测到发现与加载，Cursor 一个字没测。
        self.assertIn("Claude Code 部分实测 · Cursor 待测", self.expected["description"])
        self.assertNotIn("Claude Code 已实测", self.expected["description"])

    def test_description_counts_match_catalog_data(self):
        # 2026-09-13 发现线上描述停在「194 个条目」，而数据早已是 211。
        # 描述里的数字是手写的，此前没有任何检查会发现它和数据对不上。
        skills = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))["skills"]
        ours = sum(1 for item in skills if item.get("ours"))
        self.assertIn(f"{len(skills)} 个条目", self.expected["description"])
        self.assertIn(f"{ours} 个本站原创", self.expected["description"])
        self.assertEqual(15, len(self.expected["topics"]))
        self.assertIn("not evidence of ranking or Star growth", self.expected["notes"])
        self.assertEqual([], compare_profile(self.expected, self.actual))

    def test_checker_reports_each_drifted_field(self):
        self.actual["description"] = "stale"
        self.actual["topics"] = []
        self.assertEqual(["description", "topics"], compare_profile(self.expected, self.actual))

    def test_checker_builds_a_verifying_ssl_context(self):
        self.assertEqual(ssl.CERT_REQUIRED, ssl_context().verify_mode)


if __name__ == "__main__":
    unittest.main()
