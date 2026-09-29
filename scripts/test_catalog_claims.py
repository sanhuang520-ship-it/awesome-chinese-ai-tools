#!/usr/bin/env python3

import json
import unittest
from pathlib import Path

from check_catalog_claims import find_claim_violations


ROOT = Path(__file__).resolve().parents[1]


class CatalogClaimsTest(unittest.TestCase):
    def test_current_catalog_has_no_unstable_claims(self):
        data = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))
        self.assertEqual([], find_claim_violations(data))

    def test_rejects_rank_star_install_and_numeric_outcome_claims(self):
        descriptions = (
            "目前 Star 数最高的一份",
            "26万⭐框架完整汉化",
            "117 星但 1.1 万安装",
            "实测把检测率从 20.6% 降到 10.1%",
        )
        for description in descriptions:
            with self.subTest(description=description):
                data = {"skills": [{"name": "example", "desc": description, "descEn": ""}]}
                self.assertTrue(find_claim_violations(data))

    def test_checks_visible_english_summary_too(self):
        data = {
            "skills": [{
                "name": "example",
                "desc": "稳定的能力说明",
                "descEn": "Currently the highest-star Skill list",
            }]
        }
        self.assertEqual(["example.descEn: dynamic Star ranking"], find_claim_violations(data))

    def test_allows_capability_counts_and_attributed_non_numeric_boundaries(self):
        data = {"skills": [
            {"name": "one", "desc": "包含 20 个 Skill 与 4 种工作流", "descEn": "20 Skills across 4 workflows"},
            {"name": "two", "desc": "效果变化仅为上游案例，本仓库未独立复现", "descEn": "Upstream outcome case not reproduced here"},
            {"name": "ours", "ours": True, "desc": "本站实测 13/13", "descEn": ""},
        ]}
        self.assertEqual([], find_claim_violations(data))


if __name__ == "__main__":
    unittest.main()
