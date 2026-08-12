#!/usr/bin/env python3

import json
import unittest

from generate_retest_queue import OUTPUT, ROOT, load_items, render


class RetestQueueTest(unittest.TestCase):
    def setUp(self):
        self.items = load_items()
        self.body = OUTPUT.read_text(encoding="utf-8")

    def test_queue_only_covers_summary_only_cases(self):
        evidence = json.loads((ROOT / "data" / "task-evidence.json").read_text(encoding="utf-8"))["records"]
        summary_only = {name for name, record in evidence.items() if record["level"] == "summary-only"}
        self.assertEqual(summary_only, {item["skill"] for item in self.items})

    def test_every_item_is_prospective_and_has_four_acceptance_checks(self):
        for item in self.items:
            with self.subTest(skill=item["skill"]):
                self.assertEqual("planned", item["status"])
                self.assertEqual(4, len(item["acceptanceZh"]))
                self.assertNotIn(item["skill"], item["promptZh"])

    def test_generated_page_is_current_and_does_not_claim_results(self):
        self.assertEqual(render(), self.body)
        self.assertEqual(6, self.body.count('class="queue-card"'))
        self.assertEqual(6, self.body.count(">复制待测任务</button>"))
        self.assertEqual(6, self.body.count("PLANNED · 尚无结果"))
        self.assertIn("目前一个都不算通过", self.body)
        for forbidden in ("测试通过", "兼容通过", "自动触发成功"):
            self.assertNotIn(forbidden, self.body)


if __name__ == "__main__":
    unittest.main()
