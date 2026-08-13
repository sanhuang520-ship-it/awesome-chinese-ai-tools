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
        self.assertIn("Claude Code / Cursor 待测", self.expected["description"])
        self.assertEqual(20, len(self.expected["topics"]))
        for topic in ("ai-skills", "agent-skill", "chinese-skills", "codex-skill", "skills"):
            self.assertIn(topic, self.expected["topics"])
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
