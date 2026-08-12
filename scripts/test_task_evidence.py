#!/usr/bin/env python3

import json
import unittest

from generate_reproduce_page import OUTPUT, ROOT, load_records, render, validate_records


class TaskEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.records, self.results = load_records()

    def test_evidence_levels_match_preserved_case_text(self):
        verbatim, summaries = validate_records(self.records)
        self.assertEqual(7, len(verbatim))
        self.assertEqual(6, len(summaries))
        self.assertEqual(
            {
                "ai-learning-coach",
                "bookkeeping-cn",
                "chinese-typography",
                "chinese-work-report",
                "ecommerce-copywriting",
                "github-readme-cn",
                "homework-tutor-cn",
            },
            {name for name, _, _ in verbatim},
        )

    def test_task_evidence_covers_every_activation_result(self):
        self.assertEqual(set(self.results), set(self.records))
        compatibility = json.loads((ROOT / "data" / "compatibility.json").read_text(encoding="utf-8"))
        cases = set(compatibility["results"]["codexActivation"]["cases"])
        self.assertEqual(cases, {record["case"] for record in self.records.values()})

    def test_generated_reproduce_page_is_current(self):
        self.assertEqual(render(), OUTPUT.read_text(encoding="utf-8"))

    def test_only_verbatim_records_have_copyable_tasks(self):
        body = OUTPUT.read_text(encoding="utf-8")
        self.assertEqual(7, body.count(">复制任务</button>"))
        self.assertIn("7 条逐字任务原文", body)
        self.assertIn("6 条只有任务摘要", body)
        for name, record in self.records.items():
            with self.subTest(skill=name):
                if record["level"] == "verbatim":
                    self.assertIn(f'<span>{name}</span>', body)
                else:
                    self.assertIn(f'<code>{name}</code>', body)


if __name__ == "__main__":
    unittest.main()
