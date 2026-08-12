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
            ["chinese-typography", "github-readme-cn", "chinese-work-report", "bookkeeping-cn", "ecommerce-copywriting", "homework-tutor-cn", "ai-learning-coach", "book-digest-cn", "chinese-lesson-plan", "chinese-design-md", "chinese-web-themes", "guochao-visual-cn", "guofeng-threejs"],
        )
        expected_cases = [
            f"cases/{skill}-codex.md" for skill in activation["verifiedSkills"]
        ]
        self.assertEqual(activation["cases"], expected_cases)

        examples = (ROOT / "EXAMPLES.md").read_text(encoding="utf-8")
        case_index = (ROOT / "cases" / "README.md").read_text(encoding="utf-8")
        for case in expected_cases:
            self.assertTrue((ROOT / case).is_file())
            relative_case = case.removeprefix("cases/")
            self.assertIn(f"cases/{relative_case}", examples)
            self.assertIn(f"({relative_case})", case_index)

    def test_codex_client_version_matches_every_activation_case(self):
        activation = self.data["results"]["codexActivation"]
        version = "0.147.0-alpha.6.5"
        self.assertEqual(self.data["clients"]["codex"], f"Codex CLI {version}")
        self.assertEqual(activation["clientVersion"], f"codex-cli {version}")
        for case in activation["cases"]:
            with self.subTest(case=case):
                body = (ROOT / case).read_text(encoding="utf-8")
                self.assertIn(f"Codex CLI `{version}`", body)
                self.assertNotIn("Codex desktop", body)

    def test_unrun_clients_are_not_claimed_as_verified(self):
        self.assertEqual(self.data["results"]["claudeCode"]["status"], "not-tested")
        self.assertEqual(self.data["results"]["cursor"]["status"], "not-tested")


if __name__ == "__main__":
    unittest.main()
