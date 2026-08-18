#!/usr/bin/env python3

import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

from render_static_catalog import render_catalog


ROOT = Path(__file__).resolve().parents[1]


class CatalogParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skill_cards = 0
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "article" and "skill-card" in values.get("class", "").split():
            self.skill_cards += 1
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"])


class StaticCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))
        cls.page = (ROOT / "catalog" / "index.html").read_text(encoding="utf-8")

    def test_page_is_exact_generated_output(self):
        self.assertEqual(render_catalog(self.data), self.page)

    def test_all_skills_are_visible_without_javascript(self):
        parser = CatalogParser()
        parser.feed(self.page)
        self.assertEqual(len(self.data["skills"]), parser.skill_cards)
        for skill in self.data["skills"]:
            with self.subTest(skill=skill["name"]):
                self.assertIn(skill["url"], parser.hrefs)
                self.assertIn(skill["name"], self.page)

    def test_categories_and_counts_come_from_data(self):
        for key, meta in self.data["categories"].items():
            count = sum(skill["cat"] == key for skill in self.data["skills"])
            with self.subTest(category=key):
                self.assertIn(f'id="cat-{key}"', self.page)
                self.assertIn(meta["label"], self.page)
                self.assertIn(f"{count} 个条目", self.page)

    def test_page_preserves_evidence_and_ranking_boundaries(self):
        for phrase in (
            "不按 Star 排名",
            "来源存在不等于功能、兼容或安全认证",
            "第三方资料”只表示目录线索",
            "安装前仍应检查",
        ):
            self.assertIn(phrase, self.page)
        self.assertNotIn("最受欢迎", self.page)
        self.assertNotIn("必装", self.page)

    def test_search_and_social_metadata_are_complete(self):
        for phrase in (
            '<meta name="robots" content="index,follow">',
            '/awesome-chinese-ai-tools/catalog/">',
            'property="og:title"',
            'name="twitter:card"',
            'type="application/ld+json"',
            # 结构化数据里的条目数必须跟 skills.json 一致；用 self.data 现算，
            # 不写死当天数字（写死的话每次增删 Skill 都得回来抄一遍）
            f'"numberOfItems":{len(self.data["skills"])}',
        ):
            self.assertIn(phrase, self.page)


if __name__ == "__main__":
    unittest.main()
