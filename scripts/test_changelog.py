#!/usr/bin/env python3

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ChangelogTest(unittest.TestCase):
    def test_current_release_keeps_evidence_boundaries(self):
        body = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [v1.1.1] - 2026-08-12", body)
        self.assertIn("## [v1.1.0] - 2026-08-12", body)
        self.assertIn("Claude Code：待任务级实测", body)
        self.assertIn("Cursor：待任务级实测", body)
        self.assertIn("不声明准确率", body)
        self.assertIn("GitHub Stars 在本版本发布前仍为 7", body)

    def test_unreleased_section_tracks_current_main_without_claiming_growth(self):
        body = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [Unreleased]", body)
        self.assertIn("compare/v1.1.1...HEAD", body)
        self.assertIn("不等于独立用户或效果证明", body)
        self.assertIn("workflow` 写入权限", body)


if __name__ == "__main__":
    unittest.main()
