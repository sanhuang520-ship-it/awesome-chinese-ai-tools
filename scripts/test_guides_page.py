#!/usr/bin/env python3

import json
import re
import unittest

from generate_guides_page import OUTPUT, ROOT, render, sync_explainer_links


class GuidesPageTest(unittest.TestCase):
    def setUp(self):
        self.body = OUTPUT.read_text(encoding="utf-8")
        catalog = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))
        self.originals = [item for item in catalog["skills"] if item.get("ours")]

    def test_generated_page_is_current(self):
        self.assertEqual(render(), self.body)

    def test_every_original_has_one_card_and_three_destinations(self):
        self.assertEqual(13, self.body.count('<article class="guide-card"'))
        for skill in self.originals:
            with self.subTest(skill=skill["name"]):
                self.assertEqual(1, self.body.count(f'<span class="number">{skill["name"]}</span>'))
                self.assertIn(f'href="../{skill["explainer"]}"', self.body)
                self.assertIn(f'href="../skills/{skill["name"]}/SKILL.md"', self.body)

    def test_outcome_totals_match_public_summary(self):
        outcomes = re.findall(r'<article class="guide-card" data-outcome="([^"]+)"', self.body)
        self.assertEqual(10, outcomes.count("done"))
        self.assertEqual(1, outcomes.count("wait"))
        self.assertEqual(2, outcomes.count("partial"))

    def test_all_explainers_link_back_to_index(self):
        self.assertEqual([], sync_explainer_links())


if __name__ == "__main__":
    unittest.main()
