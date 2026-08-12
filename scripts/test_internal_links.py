#!/usr/bin/env python3

import tempfile
import re
import unittest
from pathlib import Path

from check_internal_links import missing_links


ROOT = Path(__file__).resolve().parents[1]


class InternalLinksTest(unittest.TestCase):
    def test_published_site_has_no_missing_explicit_links(self):
        self.assertEqual([], missing_links(ROOT))

    def test_missing_relative_link_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text('<a href="missing/">broken</a>', encoding="utf-8")
            self.assertEqual(["index.html: missing missing/"], missing_links(root))

    def test_new_tab_links_are_opener_safe(self):
        failures = []
        for path in ROOT.rglob("*.html"):
            text = path.read_text(encoding="utf-8")
            for tag in re.findall(r"<a\b[^>]*target=[\"']_blank[\"'][^>]*>", text, re.I):
                if not re.search(r"rel=[\"'][^\"']*noopener", tag, re.I):
                    failures.append(path.relative_to(ROOT).as_posix())
        self.assertEqual([], failures)

    def test_primary_search_and_icon_controls_have_accessible_names(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        for label in ("搜索 Skill 和使用场景", "切换明暗主题", "关闭工作流示例", "关闭工具对比", "关闭条件筛选"):
            with self.subTest(label=label):
                self.assertIn(f'aria-label="{label}"', index)
        self.assertIn("'搜索工具和功能'", index)
        self.assertIn("'额度记录暂不支持搜索'", index)

    def test_maintenance_plan_links_to_every_named_explainer(self):
        plan = (ROOT / "MAINTENANCE_PLAN.md").read_text(encoding="utf-8")
        for page in ("typography/", "design/", "guochao/", "readme-audit/", "work-report/"):
            with self.subTest(page=page):
                self.assertIn(f"]({page})", plan)

if __name__ == "__main__":
    unittest.main()
