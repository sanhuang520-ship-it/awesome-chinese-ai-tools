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
        self.assertEqual(4, structured["numberOfItems"])
        self.assertEqual(
            ["#writing", "#visual", "#learning", "#office"],
            [item["url"].removeprefix(structured["url"]) for item in structured["itemListElement"]],
        )

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


if __name__ == "__main__":
    unittest.main()
