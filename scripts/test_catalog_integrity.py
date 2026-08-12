#!/usr/bin/env python3

import json
import re
import unittest
import yaml
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

    def test_tool_fields_are_safe_for_current_html_templates(self):
        attribute_unsafe = re.compile(r"[<>\"'`]")
        for tool in self.tools:
            with self.subTest(tool=tool["name"]):
                self.assertNotRegex(tool["name"], attribute_unsafe)
                self.assertNotRegex(tool["url"], attribute_unsafe)
                self.assertNotRegex(tool.get("desc", ""), r"[<>]")
                self.assertNotRegex(tool.get("freeInfo", ""), r"[<>]")

    def test_category_style_values_use_expected_formats(self):
        for name, category in self.data["categories"].items():
            with self.subTest(category=name):
                self.assertRegex(name, r"^[a-z][a-z0-9-]*$")
                self.assertRegex(category["color"], r"^#[0-9a-fA-F]{6}$")
                self.assertRegex(category["bg"], r"^rgba\(\d{1,3},\d{1,3},\d{1,3},(?:0|1|0?\.\d+)\)$")

    def test_skill_fields_are_safe_for_current_html_templates(self):
        data = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))
        for skill in data["skills"]:
            with self.subTest(skill=skill["name"]):
                self.assertTrue(skill["name"].strip())
                self.assertNotRegex(skill["name"], r"[<>\"'`\\]")
                self.assertNotRegex(skill["url"], r"[<>\"'`]")
                self.assertNotRegex(skill.get("desc", ""), r"[<>]")
                self.assertNotRegex(skill.get("descEn", ""), r"[<>]")

    def test_every_declared_skill_explainer_exists_and_is_first_party(self):
        data = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))
        explainers = {skill["name"]: skill["explainer"] for skill in data["skills"] if skill.get("explainer")}
        first_party = {skill["name"] for skill in data["skills"] if skill.get("ours")}
        self.assertGreaterEqual(len(explainers), 12)
        self.assertEqual(set(), set(explainers) - first_party)
        for name, relative in explainers.items():
            with self.subTest(skill=name):
                self.assertRegex(relative, r"^[a-z0-9-]+/$")
                self.assertTrue((ROOT / relative / "index.html").is_file())

    def test_first_party_drawer_routes_to_guide_source_and_case(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="sp-guide"', index)
        self.assertIn('id="sp-case"', index)
        self.assertIn("skill.explainer", index)
        self.assertIn("'cases/' + name + '-codex.md'", index)

    def test_first_party_skill_frontmatter_is_directory_and_index_friendly(self):
        allowed_categories = {
            "content-creation",
            "design",
            "development",
            "documentation",
            "finance",
            "marketing",
            "productivity",
        }
        for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                frontmatter = text.split("---\n", 2)[1]
                data = yaml.safe_load(frontmatter)
                self.assertEqual(path.parent.name, data["name"])
                self.assertRegex(data["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertLessEqual(len(data["name"]), 64)
                self.assertTrue(data["description"].strip())
                self.assertLessEqual(len(data["description"]), 1024)
                metadata = data["metadata"]
                self.assertEqual("sanhuang520-ship-it", metadata["author"])
                self.assertIn(metadata["category"], allowed_categories)
                tags = [tag for tag in re.split(r"[,\s]+", metadata["tags"]) if tag]
                self.assertGreaterEqual(len(tags), 3)
                self.assertLessEqual(len(tags), 5)
                self.assertEqual(len(tags), len(set(tags)))
                for tag in tags:
                    self.assertRegex(tag, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

    def test_timeline_fields_cannot_inject_markup(self):
        data = json.loads((ROOT / "data" / "updates.json").read_text(encoding="utf-8"))
        for event in data.get("events", []):
            with self.subTest(event=event.get("title")):
                for field in ("date", "type", "title", "desc"):
                    self.assertNotRegex(str(event.get(field, "")), r"[<>]")


if __name__ == "__main__":
    unittest.main()
