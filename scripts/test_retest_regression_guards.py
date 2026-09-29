#!/usr/bin/env python3

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RetestRegressionGuardsTest(unittest.TestCase):
    def test_web_theme_existing_site_checklist_preserves_all_six_gates(self):
        body = (ROOT / "skills/chinese-web-themes/SKILL.md").read_text(encoding="utf-8")
        for gate in ("正文", "移动端", "代码块", "样式覆盖", "授权", "无障碍"):
            with self.subTest(gate=gate):
                self.assertIn(f"**{gate}**", body)
        self.assertIn("不要生成整份 CSS", body)

    def test_threejs_bounded_review_has_count_path_and_no_run_guards(self):
        body = (ROOT / "skills/guofeng-threejs/SKILL.md").read_text(encoding="utf-8")
        for phrase in (
            "按 Unicode 字符计数必须 `<= 300`",
            "压到约 220–260 字留余量",
            "路径用仓库相对路径",
            "不要启动浏览器、服务器、构建或 Demo",
            "skills/guofeng-threejs/demo.html",
            "skills/guofeng-threejs/intro-demo.html",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, body)


if __name__ == "__main__":
    unittest.main()
