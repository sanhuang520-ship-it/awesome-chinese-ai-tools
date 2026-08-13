#!/usr/bin/env python3

import json
import unittest
from pathlib import Path

from check_install_environment_report import validate


ROOT = Path(__file__).resolve().parents[1]


class InstallEnvironmentReportTest(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((ROOT / "examples" / "install-environment-result.example.json").read_text(encoding="utf-8"))

    def test_example_is_valid(self):
        self.assertEqual([], validate(self.report))

    def test_private_path_is_rejected(self):
        self.report["paths"][0]["path"] = "/Users/someone/.agents/skills/chinese-typography"
        self.assertTrue(any("privacy scan" in error for error in validate(self.report)))

    def test_activation_claim_is_not_part_of_installation_contract(self):
        self.report["activation"] = "verified"
        self.assertTrue(any("unknown fields" in error for error in validate(self.report)))


if __name__ == "__main__":
    unittest.main()
