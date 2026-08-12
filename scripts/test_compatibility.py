#!/usr/bin/env python3

import json
import unittest
from pathlib import Path

from check_compatibility import repository_skills


ROOT = Path(__file__).resolve().parents[1]


class CompatibilityDataTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            (ROOT / "data" / "compatibility.json").read_text(encoding="utf-8")
        )

    def test_all_repository_skills_are_recorded(self):
        self.assertEqual(self.data["skills"], repository_skills())

    def test_verified_counts_match_recorded_skills(self):
        count = len(self.data["skills"])
        self.assertEqual(self.data["results"]["discovery"]["count"], count)
        self.assertEqual(self.data["results"]["codexInstall"]["identicalCount"], count)

    def test_activation_evidence_points_to_a_case(self):
        activation = self.data["results"]["codexActivation"]
        self.assertEqual(activation["status"], "partial")
        self.assertEqual(
            activation["verifiedSkills"],
            ["chinese-typography", "github-readme-cn", "chinese-work-report", "bookkeeping-cn", "ecommerce-copywriting", "homework-tutor-cn"],
        )
        self.assertEqual(len(activation["verifiedSkills"]), len(activation["cases"]))
        for case in activation["cases"]:
            self.assertTrue((ROOT / case).is_file())

    def test_unrun_clients_are_not_claimed_as_verified(self):
        self.assertEqual(self.data["results"]["claudeCode"]["status"], "not-tested")
        self.assertEqual(self.data["results"]["cursor"]["status"], "not-tested")


if __name__ == "__main__":
    unittest.main()
