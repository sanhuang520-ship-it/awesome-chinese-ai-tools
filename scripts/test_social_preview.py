#!/usr/bin/env python3

import struct
import unittest
from pathlib import Path

from generate_social_preview import PNG_PATH, SVG_PATH, load_stats, render_svg


ROOT = Path(__file__).resolve().parents[1]


class SocialPreviewTest(unittest.TestCase):
    def test_svg_is_generated_from_current_repository_evidence(self):
        expected = render_svg(load_stats())
        self.assertEqual(expected, SVG_PATH.read_text(encoding="utf-8"))

    def test_preview_uses_precise_units_and_client_boundaries(self):
        svg = SVG_PATH.read_text(encoding="utf-8")
        for phrase in ("Agent Skill 条目", "中文 Skill 条目", "Codex 13/13 自动触发记录", "Claude Code / Cursor 待测"):
            self.assertIn(phrase, svg)
        for stale in ("184 个可安装", "68 个中文项目", "Codex / Claude Code / Cursor"):
            self.assertNotIn(stale, svg)

    def test_png_has_social_preview_dimensions(self):
        data = PNG_PATH.read_bytes()
        self.assertEqual(b"\x89PNG\r\n\x1a\n", data[:8])
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((1200, 630), (width, height))


if __name__ == "__main__":
    unittest.main()
