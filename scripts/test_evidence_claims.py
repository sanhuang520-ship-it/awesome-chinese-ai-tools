#!/usr/bin/env python3

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = [
    ROOT / "README.md",
    ROOT / "SKILLS.md",
    ROOT / "index.html",
    ROOT / "blog" / "skill-pitfalls.md",
]


class EvidenceClaimsTest(unittest.TestCase):
    def test_installation_evidence_is_not_called_official_or_activation(self):
        combined = "\n".join(path.read_text(encoding="utf-8") for path in PUBLIC_FILES)
        forbidden = [
            "这个官方 CLI",
            "用官方 CLI 实测",
            "Claude Code 读的是 `~/.claude/skills/`",
            "装好后重启 Claude Code，**无需手动调用**",
        ]
        for claim in forbidden:
            with self.subTest(claim=claim):
                self.assertNotIn(claim, combined)

    def test_unknown_clients_remain_explicitly_unverified(self):
        compatibility = (ROOT / "COMPATIBILITY.md").read_text(encoding="utf-8")
        self.assertIn("| Claude Code | ⏳ 待测 |", compatibility)
        self.assertIn("| Cursor | ⏳ 待测 |", compatibility)

    def test_first_party_tool_copy_avoids_unmeasured_superlatives(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        tools = (ROOT / "data" / "tools.json").read_text(encoding="utf-8")
        forbidden = ["国内最好用", "效果最佳", "国内最强", "效果最准", "减少 70%", "完全免费，无限次"]
        for claim in forbidden:
            with self.subTest(claim=claim):
                self.assertNotIn(claim, index + tools)

    def test_ecommerce_examples_do_not_infer_unmeasured_outcomes_from_specs(self):
        skill = (ROOT / "skills" / "ecommerce-copywriting" / "SKILL.md").read_text(encoding="utf-8")
        examples = (ROOT / "EXAMPLES.md").read_text(encoding="utf-8")
        combined = skill + examples
        for claim in ("柠檬水放一天没金属味", "放一天没有金属味", "下午三点还烫嘴", "下午 3 点还烫嘴"):
            with self.subTest(claim=claim):
                self.assertNotIn(claim, combined)
        self.assertIn("不是法律意见、平台审核结果", skill)
        self.assertIn("只有用户提供并核对过的事实", examples)
        catalog_data = (ROOT / "data" / "skills.json").read_text(encoding="utf-8")
        generated = (ROOT / "SKILLS.md").read_text(encoding="utf-8")
        self.assertNotIn("广告法违禁词红线", catalog_data + generated)
        self.assertIn("不把机械禁词替换当作合规保证", catalog_data)
        self.assertIn("不把机械禁词替换当作合规保证", generated)

    def test_commercial_terms_are_presented_as_unverified_history(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        tools = (ROOT / "data" / "tools.json").read_text(encoding="utf-8")
        self.assertIn('"status": "unverified-snapshot"', tools)
        self.assertIn("链接存活不代表商业条款仍有效", tools)
        self.assertIn("这里是发现线索，不是实时价格库", index)
        self.assertIn("不会验证价格、额度、地区或账号资格", index)
        self.assertNotIn("t.priceFree", index)
        self.assertNotIn("t.pricePro", index)

    def test_tool_descriptions_avoid_unmeasured_ranking_language(self):
        tools = (ROOT / "data" / "tools.json").read_text(encoding="utf-8")
        forbidden = ["顶级", "最大", "最稳定", "最自然", "远超", "神器", "当天可上线", "无限生成"]
        for claim in forbidden:
            with self.subTest(claim=claim):
                self.assertNotIn(claim, tools)

    def test_retired_editorial_scores_do_not_drive_the_frontend(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        tools = (ROOT / "data" / "tools.json").read_text(encoding="utf-8")
        self.assertIn('"status": "retired"', tools)
        self.assertIn("不再用于前端徽章、评分、筛选或排序", tools)
        forbidden = ["t.stars", "t.rec", "t.hot", "onlyRec", "onlyHot", "编辑精选", "按精选程度和热度排序"]
        for claim in forbidden:
            with self.subTest(claim=claim):
                self.assertNotIn(claim, index)

    def test_skill_install_counts_are_not_called_actual_usage(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        skills = (ROOT / "data" / "skills.json").read_text(encoding="utf-8")
        self.assertIn("不等于独立用户或实际使用次数", index)
        self.assertIn('"status": "retired"', skills)
        self.assertNotIn("星数远低于实际使用量", index)
        self.assertNotIn("s.rec && !s.ours", index)

    def test_skills_sh_index_is_linked_without_calling_installs_users(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        english = (ROOT / "README.en.md").read_text(encoding="utf-8")
        self.assertIn("https://skills.sh/sanhuang520-ship-it/awesome-chinese-ai-tools", readme)
        self.assertNotIn("https://skills.sh/b/sanhuang520-ship-it/awesome-chinese-ai-tools", readme)
        self.assertIn("可能包含维护者安装核验", readme)
        self.assertIn("不等于独立用户、实际使用效果或质量认证", readme)
        self.assertIn("may include maintainer verification runs", english)
        self.assertIn("not a unique-user count, usage outcome, or quality certification", english)

    def test_agent_skills_directory_is_linked_with_evidence_boundaries(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        english = (ROOT / "README.en.md").read_text(encoding="utf-8")
        author_url = "https://agent-skills.md/authors/sanhuang520-ship-it"
        self.assertIn(author_url, readme)
        self.assertIn(author_url, english)
        self.assertIn("不代表独立兼容性实测、内容审核或质量认证", readme)
        self.assertIn("not independent compatibility testing, content review, or quality certification", english)
        self.assertIn("分类与标签正在刷新复核", readme)

    def test_workflow_examples_are_not_presented_as_ranked_recommendations(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        archive = (ROOT / "SCENARIOS.md").read_text(encoding="utf-8")
        self.assertIn("工作流示例", index)
        self.assertIn("不代表排名或效果保证", index)
        self.assertIn("可选入口：", index)
        self.assertNotIn("工作流推荐", index)
        self.assertNotIn("获得最适合的 AI 工具组合", index)
        self.assertNotIn("推荐工具", archive)

    def test_current_workflow_copy_avoids_unverified_speed_and_privacy_claims(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        forbidden = [
            "10 分钟出 PPT",
            "最快当天完成",
            "当天上线",
            "代码质量高",
            "可私有部署不泄密",
            "数据完全不出公司网络",
            "GitHub 50k+ stars",
        ]
        for claim in forbidden:
            with self.subTest(claim=claim):
                self.assertNotIn(claim, index)

    def test_picker_is_a_filter_not_a_ranker(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("按条件筛选工具入口", index)
        self.assertIn("按目录顺序查看匹配项", index)
        self.assertNotIn("直接告诉你最该用的工具", index)
        self.assertNotIn("3 秒帮你选", index)

    def test_nav_counts_wait_for_data_instead_of_showing_stale_defaults(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('<b id="skc">—</b> Skills', index)
        self.assertIn('<b id="tc">—</b> 工具', index)

    def test_default_global_search_targets_the_primary_skills_view(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('placeholder="搜索 Skill、场景…"', index)
        self.assertIn("let activeView = 'skills'", index)
        self.assertIn("if (activeView === 'price') return", index)
        self.assertIn("if (activeView === 'skills')", index)
        self.assertIn("search.disabled = inPrice", index)
        self.assertIn("button.hidden = !inTools", index)

    def test_generated_skill_catalog_leads_to_reproducible_evidence(self):
        generator = (ROOT / "scripts" / "daily_check.py").read_text(encoding="utf-8")
        catalog = (ROOT / "SKILLS.md").read_text(encoding="utf-8")
        for phrase in (
            "Codex 13/13 自动触发实测",
            "Claude Code 与 Cursor 待测",
            "compatibility-result.yml",
            "安装与排错页",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, generator)
                self.assertIn(phrase, catalog)

    def test_compatibility_page_routes_people_to_rendered_case_records(self):
        page = (ROOT / "compatibility" / "index.html").read_text(encoding="utf-8")
        prefix = "https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/blob/main/cases/"
        for case in (ROOT / "cases").glob("*-codex.md"):
            with self.subTest(case=case.name):
                self.assertIn(prefix + case.name, page)
                self.assertNotIn(f'href="../cases/{case.name}"', page)

    def test_generated_catalog_does_not_call_every_third_party_entry_tested(self):
        generator = (ROOT / "scripts" / "daily_check.py").read_text(encoding="utf-8")
        catalog = (ROOT / "SKILLS.md").read_text(encoding="utf-8")
        for phrase in ("其他中文条目", "不等于逐项功能实测"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, generator)
                self.assertIn(phrase, catalog)
        self.assertIn("{cn_n} 个中文条目", generator)
        self.assertIn("68 个中文条目", catalog)
        self.assertNotIn("68 个中文原创", catalog)

    def test_skill_activation_is_described_as_client_dependent(self):
        generator = (ROOT / "scripts" / "daily_check.py").read_text(encoding="utf-8")
        current = "\n".join(
            (ROOT / relative).read_text(encoding="utf-8")
            for relative in ("README.md", "SKILLS.md", "index.html")
        )
        self.assertIn("是否触发取决于客户端、版本、安装位置和任务措辞", generator)
        self.assertIn("是否触发取决于客户端、版本、安装位置和任务措辞", current)
        self.assertNotIn("AI 会自动判断何时激活", current)
        self.assertNotIn("AI 自动判断何时激活", current)

    def test_third_party_install_records_are_not_called_usage(self):
        skills = (ROOT / "data" / "skills.json").read_text(encoding="utf-8")
        catalog = (ROOT / "SKILLS.md").read_text(encoding="utf-8")
        self.assertIn("该数值不等于独立用户或实际使用", skills)
        self.assertIn("该数值不等于独立用户或实际使用", catalog)
        self.assertNotIn("星数完全反映不出使用量", skills + catalog)

    def test_public_copy_distinguishes_skill_entries_from_repositories(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("184 个 Skill 条目来自 141 个仓库", readme)
        self.assertIn("141 个来源仓库复检", readme)
        self.assertNotIn("184 个 Skill 仓库复检", readme)
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("每个仓库都验证过真实存在", index)
        self.assertNotIn("个中文原创", index)
        self.assertNotIn("全部已验证仓库真实存在", index)
        self.assertIn("其他条目不等于逐项功能实测", index)

    def test_english_overview_preserves_evidence_boundaries(self):
        english = (ROOT / "README.en.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("184 Agent Skill entries from 141 source repositories", english)
        self.assertIn("Claude Code and Cursor task-level compatibility are still untested", english)
        self.assertIn("Installation, discovery, automatic activation, and task completion are separate claims", english)
        self.assertIn("Ten completed the recorded task", english)
        self.assertIn("one correctly stopped to request required input", english)
        self.assertIn("two large tasks failed before passing reduced-scope retests", english)
        self.assertNotIn("Eleven completed on the first task", english)
        self.assertIn("python3 scripts/audit_skill.py /path/to/skill", english)
        self.assertIn("does not import, install or execute the target", english)
        self.assertIn("zero-finding result does **not** mean the Skill is safe", english)
        self.assertIn("python3 scripts/check_compatibility_reports.py", english)
        self.assertIn("clone counts and Stars are not", english)
        self.assertIn("[English](README.en.md)", readme)
        self.assertIn("README.en.md", llms)

    def test_stale_alternative_pages_are_not_indexed_as_current_advice(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for page in sorted((ROOT / "alternatives").glob("*.html")):
            with self.subTest(page=page.name):
                body = page.read_text(encoding="utf-8")
                self.assertIn('<meta name="robots" content="noindex, nofollow">', body)
                self.assertIn("历史快照", body)
                self.assertNotIn(f"alternatives/{page.name}", sitemap)

    def test_indexed_pitfalls_article_marks_historical_counts_as_a_snapshot(self):
        article = (ROOT / "blog" / "skill-pitfalls.md").read_text(encoding="utf-8")
        self.assertIn("快照说明（2026-08-12）", article)
        self.assertIn("分类只表示中文场景，不能证明原创归属", article)
        self.assertIn("链接可访问不等于逐项功能实测", article)
        self.assertNotIn("于是我收录了 130 个（其中 59 个中文原创）", article)

    def test_security_policy_routes_sensitive_reports_privately(self):
        policy = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("security/advisories/new", policy)
        self.assertIn("请不要在公开 Issue", policy)
        self.assertIn("第三方条目只做目录收录和链接复检", policy)
        self.assertIn("[🔒 安全报告](SECURITY.md)", readme)

    def test_community_policy_rejects_manipulated_growth(self):
        conduct = (ROOT / "CODE_OF_CONDUCT.md").read_text(encoding="utf-8")
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        for phrase in ("买星", "刷星", "互星", "伪造实测", "推广、返利、追踪参数"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, conduct)
        self.assertIn("[社区行为规范](CODE_OF_CONDUCT.md)", contributing)

    def test_readme_first_screen_keeps_one_clear_value_and_action_path(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        first_screen = readme.split("## 这是什么", 1)[0]
        self.assertEqual(4, first_screen.count("[!["))
        self.assertEqual(3, first_screen.count("img.shields.io"))
        for label in ("在线浏览与搜索", "安装与排错", "看真实输出", "看兼容性证据"):
            with self.subTest(label=label):
                self.assertIn(label, first_screen)
        for secondary in ("安全报告", "中文开箱组合", "完整清单", "12 种画风对照"):
            with self.subTest(secondary=secondary):
                self.assertNotIn(secondary, first_screen)
        self.assertIn(
            "npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --list",
            first_screen,
        )



if __name__ == "__main__":
    unittest.main()
