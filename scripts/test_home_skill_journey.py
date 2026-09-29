#!/usr/bin/env python3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class HomeSkillJourneyTest(unittest.TestCase):
    def setUp(self):
        self.body = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_home_has_one_ordered_four_step_safe_use_journey(self):
        self.assertEqual(1, self.body.count('class="skill-journey"'))
        render_start = self.body.index("function renderSkills()")
        journey_start = self.body.index('class="skill-journey"')
        self.assertGreater(journey_start, render_start)
        expected = (
            ('href="guides/"', "STEP 01"),
            ('href="audit-skill/"', "STEP 02"),
            ('href="codex-skill-not-triggering/"', "STEP 03"),
            ('href="reproduce/"', "STEP 04"),
        )
        positions = []
        for href, step in expected:
            self.assertIn(href, self.body)
            self.assertIn(step, self.body)
            positions.append(self.body.index(step))
        self.assertEqual(positions, sorted(positions))
        self.assertIn("挑选 → 安装前审计 → 安装与排错 → 复现并提交", self.body)

    def test_primary_banner_count_is_reduced_to_two(self):
        self.assertEqual(2, self.body.count('class="skills-banner"'))
        self.assertIn('href="compatibility/"', self.body)
        self.assertIn('href="guides/"', self.body)

    def test_mobile_journey_collapses_to_one_column(self):
        self.assertIn("@media(max-width:900px) and (min-width:641px){.skill-journey-grid{grid-template-columns:repeat(2,1fr)}}", self.body)
        self.assertIn(".skill-journey-grid{grid-template-columns:1fr}", self.body)

    def test_skill_descriptions_wrap_long_technical_paths(self):
        self.assertIn(".sk-desc{font-size:12.5px;color:var(--text2);line-height:1.65;flex:1;overflow-wrap:anywhere}", self.body)

if __name__ == "__main__":
    unittest.main()
