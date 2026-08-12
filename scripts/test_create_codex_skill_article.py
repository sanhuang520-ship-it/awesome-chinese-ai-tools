#!/usr/bin/env python3
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CreateCodexSkillArticleTest(unittest.TestCase):
    def setUp(self): self.body=(ROOT/"create-codex-skill"/"index.html").read_text(encoding="utf-8")
    def test_structure(self):
        for phrase in ("name: my-skill","description:","scripts/","references/","assets/","openai.yaml"): self.assertIn(phrase,self.body)
        self.assertIn("name</code> 与 <code>description</code> 是必填项",self.body)
    def test_sources(self):
        self.assertIn("https://learn.chatgpt.com/docs/build-skills",self.body)
        self.assertIn("../skills/chinese-typography/SKILL.md",self.body)
        self.assertIn("../cases/chinese-typography-codex.md",self.body)
    def test_boundaries(self):
        self.assertIn("自动读取不等于任务完成",self.body)
        self.assertIn("不在任务里直接写 Skill 名称",self.body)
        self.assertNotIn("一定会自动触发",self.body)
    def test_json_ld(self):
        payload=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',self.body,re.S).group(1))
        self.assertEqual(len(payload["step"]),5)
if __name__=="__main__": unittest.main()
