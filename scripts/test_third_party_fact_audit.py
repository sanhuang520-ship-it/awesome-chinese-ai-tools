#!/usr/bin/env python3

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ThirdPartyFactAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads(
            (ROOT / "metrics" / "2026-08-13-third-party-skill-fact-audit.json").read_text(encoding="utf-8")
        )
        catalog = json.loads((ROOT / "data" / "skills.json").read_text(encoding="utf-8"))
        cls.skills = {}
        for skill in catalog["skills"]:
            repo = skill.get("repo")
            if not repo and skill.get("url", "").startswith("https://github.com/"):
                repo = skill["url"].removeprefix("https://github.com/").rstrip("/")
            if repo:
                cls.skills[repo] = skill

    def test_audit_is_bounded_and_did_not_execute_third_party_code(self):
        self.assertEqual(7, len(self.audit["entries"]))
        self.assertFalse(self.audit["method"]["executedThirdPartyCode"])
        self.assertFalse(self.audit["method"]["independentOutcomeTesting"])
        self.assertIn("不安装或运行第三方代码", self.audit["method"]["boundaryZh"])

    def test_every_entry_has_immutable_upstream_evidence(self):
        for entry in self.audit["entries"]:
            with self.subTest(repo=entry["repo"]):
                self.assertRegex(entry["commit"], r"^[0-9a-f]{40}$")
                self.assertRegex(entry["readmeSha"], r"^[0-9a-f]{40}$")
                self.assertIn(entry["decision"], {"corrected", "retained"})
                self.assertIn(entry["repo"], self.skills)

    def test_promotional_outcome_and_borrowed_star_claims_are_not_catalog_facts(self):
        combined = "\n".join(self.skills[entry["repo"]]["desc"] for entry in self.audit["entries"])
        for stale_claim in (
            "26万⭐",
            "20.6% 降到 10.1%",
            "117 星但 1.1 万安装",
            "目前 star 数最高",
            "7000+ 收录",
        ):
            with self.subTest(claim=stale_claim):
                self.assertNotIn(stale_claim, combined)
        self.assertIn("未独立复现", self.skills["redbaronyyyyy-eng/humanizer-zh-academic"]["desc"])
        self.assertIn("未独立复现", self.skills["qingshanliuci/cnki-aigc---skill"]["desc"])
        self.assertIn("账号权限", self.skills["zhjiang22/openclaw-xhs"]["desc"])

    def test_catalog_does_not_encode_a_dynamic_star_ranking(self):
        all_descriptions = "\n".join(skill["desc"] for skill in self.skills.values())
        self.assertNotIn("目前 star 数最高", all_descriptions.lower())
        self.assertIn("未独立复现", all_descriptions)


if __name__ == "__main__":
    unittest.main()
