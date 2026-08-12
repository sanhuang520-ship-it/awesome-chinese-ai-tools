#!/usr/bin/env python3
import unittest

from capture_github_traffic import build_snapshot


class CaptureGithubTrafficTest(unittest.TestCase):
    def test_snapshot_preserves_aggregate_evidence_and_boundaries(self):
        payloads = {
            "": {"stargazers_count": 7, "forks_count": 1, "open_issues_count": 0, "subscribers_count": 0},
            "/traffic/views": {"count": 113, "uniques": 50},
            "/traffic/clones": {"count": 968, "uniques": 413},
            "/traffic/popular/referrers": [{"referrer": "github.com", "count": 40, "uniques": 28}],
            "/traffic/popular/paths": [{"path": "/owner/repo", "title": "Overview", "count": 66, "uniques": 41}],
        }
        snapshot = build_snapshot(payloads.__getitem__, "2026-08-13T00:24:00+08:00")
        self.assertEqual(50, snapshot["traffic"]["uniqueVisitors"])
        self.assertEqual(413, snapshot["traffic"]["uniqueCloners"])
        self.assertEqual("github.com", snapshot["traffic"]["topReferrers"][0]["name"])
        self.assertIn("no token", snapshot["privacy"])
        self.assertIn("must not be called users", snapshot["notes"])
        self.assertIn("cannot be used as a Star conversion rate", snapshot["notes"])


if __name__ == "__main__":
    unittest.main()
