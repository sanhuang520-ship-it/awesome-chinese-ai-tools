#!/usr/bin/env python3

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GrowthMetricsTest(unittest.TestCase):
    def test_observation_records_reject_causal_attribution(self):
        records = sorted((ROOT / "metrics").glob("*.json"))
        self.assertGreaterEqual(len(records), 2)
        for record in records:
            data = json.loads(record.read_text(encoding="utf-8"))
            with self.subTest(record=record.name):
                notes = data.get("notes", "").lower()
                self.assertTrue("attribut" in notes or "归因" in notes)

    def test_latest_release_verification_is_complete(self):
        data = json.loads((ROOT / "metrics" / "2026-08-12-evidence-launch.json").read_text(encoding="utf-8"))
        state = data["releaseState"]
        self.assertEqual(state["publicEndpointsChecked"], state["publicEndpointsOk"])
        self.assertEqual("success", state["pagesDeployment"])


if __name__ == "__main__":
    unittest.main()
