#!/usr/bin/env python3

import unittest

from generate_try_tasks_page import OUTPUT, load_tasks, render, sync_explainer_links


class TryTasksPageTest(unittest.TestCase):
    def test_tasks_cover_all_skills_without_blurring_evidence_levels(self):
        historical, prospective = load_tasks()
        self.assertEqual(7, len(historical))
        self.assertEqual(6, len(prospective))
        self.assertEqual(13, len({item["skill"] for item in historical + prospective}))
        self.assertTrue(all("checks" not in item for item in historical))
        self.assertTrue(all(len(item["checks"]) == 4 for item in prospective))

    def test_generated_page_has_complete_first_use_flow(self):
        body = OUTPUT.read_text(encoding="utf-8")
        self.assertEqual(render(), body)
        self.assertEqual(13, body.count('class="task"'))
        self.assertEqual(13, body.count("复制安装命令"))
        self.assertEqual(13, body.count(">复制任务</button>"))
        self.assertEqual(7, body.count('data-kind="historical"'))
        self.assertEqual(6, body.count('data-kind="prospective"'))
        self.assertEqual(2, body.count("PLANNED · 尚无结果"))
        self.assertEqual(3, body.count("已执行 · 预注册门槛通过 4 / 4"))
        self.assertEqual(1, body.count("已执行 · 未通过全部门槛 3 / 4"))
        self.assertIn("2 条仍为 planned", body)
        self.assertIn("先移除 Token、邮箱、私人路径和未公开数据", body)

    def test_all_explainers_link_to_first_use_page(self):
        self.assertEqual([], sync_explainer_links())


if __name__ == "__main__":
    unittest.main()
