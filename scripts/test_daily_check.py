#!/usr/bin/env python3

import importlib.util
import base64
import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_daily_check():
    spec = importlib.util.spec_from_file_location("daily_check_for_test", ROOT / "scripts" / "daily_check.py")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(os.environ, {"GITHUB_TOKEN": "test-token"}):
        spec.loader.exec_module(module)
    return module


class DailyCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_daily_check()

    def test_same_day_without_status_changes_does_not_write(self):
        self.assertFalse(self.module.should_persist_tool_check(0, "2026-08-12", "2026-08-12"))

    def test_new_observation_day_writes_even_without_status_changes(self):
        self.assertTrue(self.module.should_persist_tool_check(0, "2026-08-11", "2026-08-12"))

    def test_status_change_always_writes(self):
        self.assertTrue(self.module.should_persist_tool_check(1, "2026-08-12", "2026-08-12"))

    def test_skill_repository_count_deduplicates_subdirectory_urls(self):
        skills = [
            {"url": "https://github.com/anthropics/skills/tree/main/skills/pdf"},
            {"url": "https://github.com/anthropics/skills/tree/main/skills/docx"},
            {"url": "https://github.com/example/one"},
        ]
        self.assertEqual({"anthropics/skills", "example/one"}, self.module.unique_skill_repositories(skills))

    def test_generated_catalog_keeps_preinstall_audit_entry(self):
        source = (ROOT / "data" / "skills.json").read_bytes()
        quality = (ROOT / "data" / "quality.json").read_bytes()
        captured = {}

        def fake_api(method, path, data=None, retries=3):
            if path.endswith("data/skills.json"):
                return {"content": base64.b64encode(source).decode("ascii")}
            if path.endswith("data/quality.json"):
                return {"content": base64.b64encode(quality).decode("ascii")}
            if method == "GET" and path.endswith("SKILLS.md"):
                return {"content": base64.b64encode(b"outdated").decode("ascii"), "sha": "old"}
            if method == "PUT" and path.endswith("SKILLS.md"):
                captured["body"] = base64.b64decode(data["content"]).decode("utf-8")
                return {"content": {"sha": "new"}}
            raise AssertionError((method, path))

        with patch.object(self.module, "github_api", side_effect=fake_api):
            self.module.build_skills_md()
        catalog = captured["body"]
        for phrase in ("安装第三方 Skill 前", "audit-skill/", "0 项命中不等于安全"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, catalog)
        self.assertEqual(184, len(json.loads(source)["skills"]))

    def test_generated_originals_expose_decision_labels_and_evidence_pages(self):
        source = (ROOT / "data" / "skills.json").read_bytes()
        quality = (ROOT / "data" / "quality.json").read_bytes()
        captured = {}

        def fake_api(method, path, data=None, retries=3):
            if path.endswith("data/skills.json"):
                return {"content": base64.b64encode(source).decode("ascii")}
            if path.endswith("data/quality.json"):
                return {"content": base64.b64encode(quality).decode("ascii")}
            if method == "GET" and path.endswith("SKILLS.md"):
                return {"content": base64.b64encode(b"outdated").decode("ascii"), "sha": "old"}
            if method == "PUT" and path.endswith("SKILLS.md"):
                captured["body"] = base64.b64decode(data["content"]).decode("utf-8")
                return {"content": {"sha": "new"}}
            raise AssertionError((method, path))

        with patch.object(self.module, "github_api", side_effect=fake_api):
            self.module.build_skills_md()
        catalog = captured["body"]
        for phrase in (
            "以下是安装前静态检查标签，不是安全认证",
            "| Skill | 做什么 | 安装前标签 |",
            "无独立可执行脚本",
            "未发现运行时联网",
            "浏览器 Demo 从 unpkg.com 加载 three@0.170.0",
            "https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/typography/",
            "[源码](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-typography)",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, catalog)

    def test_catalog_quality_label_does_not_hide_future_script_or_network_risk(self):
        label = self.module.catalog_quality_label({
            "filesZh": "说明与脚本",
            "executableScripts": True,
            "runtimeNetwork": True,
            "networkDetailZh": "运行时请求 example.com",
            "sensitiveBoundaryZh": "先在隔离环境复核",
        })
        self.assertIn("发现独立可执行脚本，安装前需人工复核", label)
        self.assertIn("运行时请求 example.com", label)
        self.assertIn("**边界：**先在隔离环境复核", label)


if __name__ == "__main__":
    unittest.main()
