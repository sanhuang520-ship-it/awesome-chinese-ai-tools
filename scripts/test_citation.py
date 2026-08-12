#!/usr/bin/env python3

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CitationTest(unittest.TestCase):
    def test_citation_metadata_matches_the_stable_release(self):
        body = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        self.assertIn("cff-version: 1.2.0", body)
        self.assertIn("version: 1.1.1", body)
        self.assertIn("date-released: 2026-08-12", body)
        self.assertIn("license: MIT", body)
        self.assertIn(
            'repository-code: "https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools"',
            body,
        )

    def test_readme_exposes_a_fixed_version_citation(self):
        body = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("[CITATION.cff](CITATION.cff)", body)
        self.assertIn(
            "https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/v1.1.1",
            body,
        )


if __name__ == "__main__":
    unittest.main()
