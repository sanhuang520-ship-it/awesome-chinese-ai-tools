#!/usr/bin/env python3

import importlib.util
import os
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_daily_check():
    spec = importlib.util.spec_from_file_location("daily_check_for_test", ROOT / "scripts" / "daily_check.py")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(os.environ, {"GITHUB_TOKEN": "test-token"}):
        spec.loader.exec_module(module)
    return module


class DailyCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_daily_check()

    def test_same_day_without_status_changes_does_not_write(self):
        self.assertFalse(self.module.should_persist_tool_check(0, "2026-08-12", "2026-08-12"))

    def test_new_observation_day_writes_even_without_status_changes(self):
        self.assertTrue(self.module.should_persist_tool_check(0, "2026-08-11", "2026-08-12"))

    def test_status_change_always_writes(self):
        self.assertTrue(self.module.should_persist_tool_check(1, "2026-08-12", "2026-08-12"))


if __name__ == "__main__":
    unittest.main()
