#!/usr/bin/env python3

import json
import unittest
from pathlib import Path

from check_compatibility import repository_skills


ROOT = Path(__file__).resolve().parents[1]


class CompatibilityDataTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            (ROOT / "data" / "compatibility.json").read_text(encoding="utf-8")
        )

    def test_all_repository_skills_are_recorded(self):
        self.assertEqual(self.data["skills"], repository_skills())

    def test_verified_counts_match_recorded_skills(self):
        count = len(self.data["skills"])
        self.assertEqual(self.data["results"]["discovery"]["count"], count)
        self.assertEqual(self.data["results"]["codexInstall"]["identicalCount"], count)

    def test_install_evidence_is_isolated_and_discloses_stale_global_copies(self):
        install = self.data["results"]["codexInstall"]
        self.assertEqual("1.5.22", install["cliVersion"])
        self.assertEqual("isolated-project-copy", install["scope"])
        self.assertTrue(install["globalSkillsUnchanged"])
        self.assertTrue((ROOT / install["case"]).is_file())
        existing = self.data["results"]["existingGlobalCopies"]
        self.assertEqual("partial", existing["status"])
        self.assertEqual(0, existing["identicalCount"])
        self.assertEqual(len(self.data["skills"]), existing["total"])

    def test_project_update_evidence_uses_a_different_historical_fixture(self):
        update = self.data["results"]["projectUpdate"]
        count = len(self.data["skills"])
        self.assertEqual("verified", update["status"])
        self.assertEqual("1.5.22", update["cliVersion"])
        self.assertEqual("isolated-project-copy", update["scope"])
        self.assertEqual("npx --yes skills@1.5.22 update -p -y", update["command"])
        self.assertEqual(count, update["fixtureDifferentCount"])
        self.assertEqual(count, update["updatedCount"])
        self.assertEqual(count, update["identicalFolderCount"])
        self.assertTrue(update["globalSkillsUnchanged"])
        self.assertTrue((ROOT / update["case"]).is_file())

    def test_activation_evidence_points_to_a_case(self):
        activation = self.data["results"]["codexActivation"]
        self.assertEqual(activation["status"], "partial")
        self.assertEqual(
            activation["verifiedSkills"],
            ["chinese-typography", "github-readme-cn", "chinese-work-report", "bookkeeping-cn", "ecommerce-copywriting", "homework-tutor-cn", "ai-learning-coach", "book-digest-cn", "chinese-lesson-plan", "chinese-design-md", "chinese-web-themes", "guochao-visual-cn", "guofeng-threejs"],
        )
        expected_cases = [
            f"cases/{skill}-codex.md" for skill in activation["verifiedSkills"]
        ]
        self.assertEqual(activation["cases"], expected_cases)

        examples = (ROOT / "EXAMPLES.md").read_text(encoding="utf-8")
        case_index = (ROOT / "cases" / "README.md").read_text(encoding="utf-8")
        for case in expected_cases:
            self.assertTrue((ROOT / case).is_file())
            relative_case = case.removeprefix("cases/")
            self.assertIn(f"cases/{relative_case}", examples)
            self.assertIn(f"({relative_case})", case_index)

    def test_codex_client_version_matches_every_activation_case(self):
        activation = self.data["results"]["codexActivation"]
        version = "0.147.0-alpha.6.5"
        self.assertEqual(self.data["clients"]["codex"], f"Codex CLI {version}")
        self.assertEqual(activation["clientVersion"], f"codex-cli {version}")
        for case in activation["cases"]:
            with self.subTest(case=case):
                body = (ROOT / case).read_text(encoding="utf-8")
                self.assertIn(f"Codex CLI `{version}`", body)
                self.assertNotIn("Codex desktop", body)

    def test_per_skill_outcomes_cover_activation_evidence(self):
        activation = self.data["results"]["codexActivation"]
        results = activation["skillResults"]
        self.assertEqual(set(activation["verifiedSkills"]), set(results))
        totals = {"completed": 0, "waiting-input": 0, "bounded-retest": 0}
        for skill, result in results.items():
            with self.subTest(skill=skill):
                self.assertIn(result["outcome"], totals)
                totals[result["outcome"]] += 1
                self.assertEqual(f"cases/{skill}-codex.md", result["case"])
                self.assertTrue(result["labelZh"])
                self.assertTrue(result["summaryZh"])
        self.assertEqual({"completed": 10, "waiting-input": 1, "bounded-retest": 2}, totals)

    def test_unrun_clients_are_not_claimed_as_verified(self):
        self.assertEqual(self.data["results"]["cursor"]["status"], "not-tested")

    def test_claude_code_records_observation_without_claiming_activation(self):
        # 2026-08-26 起 Claude Code 有了发现与加载的实测证据，但那一轮是自测：
        # 选择调用 Skill 的模型，就是撰写任务措辞和判定结果的模型。
        # 它不与 Codex 那轮同级（Codex 在提示词未点名时自己声明了 Skill 名称），
        # 所以这里守的是「可以记录观察，但不许把它写成自动触发通过」。
        result = self.data["results"]["claudeCode"]
        self.assertEqual("partial", result["status"])
        self.assertIs(False, result["activationRecorded"])
        self.assertEqual(13, result["discoveryCount"])
        self.assertEqual(13, result["loadCount"])
        # 首轮 12/13（guofeng-threejs 副本过期）；08-28 副本追平后 7 项重跑为 13/13。
        # 守的是「两项之和必须等于 13」——不许把某一项悄悄从分母里拿掉。
        self.assertEqual(13, result["taskCoverageCompleted"] + result["taskCoveragePartial"])
        self.assertEqual(13, result["taskCoverageCompleted"])
        self.assertEqual("2026-08-28", result["retestedAt"])
        self.assertTrue((ROOT / result["case"]).is_file())

    def test_preregistered_retests_preserve_executed_and_remaining_counts(self):
        result = self.data["results"]["prospectiveRetests"]
        self.assertEqual(6, result["plannedCount"])
        self.assertEqual(6, result["executedCount"])
        self.assertEqual(4, result["passedCount"])
        self.assertEqual(2, result["failedCount"])
        self.assertEqual(0, result["remainingCount"])
        self.assertEqual({"book-digest-cn", "chinese-design-md", "chinese-lesson-plan", "chinese-web-themes", "guochao-visual-cn", "guofeng-threejs"}, set(result["results"]))
        for skill, record in result["results"].items():
            with self.subTest(skill=skill):
                self.assertIn(record["passedChecks"], (3, 4))
                self.assertEqual(4, record["totalChecks"])
                self.assertTrue((ROOT / record["case"]).is_file())
        remediation = result["remediationRetests"]
        self.assertEqual("completed", remediation["status"])
        self.assertEqual(2, remediation["executedCount"])
        self.assertEqual(2, remediation["passedCount"])
        self.assertEqual(0, remediation["failedCount"])
        self.assertEqual({"chinese-web-themes", "guofeng-threejs"}, set(remediation["results"]))
        self.assertEqual(294, remediation["results"]["guofeng-threejs"]["measuredCharacters"])

    def test_compatibility_submission_separates_naming_activation_and_completion(self):
        template = (ROOT / ".github" / "ISSUE_TEMPLATE" / "compatibility-result.yml").read_text(encoding="utf-8")
        for field in ("id: named_skill", "id: environment", "id: activation", "id: completion", "id: evidence", "id: boundary"):
            with self.subTest(field=field):
                self.assertIn(field, template)
        self.assertIn("否，没有点名", template)
        self.assertIn("失败、报错或卡住", template)
        self.assertIn("未执行，平台、账户或环境", template)
        self.assertIn("compatibility-result.schema.json", template)
        self.assertIn("截图不是必需的", template)

    def test_public_compatibility_summary_matches_recorded_cli_client(self):
        summary = (ROOT / "COMPATIBILITY.md").read_text(encoding="utf-8")
        self.assertIn("Codex CLI `0.147.0-alpha.6.5`", summary)
        self.assertNotIn("当前 Codex 客户端为桌面版", summary)
        self.assertIn("compatibility-result.yml", summary)
        self.assertIn("隔离项目安装内容", summary)
        # 2026-08-28 重装后全局副本已追平，但「曾经漂移到 0/13」这个事实不能因此被抹掉：
        # 它是「安装不是持续同步」的原始证据。守卫改为同时锁住历史与修复两半。
        self.assertIn("曾 0 / 13", summary)
        self.assertIn("重装后 13 / 13", summary)
        self.assertIn("安装不是自动更新", summary)

    def test_global_update_failure_stays_recorded(self):
        # update -g 静默跳过无锁条目的 Skill，是本仓库唯一一条 ❌ 结论。
        # 重装修好了本机副本，但不等于 CLI 的这个行为被修复了，不许因此删掉。
        summary = (ROOT / "COMPATIBILITY.md").read_text(encoding="utf-8")
        self.assertIn("不更新无锁条目的 Skill", summary)
        result = self.data["results"]["globalUpdate"]
        self.assertEqual("failed", result["status"])
        self.assertEqual(0, result["ourSkillsChangedCount"])
        self.assertEqual(0, result["exitCode"])          # 报成功却没更新，这才是问题所在
        self.assertEqual(7, result["skippedWithoutWarningCount"])
        self.assertTrue((ROOT / result["case"]).is_file())


if __name__ == "__main__":
    unittest.main()
