#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path

from check_compatibility_reports import check_directory


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "compatibility-result.example.json"


class CompatibilityReportsTest(unittest.TestCase):
    def test_empty_directory_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual([], check_directory(Path(tmp)))

    def test_valid_report_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "valid.json"
            target.write_text(EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
            self.assertEqual([], check_directory(Path(tmp)))

    def test_invalid_json_and_invalid_report_name_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "broken.json").write_text("{", encoding="utf-8")
            report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            report["privacy"]["scrubbed"] = False
            (directory / "unsafe.json").write_text(json.dumps(report), encoding="utf-8")
            errors = check_directory(directory)
            self.assertTrue(any(error.startswith("broken.json:") for error in errors))
            self.assertTrue(any(error.startswith("unsafe.json:") for error in errors))


if __name__ == "__main__":
    unittest.main()
