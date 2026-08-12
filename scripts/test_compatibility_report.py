#!/usr/bin/env python3

import copy
import json
import unittest
from pathlib import Path

from check_compatibility_report import validate


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "compatibility-result.example.json"
SCHEMA = ROOT / "schemas" / "compatibility-result.schema.json"


class CompatibilityReportTest(unittest.TestCase):
    def setUp(self):
        self.report = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_published_example_passes_repository_validator(self):
        self.assertEqual(validate(self.report), [])

    def test_every_submitted_report_passes_repository_validator(self):
        for path in sorted((ROOT / "compatibility-reports").glob("*.json")):
            with self.subTest(path=path.name):
                report = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(validate(report), [])

    def test_schema_is_draft_2020_12_and_strict(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])
        self.assertIn("boundaries", schema["required"])
        self.assertIn("not-run", schema["properties"]["completion"]["properties"]["status"]["enum"])
        self.assertEqual(schema["properties"]["privacy"]["properties"]["scrubbed"], {"const": True})
        self.assertEqual(len(schema["allOf"]), 2)

    def test_unknown_skill_is_rejected(self):
        self.report["skill"] = "invented-skill"
        self.assertTrue(any("not one of" in error for error in validate(self.report)))

    def test_missing_evidence_boundary_is_rejected(self):
        self.report["boundaries"] = []
        self.assertTrue(any(error.startswith("boundaries:") for error in validate(self.report)))

    def test_environment_block_cannot_be_claimed_as_completion(self):
        self.report["environment"] = {"status": "blocked", "error": "Account quota reached"}
        errors = validate(self.report)
        self.assertIn("environment blocked: activation.status must be unknown", errors)
        self.assertIn("environment blocked: completion.status must be not-run", errors)

    def test_consistent_environment_block_is_accepted(self):
        self.report["environment"] = {"status": "blocked", "error": "Account quota reached"}
        self.report["activation"] = {"status": "unknown", "evidence": "Model execution did not begin."}
        self.report["completion"] = {"status": "not-run", "summary": "No model output was produced."}
        self.assertEqual(validate(self.report), [])

    def test_sensitive_values_are_rejected(self):
        for value in (
            "contact maintainer@example.com",
            "Bearer abcdefghijklmnop",
            "/Users/private-name/project/result.txt",
        ):
            with self.subTest(value=value):
                report = copy.deepcopy(self.report)
                report["observed"] = [value]
                self.assertTrue(any(error.startswith("privacy scan:") for error in validate(report)))


if __name__ == "__main__":
    unittest.main()
