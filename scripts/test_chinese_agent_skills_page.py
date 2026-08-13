#!/usr/bin/env python3
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ChineseAgentSkillsPageTest(unittest.TestCase):
    def setUp(self):
        self.body = (ROOT / "chinese-agent-skills" / "index.html").read_text(encoding="utf-8")

    def test_search_terms_are_used_as_truthful_positioning(self):
        for phrase in ("Chinese Agent Skills", "Chinese AI Skills", "184", "141 source repositories", "13 first-party Skills"):
            self.assertIn(phrase, self.body)

    def test_install_evidence_and_contribution_paths_are_actionable(self):
        for phrase in ("npx skills add", "../try-agent-skills/", "../audit-skill/", "../method/", "../fix-agent-skill/", "../contribute/"):
            self.assertIn(phrase, self.body)

    def test_cross_client_and_accuracy_boundaries_are_explicit(self):
        for phrase in ("Claude Code and Cursor task-level compatibility are still untested", "not an overall accuracy rate", "cross-client guarantee"):
            self.assertIn(phrase, self.body)

    def test_metadata_and_structured_data_are_complete(self):
        for token in ('rel="canonical"', 'hreflang="zh-CN"', 'property="og:title"', 'name="twitter:card"'):
            self.assertIn(token, self.body)
        payload = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', self.body, re.S).group(1))
        self.assertEqual("CollectionPage", payload["@type"])
        self.assertEqual(184, payload["mainEntity"]["numberOfItems"])

if __name__ == "__main__":
    unittest.main()
