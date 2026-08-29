#!/usr/bin/env python3

import struct
import unittest
from pathlib import Path

from generate_social_preview import PNG_PATH, SVG_PATH, load_stats, png_is_stale, render_svg


ROOT = Path(__file__).resolve().parents[1]


class SocialPreviewTest(unittest.TestCase):
    def test_svg_is_generated_from_current_repository_evidence(self):
        expected = render_svg(load_stats())
        self.assertEqual(expected, SVG_PATH.read_text(encoding="utf-8"))

    def test_preview_uses_precise_units_and_client_boundaries(self):
        svg = SVG_PATH.read_text(encoding="utf-8")
        for phrase in ("Agent Skill 条目", "中文 Skill 条目", "Codex 13/13 自动触发记录",
                       "Claude Code 部分实测 · Cursor 待测"):
            self.assertIn(phrase, svg)
        for stale in ("184 个可安装", "68 个中文项目", "Codex / Claude Code / Cursor",
                      # cron 已于 2026-08-20 移除，改为手动触发。分享图是最外层的对外
                      # 物料，措辞必须跟着改，不能继续宣称「每日/每天」自动复检。
                      "每日来源复检", "每天自动复检",
                      # Claude Code 只做过发现与加载，触发那一项是自测，不许写成全测过。
                      "Claude Code 已实测", "Claude Code 13/13 自动触发"):
            self.assertNotIn(stale, svg)
        # Cursor 一个字都没测过，这条必须留着
        self.assertIn("Cursor 待测", svg)

    def test_png_is_not_stale_relative_to_svg(self):
        """
        og.png 必须是照当前 og.svg 渲染的。

        og.svg 现在由 daily_check.py 自动同步，但 og.png 只能本地生成
        （要 rsvg-convert，而且这张图是中文文案、CI runner 没有中文字体，
        在那边渲染会出豆腐块）。所以这里靠 og.png.sha256 这个哈希戳判断是否过期，
        不需要渲染也不需要字体——否则 PNG 会在无人察觉的情况下一直显示旧数字，
        而它正是分享到社交平台时别人看到的那张图。

        报红时的修法：python3 scripts/generate_social_preview.py --write --png
        """
        svg = SVG_PATH.read_text(encoding="utf-8")
        self.assertFalse(
            png_is_stale(svg),
            "og.png 落后于 og.svg；本地跑 generate_social_preview.py --write --png 后提交",
        )

    def test_png_has_social_preview_dimensions(self):
        data = PNG_PATH.read_bytes()
        self.assertEqual(b"\x89PNG\r\n\x1a\n", data[:8])
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((1200, 630), (width, height))


if __name__ == "__main__":
    unittest.main()
