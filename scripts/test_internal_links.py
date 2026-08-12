#!/usr/bin/env python3

import tempfile
import json
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

    def test_mobile_skill_drawer_allows_command_and_actions_to_wrap(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn(".sp-bar{padding:10px 14px;overflow:hidden}", index)
        self.assertIn(".sp-cmd{flex:1 0 100%;width:100%;min-width:0}", index)
        self.assertIn("width:100%;max-width:1200px;min-width:0;margin:0 auto", index)
        self.assertIn("opacity:0;visibility:hidden;pointer-events:none", index)
        self.assertIn("opacity:1;visibility:visible;pointer-events:auto", index)

    def test_maintenance_plan_links_to_every_named_explainer(self):
        plan = (ROOT / "MAINTENANCE_PLAN.md").read_text(encoding="utf-8")
        for page in ("typography/", "design/", "guochao/", "readme-audit/", "work-report/", "ecommerce-copywriting/", "themes/", "guofeng-threejs/", "bookkeeping/"):
            with self.subTest(page=page):
                self.assertIn(f"]({page})", plan)

    def test_first_party_explainers_offer_an_evidence_first_repository_path(self):
        catalog = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))
        explainers = {skill["explainer"] for skill in catalog["skills"] if skill.get("explainer")}
        repository = "https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools"
        for relative in explainers:
            with self.subTest(page=relative):
                page = (ROOT / relative / "index.html").read_text(encoding="utf-8")
                self.assertIn(repository, page)
                self.assertIn("觉得有用再 Star", page)

    def test_threejs_guide_keeps_install_command_visible_without_clipboard_access(self):
        page = (ROOT / "guofeng-threejs" / "index.html").read_text(encoding="utf-8")
        command = "npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill guofeng-threejs"
        self.assertIn(f"<code>{command}</code>", page)
        self.assertIn(f'data-copy="{command}"', page)

    def test_bookkeeping_guide_keeps_reconciliation_and_install_command_visible(self):
        page = (ROOT / "bookkeeping" / "index.html").read_text(encoding="utf-8")
        command = "npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill bookkeeping-cn"
        for value in ("12,000", "5,000", "1,000", "6,000"):
            self.assertIn(value, page)
        self.assertIn(f"<code>{command}</code>", page)
        self.assertNotIn("投资收益", page)
        self.assertNotIn("节税方案", page)

if __name__ == "__main__":
    unittest.main()
