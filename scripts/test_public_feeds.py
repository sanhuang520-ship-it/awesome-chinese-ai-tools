#!/usr/bin/env python3

import unittest
import xml.etree.ElementTree as ET
from collections import Counter
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

    def test_sitemap_includes_bilingual_project_overviews(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("/README.md", sitemap)
        self.assertIn("/README.en.md", sitemap)

    def test_sitemap_contains_reproducible_case_evidence(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("/cases/README.md", sitemap)
        for case in (ROOT / "cases").glob("*-codex.md"):
            expected = f"/cases/{case.name}"
            with self.subTest(case=case.name):
                self.assertIn(expected, sitemap)

    def test_sitemap_contains_first_party_explainer_pages(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for page in ("typography/", "design/", "guochao/", "readme-audit/", "work-report/", "ecommerce-copywriting/", "themes/", "guofeng-threejs/", "bookkeeping/"):
            with self.subTest(page=page):
                self.assertIn(f"/awesome-chinese-ai-tools/{page}", sitemap)

    def test_first_party_explainers_have_complete_search_metadata(self):
        for page in ("typography", "design", "guochao", "readme-audit", "work-report", "ecommerce-copywriting", "themes", "guofeng-threejs", "bookkeeping"):
            body = (ROOT / page / "index.html").read_text(encoding="utf-8")
            with self.subTest(page=page):
                self.assertTrue(body.lower().startswith("<!doctype html>"))
                self.assertRegex(body, r'<html\b[^>]*\blang="zh-CN"[^>]*>')
                self.assertIn("<head>", body)
                self.assertIn("</head>", body)
                self.assertIn("<body", body)
                self.assertIn("</body>", body)
                self.assertTrue(body.rstrip().endswith("</html>"))
                self.assertIn('<meta name="robots" content="index,follow">', body)
                self.assertIn(f'/awesome-chinese-ai-tools/{page}/', body)
                self.assertIn('property="og:title"', body)
                self.assertIn('property="og:description"', body)
                self.assertIn('property="og:url"', body)
                self.assertIn('type="application/ld+json"', body)

    def test_llms_summary_preserves_client_evidence_boundary(self):
        summary = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("Claude Code 与 Cursor 尚无本仓库运行的任务级实测", summary)
        self.assertIn("区分 CLI 发现、文件安装、自动触发和任务完成", summary)
        self.assertIn("data/compatibility.json", summary)
        for page in ("typography/", "design/", "guochao/", "readme-audit/", "work-report/", "ecommerce-copywriting/", "themes/", "guofeng-threejs/", "bookkeeping/"):
            with self.subTest(page=page):
                self.assertIn(f"/awesome-chinese-ai-tools/{page}", summary)

    def test_sitemap_urls_are_unique(self):
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = [node.text for node in root.findall("s:url/s:loc", namespace)]
        duplicates = sorted(url for url, count in Counter(locations).items() if count > 1)
        self.assertEqual([], duplicates)


if __name__ == "__main__":
    unittest.main()
