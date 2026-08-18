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
        """
        目的是验证「不管原来写的步骤编号是几，行本身会被换成当天真实统计」——
        不是验证某天具体查到多少个工具被拦截。之前把 39/5/2 这几个数字焊死在测试里，
        而这三个数字来自当天对外部网站的真实探活，站点自己加个机器人验证第二天数字
        就会变，跟仓库代码有没有 bug 无关。2026-08-16 就撞上了（39→38，5→6）。
        改成从 self.stats 里现取现拼，只测模板和替换逻辑对不对。
        """
        original = "| 2 | 999 个工具链接实测可访问性 |\n"
        n, direct_ok, bot_blocked, whitelisted = (
            self.stats["tools"], self.stats["tools_direct_ok"],
            self.stats["tools_bot_blocked"], self.stats["tools_whitelisted"],
        )
        self.assertEqual(
            f"| 2 | {n} 个工具入口复检：{direct_ok} 个直接成功，"
            f"{bot_blocked} 个返回机器人拦截响应，{whitelisted} 个白名单跳过请求 |\n",
            sync_readme_text(original, self.stats),
        )

    def test_every_nonempty_category_is_rendered(self):
        skills = json.loads((ROOT / "data/skills.json").read_text(encoding="utf-8"))["skills"]
        used_categories = {item.get("cat") for item in skills}
        self.assertEqual(used_categories, set(CAT_ORDER))

    def test_skill_entries_and_source_repositories_are_distinct_counts(self):
        """
        要守的是「条目数」和「来源仓库数」是两个不同口径、且 build_stats 算得对——
        不是某天恰好是 194/151。之前把当天数字写死在这里，结果每次增删 skill
        都得回来改一遍测试（08-14 改成 195/152，08-17 又改成 194/151），
        而这种改动纯属抄写，不构成任何验证。改成从 data/skills.json 现场推导。
        """
        skills = json.loads((ROOT / "data/skills.json").read_text(encoding="utf-8"))["skills"]
        expected_repos = {
            "/".join(item["url"].split("github.com/")[1].split("/")[:2]).lower()
            for item in skills
            if "github.com/" in item.get("url", "")
        }
        self.assertEqual(len(skills), self.stats["skills"])
        self.assertEqual(len(expected_repos), self.stats["repos"])
        # 多个 Skill 可以来自同一个仓库，所以仓库数必须严格小于条目数；
        # 如果两者相等，说明去重逻辑失效了。
        self.assertLess(self.stats["repos"], self.stats["skills"])

    def test_tool_link_statuses_are_counted_by_evidence_type(self):
        """
        真正要守住的不变量是「三类状态加起来等于工具总数」——分类不能漏掉或算重。
        具体 39/5/2 这种精确值是当天对外部网站真实探活的结果，第二天完全可能因为
        对方网站行为变化而不同，不是这里的逻辑错了，硬编码这几个数字迟早天天报红。
        """
        self.assertGreaterEqual(self.stats["tools_direct_ok"], 0)
        self.assertGreaterEqual(self.stats["tools_bot_blocked"], 0)
        self.assertGreaterEqual(self.stats["tools_whitelisted"], 0)
        self.assertEqual(
            self.stats["tools"],
            self.stats["tools_direct_ok"] + self.stats["tools_bot_blocked"] + self.stats["tools_whitelisted"],
        )

    def test_index_metadata_uses_entry_and_repository_units(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        synced = sync_index_text(index, self.stats)
        # 同样从 self.stats 取，避免每次增删 skill 都要回来改这两个数字
        self.assertIn(f"{self.stats['cn']} 个中文条目", synced)
        self.assertIn(f"来自 {self.stats['repos']} 个来源仓库", synced)
        # 「项目」是旧口径（把条目说成项目），换成「条目」之后不该再出现
        self.assertNotIn("个中文项目", synced)
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
