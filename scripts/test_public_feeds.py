#!/usr/bin/env python3

import unittest
import json
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urljoin
from pathlib import Path

from sync_feed import render_feed


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/"


class DiscoveryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.robots = ""
        self.canonical = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "meta" and values.get("name", "").lower() == "robots":
            self.robots = values.get("content", "").lower()
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical.append(values.get("href"))


class PublicFeedsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))
        cls.explainers = sorted(
            skill["explainer"].rstrip("/")
            for skill in catalog["skills"]
            if skill.get("ours") and skill.get("explainer")
        )

    def test_robots_allows_crawling_and_declares_canonical_sitemap(self):
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("User-agent: *", robots)
        self.assertIn("Allow: /", robots)
        self.assertNotIn("Disallow: /", robots)
        self.assertIn(f"Sitemap: {BASE_URL}sitemap.xml", robots)

    def test_feed_is_valid_and_contains_only_repository_updates(self):
        feed = (ROOT / "feed.xml").read_text(encoding="utf-8")
        self.assertEqual(render_feed(), feed)
        root = ET.fromstring(feed)
        items = root.findall("./channel/item")
        self.assertGreaterEqual(len(items), 5)
        self.assertNotIn("AI 日报", feed)
        self.assertNotIn("今日推荐", feed)
        self.assertTrue(all("awesome-chinese-ai-tools" in item.findtext("link", "") for item in items))
        guids = [item.findtext("guid", "") for item in items]
        self.assertEqual(len(guids), len(set(guids)))
        self.assertIn("10 项当次任务完成", feed)
        self.assertIn("1 项按流程等待必要输入", feed)
        self.assertIn("2 项大任务失败后缩小复测通过", feed)
        self.assertNotIn("11 项首次完成", feed)
        self.assertIn("Agent Skills 兼容性怎么测试：四层证据法", feed)
        self.assertIn("Codex Skill 安装了却不触发？5 步定位", feed)
        self.assertIn("如何创建 Codex Skill：从 SKILL.md 到自动触发", feed)
        self.assertIn("Agent Skill 安装前安全检查：只读本地审计器", feed)
        self.assertIn("skills CLI 1.5.22 隔离安装与项目更新复测：13/13 一致", feed)
        self.assertIn("不会持续同步", feed)

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

    def test_sitemap_contains_read_only_skill_auditor(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("/awesome-chinese-ai-tools/audit-skill/", sitemap)

    def test_sitemap_contains_reproducible_case_evidence(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("/cases/README.md", sitemap)
        for case in (ROOT / "cases").glob("*-codex.md"):
            expected = f"/cases/{case.name}"
            with self.subTest(case=case.name):
                self.assertIn(expected, sitemap)

    def test_sitemap_contains_first_party_explainer_pages(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for page in self.explainers:
            with self.subTest(page=page):
                self.assertIn(f"/awesome-chinese-ai-tools/{page}/", sitemap)

    def test_first_party_explainers_have_complete_search_metadata(self):
        for page in self.explainers:
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
        for page in self.explainers:
            with self.subTest(page=page):
                self.assertIn(f"/awesome-chinese-ai-tools/{page}/", summary)

    def test_sitemap_urls_are_unique(self):
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = [node.text for node in root.findall("s:url/s:loc", namespace)]
        duplicates = sorted(url for url, count in Counter(locations).items() if count > 1)
        self.assertEqual([], duplicates)

    def test_updated_discovery_pages_have_matching_sitemap_dates(self):
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        lastmods = {
            node.findtext("s:loc", namespaces=namespace): node.findtext("s:lastmod", namespaces=namespace)
            for node in root.findall("s:url", namespace)
        }
        expected = {
            BASE_URL: "2026-08-13",
            BASE_URL + "guides/": "2026-08-13",
            BASE_URL + "audit-skill/": "2026-08-13",
            BASE_URL + "install/": "2026-08-13",
            BASE_URL + "guochao/": "2026-08-12",
        }
        for url, date in expected.items():
            with self.subTest(url=url):
                self.assertEqual(date, lastmods.get(url))

    def test_every_indexable_html_has_one_canonical_and_sitemap_entry(self):
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = {node.text for node in root.findall("s:url/s:loc", namespace)}
        for page in sorted(ROOT.rglob("*.html")):
            if any(part.startswith(".") or part in {"node_modules", "work"} for part in page.relative_to(ROOT).parts):
                continue
            parser = DiscoveryParser()
            parser.feed(page.read_text(encoding="utf-8"))
            if "noindex" in parser.robots:
                continue
            relative = page.relative_to(ROOT).as_posix()
            expected = BASE_URL if relative == "index.html" else urljoin(BASE_URL, relative.removesuffix("index.html"))
            with self.subTest(page=relative):
                self.assertEqual([expected], parser.canonical)
                self.assertIn(expected, locations)

    def test_raw_demo_pages_are_noindex_but_links_remain_followable(self):
        demos = (
            "skills/chinese-web-themes/demo.html",
            "skills/guofeng-threejs/demo.html",
            "skills/guofeng-threejs/intro-demo.html",
            "themes/ink3d.html",
            "themes/intro.html",
        )
        for relative in demos:
            body = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(page=relative):
                self.assertIn('<meta name="robots" content="noindex,follow">', body)


if __name__ == "__main__":
    unittest.main()
