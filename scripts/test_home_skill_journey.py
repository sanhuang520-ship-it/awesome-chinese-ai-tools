#!/usr/bin/env python3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class HomeSkillJourneyTest(unittest.TestCase):
    def setUp(self):
        self.body = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_home_has_one_ordered_three_step_skill_journey(self):
        self.assertEqual(1, self.body.count('class="skill-journey"'))
        render_start = self.body.index("function renderSkills()")
        journey_start = self.body.index('class="skill-journey"')
        self.assertGreater(journey_start, render_start)
        expected = (
            ('href="create-codex-skill/"', "STEP 01"),
            ('href="codex-skill-not-triggering/"', "STEP 02"),
            ('href="reproduce/"', "STEP 03"),
        )
        positions = []
        for href, step in expected:
            self.assertIn(href, self.body)
            self.assertIn(step, self.body)
            positions.append(self.body.index(step))
        self.assertEqual(positions, sorted(positions))

    def test_primary_banner_count_is_reduced_to_two(self):
        self.assertEqual(2, self.body.count('class="skills-banner"'))
        self.assertIn('href="compatibility/"', self.body)
        self.assertIn('href="guides/"', self.body)

    def test_mobile_journey_collapses_to_one_column(self):
        self.assertIn(".skill-journey-grid{grid-template-columns:1fr}", self.body)

    def test_skill_descriptions_wrap_long_technical_paths(self):
        self.assertIn(".sk-desc{font-size:12.5px;color:var(--text2);line-height:1.65;flex:1;overflow-wrap:anywhere}", self.body)

if __name__ == "__main__":
    unittest.main()
