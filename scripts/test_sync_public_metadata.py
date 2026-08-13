#!/usr/bin/env python3
"""公开统计一致性检查。"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from sync_public_metadata import (
    CAT_ORDER,
    build_stats,
    sync_index_text,
    sync_english_readme_text,
    sync_llms_text,
    sync_local,
    sync_readme_text,
    sync_sitemap_text,
)


ROOT = Path(__file__).resolve().parents[1]


class PublicMetadataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        skills = json.loads((ROOT / "data/skills.json").read_text(encoding="utf-8"))
        tools = json.loads((ROOT / "data/tools.json").read_text(encoding="utf-8"))
        cls.stats = build_stats(skills, tools)

    def test_committed_files_are_in_sync(self):
        cases = {
            "README.md": lambda text: sync_readme_text(text, self.stats),
            "README.en.md": lambda text: sync_english_readme_text(text, self.stats),
            "index.html": lambda text: sync_index_text(text, self.stats),
            "llms.txt": lambda text: sync_llms_text(text, self.stats),
            "sitemap.xml": lambda text: sync_sitemap_text(text, self.stats["checked"]),
        }
        for relative, transform in cases.items():
            with self.subTest(path=relative):
                current = (ROOT / relative).read_text(encoding="utf-8")
                self.assertEqual(current, transform(current))

    def test_sitemap_does_not_touch_static_directory_pages(self):
        original = (
            "<url><loc>https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/themes/</loc>"
            "<lastmod>2026-01-01</lastmod></url>\n"
        )
        self.assertEqual(original, sync_sitemap_text(original, "2026-08-12"))

    def test_sitemap_core_lastmod_never_moves_backwards(self):
        original = (
            "<url><loc>https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/</loc>"
            "<lastmod>2026-08-13</lastmod></url>\n"
        )
        self.assertEqual(original, sync_sitemap_text(original, "2026-08-12"))

    def test_sitemap_core_lastmod_moves_forward_with_newer_data(self):
        original = (
            "<url><loc>https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/</loc>"
            "<lastmod>2026-08-11</lastmod></url>\n"
        )
        expected = original.replace("2026-08-11", "2026-08-12")
        self.assertEqual(expected, sync_sitemap_text(original, "2026-08-12"))

    def test_readme_step_number_does_not_affect_tool_count_sync(self):
        original = "| 2 | 999 个工具链接实测可访问性 |\n"
        self.assertEqual(
            "| 2 | 46 个工具入口复检：39 个直接成功，5 个返回机器人拦截响应，2 个白名单跳过请求 |\n",
            sync_readme_text(original, self.stats),
        )

    def test_every_nonempty_category_is_rendered(self):
        skills = json.loads((ROOT / "data/skills.json").read_text(encoding="utf-8"))["skills"]
        used_categories = {item.get("cat") for item in skills}
        self.assertEqual(used_categories, set(CAT_ORDER))

    def test_skill_entries_and_source_repositories_are_distinct_counts(self):
        self.assertEqual(184, self.stats["skills"])
        self.assertEqual(141, self.stats["repos"])
        self.assertLess(self.stats["repos"], self.stats["skills"])

    def test_tool_link_statuses_are_counted_by_evidence_type(self):
        self.assertEqual(39, self.stats["tools_direct_ok"])
        self.assertEqual(5, self.stats["tools_bot_blocked"])
        self.assertEqual(2, self.stats["tools_whitelisted"])
        self.assertEqual(
            self.stats["tools"],
            self.stats["tools_direct_ok"] + self.stats["tools_bot_blocked"] + self.stats["tools_whitelisted"],
        )

    def test_index_metadata_uses_entry_and_repository_units(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        synced = sync_index_text(index, self.stats)
        self.assertIn("68 个中文条目", synced)
        self.assertIn("来自 141 个来源仓库", synced)
        self.assertNotIn("68 个中文项目", synced)
        self.assertIn("Chinese Agent Skills / 中文 AI Skills 库", synced)
        self.assertIn("Chinese Agent Skills / 中文 AI Skills 合集", synced)

    def test_local_check_reports_drift_without_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "data").mkdir()
            for relative in ("data/skills.json", "data/tools.json", "README.md", "README.en.md", "index.html", "llms.txt", "sitemap.xml"):
                source = ROOT / relative
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            readme = root / "README.md"
            stale = readme.read_text(encoding="utf-8").replace("46 个 AI 工具导航", "999 个 AI 工具导航")
            readme.write_text(stale, encoding="utf-8")

            _, changed = sync_local(root)
            self.assertEqual(["README.md"], changed)
            self.assertIn("999 个 AI 工具导航", readme.read_text(encoding="utf-8"))

            _, written = sync_local(root, write=True)
            self.assertEqual(["README.md"], written)
            self.assertIn("46 个 AI 工具导航", readme.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
