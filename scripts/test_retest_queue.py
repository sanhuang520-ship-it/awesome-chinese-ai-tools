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

    def test_every_item_is_preregistered_and_has_four_acceptance_checks(self):
        for item in self.items:
            with self.subTest(skill=item["skill"]):
                self.assertEqual(4, len(item["acceptanceZh"]))
                self.assertNotIn(item["skill"], item["promptZh"])
        statuses = {item["skill"]: item["status"] for item in self.items}
        self.assertEqual({"book-digest-cn", "chinese-design-md"}, {skill for skill, status in statuses.items() if status == "executed-pass"})
        self.assertEqual(4, sum(status == "planned" for status in statuses.values()))
        for item in self.items:
            if item["status"] == "planned":
                continue
            execution = item["execution"]
            self.assertEqual(execution["passedChecks"], execution["totalChecks"])
            self.assertTrue((ROOT / execution["case"]).is_file())
            case = (ROOT / execution["case"]).read_text(encoding="utf-8")
            self.assertIn(item["promptZh"], case)
            for check in item["acceptanceZh"]:
                self.assertIn(check, case)

    def test_generated_page_is_current_and_does_not_claim_results(self):
        self.assertEqual(render(), self.body)
        self.assertEqual(6, self.body.count('class="queue-card"'))
        self.assertEqual(6, self.body.count(">复制任务</button>"))
        self.assertEqual(4, self.body.count("PLANNED · 尚无结果"))
        self.assertEqual(2, self.body.count("已执行 · 预注册门槛通过 4 / 4"))
        self.assertIn("2 个已执行", self.body)
        self.assertIn("4 项 planned 仍不算通过", self.body)


if __name__ == "__main__":
    unittest.main()
