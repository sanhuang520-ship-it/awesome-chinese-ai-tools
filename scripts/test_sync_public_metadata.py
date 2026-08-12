#!/usr/bin/env python3
"""公开统计一致性检查。"""

import json
import unittest
from pathlib import Path

from sync_public_metadata import (
    CAT_ORDER,
    build_stats,
    sync_index_text,
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
            "index.html": lambda text: sync_index_text(text, self.stats),
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

    def test_every_nonempty_category_is_rendered(self):
        skills = json.loads((ROOT / "data/skills.json").read_text(encoding="utf-8"))["skills"]
        used_categories = {item.get("cat") for item in skills}
        self.assertEqual(used_categories, set(CAT_ORDER))


if __name__ == "__main__":
    unittest.main()
