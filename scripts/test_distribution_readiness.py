#!/usr/bin/env python3
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DistributionReadinessTest(unittest.TestCase):
    def test_first_party_skill_improvement_has_a_distinct_private_safe_route(self):
        template = (ROOT / ".github" / "ISSUE_TEMPLATE" / "improve-skill.yml").read_text(encoding="utf-8")
        for phrase in (
            "改进一个本站原创 Skill",
            "这是实际任务反馈",
            "合成示例",
            "截图不是必需的",
            "我已删除 Token、邮箱、私人路径和未公开业务数据",
            "不等于所有客户端或版本都会复现",
        ):
            self.assertIn(phrase, template)
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("template=improve-skill.yml", contributing)
        self.assertIn("template=improve-skill.yml", readme)

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

    def test_update_launch_copy_is_unpublished_and_preserves_fixture_boundaries(self):
        body = (ROOT / "promo" / "update-agent-skill-posts.md").read_text(encoding="utf-8")
        self.assertIn("状态：**未发布**", body)
        self.assertIn("skills@1.5.22 update -p -y", body)
        self.assertIn("受控测试夹具", body)
        self.assertIn("没有测试全局", body)
        self.assertIn("发布操作需用户当时确认", body)
        self.assertIn("Clone 不能称为用户", body)
        index = (ROOT / "promo" / "README.md").read_text(encoding="utf-8")
        self.assertIn("promo/update-agent-skill-posts.md", index)
        self.assertIn("当前首选", index)

    def test_bundles_launch_copy_is_unpublished_and_avoids_rank_claims(self):
        body = (ROOT / "promo" / "bundles-launch-posts.md").read_text(encoding="utf-8")
        self.assertIn("状态：**未发布**", body)
        self.assertIn("发布操作需用户当时确认", body)
        self.assertIn("不代表同时触发或跨客户端认证", body)
        self.assertIn("Clone 不能称为用户", body)
        self.assertNotIn("最佳 Agent Skills", body)
        self.assertNotIn("必装 Skill", body)
        index = (ROOT / "promo" / "README.md").read_text(encoding="utf-8")
        self.assertIn("promo/bundles-launch-posts.md", index)

    def test_machine_readable_record_has_no_false_publication_or_attribution(self):
        data = json.loads((ROOT / "metrics" / "2026-08-13-distribution-readiness.json").read_text(encoding="utf-8"))
        self.assertEqual("not-published", data["preparedContent"]["status"])
        self.assertEqual(2, len(data["verifiedListings"]))
        self.assertIn("No external form", data["notes"])
        self.assertIn("cannot be attributed", data["notes"])
        self.assertTrue(all(item["status"].startswith("deferred-") for item in data["candidateChannels"]))


if __name__ == "__main__":
    unittest.main()
