#!/usr/bin/env python3
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DistributionReadinessTest(unittest.TestCase):
    def test_directory_ledger_prevents_duplicate_submission(self):
        body = (ROOT / "promo" / "directory-submissions.md").read_text(encoding="utf-8")
        self.assertIn("Agent-Skills.md", body)
        self.assertIn("已提交、已收录、已验证", body)
        self.assertIn("不重复提交", body)
        self.assertIn("real community usage", body)
        self.assertIn("Clone 不能叫用户", body)

    def test_audit_launch_copy_is_unpublished_and_preserves_boundaries(self):
        body = (ROOT / "promo" / "audit-skill-launch-posts.md").read_text(encoding="utf-8")
        self.assertIn("状态：**未发布**", body)
        self.assertIn("不会执行目标", body)
        self.assertIn("0 项命中绝不等于安全", body)
        self.assertIn("Linux.do 不使用本稿", body)
        self.assertIn("发布操作需用户当时确认", body)

    def test_machine_readable_record_has_no_false_publication_or_attribution(self):
        data = json.loads((ROOT / "metrics" / "2026-08-13-distribution-readiness.json").read_text(encoding="utf-8"))
        self.assertEqual("not-published", data["preparedContent"]["status"])
        self.assertEqual(2, len(data["verifiedListings"]))
        self.assertIn("No external form", data["notes"])
        self.assertIn("cannot be attributed", data["notes"])
        self.assertTrue(all(item["status"].startswith("deferred-") for item in data["candidateChannels"]))


if __name__ == "__main__":
    unittest.main()
