#!/usr/bin/env python3

import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublicFeedsTest(unittest.TestCase):
    def test_feed_is_valid_and_contains_only_repository_updates(self):
        feed = (ROOT / "feed.xml").read_text(encoding="utf-8")
        root = ET.fromstring(feed)
        items = root.findall("./channel/item")
        self.assertGreaterEqual(len(items), 1)
        self.assertNotIn("AI 日报", feed)
        self.assertNotIn("今日推荐", feed)
        self.assertTrue(all("awesome-chinese-ai-tools" in item.findtext("link", "") for item in items))

    def test_sitemap_contains_every_repository_owned_skill(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        ET.fromstring(sitemap)
        for skill_file in (ROOT / "skills").glob("*/SKILL.md"):
            expected = f"/skills/{skill_file.parent.name}/SKILL.md"
            with self.subTest(skill=skill_file.parent.name):
                self.assertIn(expected, sitemap)


if __name__ == "__main__":
    unittest.main()
