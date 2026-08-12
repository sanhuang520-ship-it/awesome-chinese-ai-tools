#!/usr/bin/env python3

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class QualityDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "data" / "quality.json").read_text(encoding="utf-8"))

    def test_all_repository_owned_skills_are_covered(self):
        actual = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(actual, set(self.data["skills"]))

    def test_no_skill_claims_a_formal_certification(self):
        self.assertIn("no claim of formal security certification", self.data["method"])

    def test_only_documented_runtime_network_is_marked(self):
        networked = {name for name, item in self.data["skills"].items() if item["runtimeNetwork"]}
        self.assertEqual(networked, {"guofeng-threejs"})


if __name__ == "__main__":
    unittest.main()
