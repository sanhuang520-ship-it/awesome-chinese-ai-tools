#!/usr/bin/env python3
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallJourneyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = (ROOT / "install" / "index.html").read_text(encoding="utf-8")

    def test_install_page_starts_with_pre_install_audit(self):
        audit = self.body.index("安装前，先审计第三方 Skill")
        install = self.body.index("四步安装与核对")
        self.assertLess(audit, install)
        self.assertIn('href="../audit-skill/"', self.body)
        self.assertIn("规则零命中也不等于安全", self.body)

    def test_howto_includes_audit_before_install_steps(self):
        match = re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', self.body, re.S)
        payload = json.loads(match.group(1))
        self.assertEqual("安装前审计", payload["step"][0]["name"])
        self.assertEqual(5, len(payload["step"]))
        self.assertEqual("2026-08-13", payload["dateModified"])

    def test_install_page_discloses_version_cache_and_update_drift(self):
        for phrase in ("安装后不会自动跟随仓库更新", "skills@1.5.22", "0/13 一致", "npx skills --version", "update -p -y", "13/13 与当前仓库完整一致", "没有验证全局"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.body)
        self.assertIn("../update-agent-skill/", self.body)
        update_guide = (ROOT / "update-agent-skill" / "index.html").read_text(encoding="utf-8")
        self.assertIn("../cases/skills-cli-isolated-install-2026-08-13.md", update_guide)

    def test_cross_platform_evidence_steps_do_not_claim_unmeasured_compatibility(self):
        for phrase in (
            "跨系统留证：只记录安装，不猜客户端行为",
            "WINDOWS · PowerShell",
            "WSL / LINUX · shell",
            "Get-Item",
            "不存在也很有价值",
            "不要把“能看到文件”写成“自动触发”",
            "install-environment-result.example.json",
            "check_install_environment_report.py",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.body)


if __name__ == "__main__":
    unittest.main()
