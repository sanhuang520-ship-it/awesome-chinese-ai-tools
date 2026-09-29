#!/usr/bin/env python3

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BundlesPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = (ROOT / "bundles" / "index.html").read_text(encoding="utf-8")
        data = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))
        cls.first_party = [skill for skill in data["skills"] if skill.get("ours")]

    def test_all_first_party_skills_link_to_their_evidence_pages(self):
        self.assertEqual(13, len(self.first_party))
        for skill in self.first_party:
            with self.subTest(skill=skill["name"]):
                self.assertIn(f'>{skill["name"]}</a>', self.page)
                self.assertIn(f'href="../{skill["explainer"]}"', self.page)

    def test_page_keeps_four_bounded_editorial_groups(self):
        for anchor in ("writing", "visual", "learning", "office"):
            self.assertIn(f'id="{anchor}"', self.page)
        self.assertIn("组合只是任务入口", self.page)
        self.assertIn("不是官方兼容性认证", self.page)
        self.assertIn('href="../guides/"', self.page)

    def test_page_has_complete_share_and_structured_metadata(self):
        self.assertIn('<meta name="robots" content="index,follow">', self.page)
        self.assertIn('<meta property="og:image"', self.page)
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', self.page)
        match = re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', self.page, re.S)
        self.assertIsNotNone(match)
        structured = json.loads(match.group(1))
        item_list, faq = structured["@graph"]
        self.assertEqual("ItemList", item_list["@type"])
        self.assertEqual(4, item_list["numberOfItems"])
        self.assertEqual(
            ["#writing", "#visual", "#learning", "#office"],
            [item["url"].removeprefix(item_list["url"]) for item in item_list["itemListElement"]],
        )
        self.assertEqual("FAQPage", faq["@type"])
        self.assertEqual(4, len(faq["mainEntity"]))

    def test_search_and_share_summaries_do_not_claim_untested_client_support(self):
        head = self.page.split("</head>", 1)[0]
        self.assertIn("Codex 任务级观察", head)
        self.assertIn("Claude Code 与 Cursor 待测", head)
        self.assertNotIn("适用于 Codex、Claude Code", head)
        self.assertNotIn("四组可直接安装", head)

    def test_visible_faq_matches_structured_answers_and_preserves_boundaries(self):
        match = re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', self.page, re.S)
        faq = json.loads(match.group(1))["@graph"][1]
        for item in faq["mainEntity"]:
            with self.subTest(question=item["name"]):
                self.assertIn(item["name"].replace("这些组合在 ", ""), self.page)
                self.assertIn(item["acceptedAnswer"]["text"], self.page)
        self.assertIn("Claude Code 已实测发现与加载（13/13），但自动触发未记录；Cursor 仍待实测", self.page)
        self.assertIn("结果不是安全认证", self.page)

    def test_discovery_surfaces_link_to_bundles(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        catalog = (ROOT / "SKILLS.md").read_text(encoding="utf-8")
        generator = (ROOT / "scripts" / "daily_check.py").read_text(encoding="utf-8")
        self.assertIn("/awesome-chinese-ai-tools/bundles/", readme)
        self.assertIn("/awesome-chinese-ai-tools/bundles/", llms)
        self.assertIn("/awesome-chinese-ai-tools/bundles/", catalog)
        self.assertIn("/awesome-chinese-ai-tools/bundles/", generator)
        self.assertIn("不代表会同时触发", readme)

    def test_missing_scenarios_route_to_a_privacy_safe_issue(self):
        template = (ROOT / ".github" / "ISSUE_TEMPLATE" / "request-bundle.yml").read_text(encoding="utf-8")
        self.assertIn("template=request-bundle.yml", self.page)
        for phrase in (
            "真实任务需求",
            "不是为了推广产品、索要收录或交换 Star",
            "Token、邮箱、私人路径和未公开业务数据",
            "不等于所有 Skill 会同时触发或跨客户端兼容",
        ):
            self.assertIn(phrase, template)


if __name__ == "__main__":
    unittest.main()
