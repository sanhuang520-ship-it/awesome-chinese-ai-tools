#!/usr/bin/env python3

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ChangelogTest(unittest.TestCase):
    def test_current_release_keeps_evidence_boundaries(self):
        body = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [v0.2.0] - 2026-08-12", body)
        self.assertIn("Claude Code：待任务级实测", body)
        self.assertIn("Cursor：待任务级实测", body)
        self.assertIn("不声明准确率", body)


if __name__ == "__main__":
    unittest.main()
