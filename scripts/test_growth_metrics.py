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

    def test_traffic_snapshot_does_not_call_clones_users(self):
        data = json.loads((ROOT / "metrics" / "2026-08-12-traffic.json").read_text(encoding="utf-8"))
        self.assertEqual(14, data["windowDays"])
        self.assertGreater(data["traffic"]["uniqueCloners"], data["traffic"]["uniqueVisitors"])
        notes = data["notes"].lower()
        self.assertIn("must not be called users", notes)
        self.assertIn("cannot prove", notes)

    def test_v111_snapshot_does_not_claim_growth(self):
        data = json.loads((ROOT / "metrics" / "2026-08-12-v1.1.1.json").read_text(encoding="utf-8"))
        self.assertEqual("v1.1.1", data["release"]["tag"])
        self.assertEqual(57, data["release"]["localTests"])
        self.assertEqual(7, data["repositoryMetrics"]["stars"])
        self.assertIn("cannot be credited with Star growth", data["notes"])

    def test_search_content_launch_preserves_missing_metric_and_distribution_state(self):
        data = json.loads((ROOT / "metrics" / "2026-08-12-search-content-launch.json").read_text(encoding="utf-8"))
        self.assertEqual("not-refreshed", data["repositoryMetrics"]["status"])
        self.assertEqual("not-published", data["externalDistribution"]["status"])
        self.assertEqual(200, data["publishedEndpoints"]["codexSkillNotTriggering"]["httpStatus"])
        self.assertEqual(200, data["publishedEndpoints"]["createCodexSkill"]["httpStatus"])
        self.assertIn("must not be called current", data["notes"])
        self.assertIn("cannot be attributed", data["notes"])

    def test_owner_traffic_snapshot_keeps_full_discovery_and_privacy_boundaries(self):
        data = json.loads((ROOT / "metrics" / "2026-08-13-traffic-owner.json").read_text(encoding="utf-8"))
        self.assertEqual(14, data["windowDays"])
        self.assertEqual(50, data["traffic"]["uniqueVisitors"])
        self.assertEqual(413, data["traffic"]["uniqueCloners"])
        self.assertIn("Google", {item["name"] for item in data["traffic"]["topReferrers"]})
        self.assertIn("SKILLS.md", data["traffic"]["topPaths"][1]["path"])
        self.assertIn("no token", data["privacy"])
        self.assertIn("must not be called users", data["notes"])
        self.assertIn("cannot be used as a Star conversion rate", data["notes"])


if __name__ == "__main__":
    unittest.main()
