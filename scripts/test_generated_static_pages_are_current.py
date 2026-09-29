#!/usr/bin/env python3
"""
guides/、reproduce/、retest/、try-agent-skills/ 这四个页面各自有生成脚本
（generate_guides_page.py 等），但在 2026-08-16 之前没有任何测试盯着它们——
数据（compatibility.json / quality.json / cases 目录）改了、页面没跟着重
渲染，daily-check.yml 和 tests.yml 都发现不了，跟 catalog/index.html 当初
踩的坑是同一类问题，只是这四个完全没人管。

四个生成脚本都遵循同一个模式：一个 render() 纯函数 + 一个 OUTPUT 路径，
直接比对 render() 的产出和已提交文件是否一致即可。
"""
import unittest
from pathlib import Path

from generate_guides_page import OUTPUT as GUIDES_OUTPUT, render as render_guides
from generate_reproduce_page import OUTPUT as REPRODUCE_OUTPUT, render as render_reproduce
from generate_retest_queue import OUTPUT as RETEST_OUTPUT, render as render_retest
from generate_try_tasks_page import OUTPUT as TRY_TASKS_OUTPUT, render as render_try_tasks


ROOT = Path(__file__).resolve().parents[1]


class GeneratedStaticPagesAreCurrentTest(unittest.TestCase):
    def _assert_matches(self, render_fn, output_path):
        expected = render_fn()
        actual = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
        self.assertEqual(
            expected, actual,
            f"{output_path.relative_to(ROOT)} 与数据不一致，"
            f"跑一遍对应的 generate_*.py --write 重新生成后再提交",
        )

    def test_guides_page_matches_compatibility_and_quality_data(self):
        self._assert_matches(render_guides, GUIDES_OUTPUT)

    def test_reproduce_page_matches_case_records(self):
        self._assert_matches(render_reproduce, REPRODUCE_OUTPUT)

    def test_retest_queue_matches_source_data(self):
        self._assert_matches(render_retest, RETEST_OUTPUT)

    def test_try_tasks_page_matches_source_data(self):
        self._assert_matches(render_try_tasks, TRY_TASKS_OUTPUT)


if __name__ == "__main__":
    unittest.main()
