#!/usr/bin/env python3
"""公开统计一致性检查。"""

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from sync_public_metadata import (
    CAT_ORDER,
    _transforms,
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

    def test_tool_directory_is_archived_consistently(self):
        """
        2026-09-14 工具导航转为归档快照：不再复检、不再收新工具。
        要守的是「对外说法」与「实际行为」一致——
        维护步骤里没有工具复检，就不许任何页面再宣称工具链接在被复检；
        反过来，如果以后把复检加回去，这条测试会逼着人同时改掉「归档」表述。
        """
        tools = json.loads((ROOT / "data/tools.json").read_text(encoding="utf-8"))
        self.assertEqual("archived", tools["meta"]["archive"]["status"])

        steps = re.search(r"STEPS = \[(.*?)\n    \]", (ROOT / "scripts/daily_check.py").read_text(encoding="utf-8"), re.S).group(1)
        active = [line for line in steps.splitlines() if not line.strip().startswith("#")]
        self.assertFalse(any("check_tool_links" in line for line in active))

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        english = (ROOT / "README.en.md").read_text(encoding="utf-8")
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("个工具入口复检", readme)
        self.assertNotIn("链接定期自动实测", readme)
        self.assertIn("AI 工具导航的归档快照", readme)
        self.assertNotIn("tool links; runs are manually triggered", english)
        self.assertIn("archived snapshot", english)
        self.assertIn("工具导航（归档）", index)
        self.assertIn("归档快照", index)

        # 旧格式的维护表工具行不应再被同步脚本「复活」
        self.assertEqual("| 2 | 999 个工具链接实测可访问性 |\n",
                         sync_readme_text("| 2 | 999 个工具链接实测可访问性 |\n", self.stats))

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
            # 要复制的文件直接从 _transforms 取，不再手写清单：
            # 以前是硬编码的一串路径，新增同步文件时忘了加进来，这个测试就会
            # FileNotFoundError（08-18 加 chinese-agent-skills/index.html 时正好撞上）。
            synced_files = tuple(_transforms(build_stats(
                json.loads((ROOT / "data/skills.json").read_text(encoding="utf-8")),
                json.loads((ROOT / "data/tools.json").read_text(encoding="utf-8")),
            )))
            for relative in ("data/skills.json", "data/tools.json") + synced_files:
                source = ROOT / relative
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            readme = root / "README.md"
            # 不写死工具数：加一个工具这里就会失效，而"抄一遍当前数字"验证不了任何东西
            # （08-31 加第 47 个工具时正好撞上，和 test_evidence_claims 里那次同一类问题）。
            # 这里只需要制造一处漂移，所以从数据现场取真实数字再改坏它。
            tools_n = len(json.loads((ROOT / "data/tools.json").read_text(encoding="utf-8"))["tools"])
            marker = f"{tools_n} 个 AI 工具导航"
            body = readme.read_text(encoding="utf-8")
            self.assertIn(marker, body)          # 先确认标记真的在，否则下面等于没改
            readme.write_text(body.replace(marker, "999 个 AI 工具导航"), encoding="utf-8")

            _, changed = sync_local(root)
            self.assertEqual(["README.md"], changed)
            self.assertIn("999 个 AI 工具导航", readme.read_text(encoding="utf-8"))

            _, written = sync_local(root, write=True)
            self.assertEqual(["README.md"], written)
            self.assertIn(marker, readme.read_text(encoding="utf-8"))   # 写回后应恢复成真实数字


if __name__ == "__main__":
    unittest.main()
