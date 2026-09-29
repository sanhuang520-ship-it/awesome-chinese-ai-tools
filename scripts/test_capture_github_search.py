#!/usr/bin/env python3
import unittest

from capture_github_search import QUERIES, REPOSITORY, build_snapshot


class CaptureGithubSearchTest(unittest.TestCase):
    def test_snapshot_preserves_query_order_rank_and_boundaries(self):
        payloads = {
            query: {
                "total_count": 100 + index,
                "items": ([{"full_name": "example/other"}, {"full_name": REPOSITORY}]
                          if index == len(QUERIES) - 1 else [{"full_name": "example/other"}]),
            }
            for index, query in enumerate(QUERIES)
        }
        snapshot = build_snapshot(
            payloads.__getitem__,
            {"stargazers_count": 7, "forks_count": 1, "description": "desc", "homepage": "https://example.com", "topics": ["agent-skills"]},
            "2026-08-13T10:03:00+08:00",
        )
        self.assertEqual(list(QUERIES), [item["query"] for item in snapshot["queries"]])
        self.assertIsNone(snapshot["queries"][0]["targetRankInTop20"])
        self.assertEqual(2, snapshot["queries"][-1]["targetRankInTop20"])
        self.assertEqual({"stars": 7, "forks": 1}, snapshot["repositoryMetrics"])
        self.assertEqual("desc", snapshot["repositoryProfile"]["description"])
        self.assertEqual(["agent-skills"], snapshot["repositoryProfile"]["topics"])
        self.assertIn("cannot be attributed", snapshot["notes"])
        self.assertIn("does not promise", snapshot["notes"])


if __name__ == "__main__":
    unittest.main()
