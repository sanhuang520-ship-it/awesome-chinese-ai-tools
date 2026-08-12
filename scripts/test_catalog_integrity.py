#!/usr/bin/env python3

import json
import unittest
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]


class CatalogIntegrityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "data" / "tools.json").read_text(encoding="utf-8"))
        cls.tools = cls.data["tools"]

    def test_tool_names_are_unique(self):
        names = [tool["name"].strip().casefold() for tool in self.tools]
        duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
        self.assertEqual([], duplicates, f"重复工具名称：{duplicates}")

    def test_every_tool_has_a_canonical_https_url(self):
        legacy_hosts = {"cursor.sh", "runwayml.com", "blackforestlabs.ai"}
        for tool in self.tools:
            with self.subTest(tool=tool["name"]):
                parsed = urlsplit(tool["url"])
                self.assertEqual("https", parsed.scheme)
                self.assertTrue(parsed.netloc)
                self.assertNotIn(parsed.netloc.lower().removeprefix("www."), legacy_hosts)

    def test_categories_exist(self):
        categories = self.data["categories"]
        unknown = sorted({tool["cat"] for tool in self.tools if tool["cat"] not in categories})
        self.assertEqual([], unknown, f"未定义分类：{unknown}")

    def test_current_scenario_links_do_not_use_legacy_hosts(self):
        current_surfaces = [ROOT / "index.html", ROOT / "SCENARIOS.md"]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in current_surfaces)
        for host in ("cursor.sh", "runwayml.com", "blackforestlabs.ai"):
            with self.subTest(host=host):
                self.assertNotIn(f"https://{host}", combined)


if __name__ == "__main__":
    unittest.main()
