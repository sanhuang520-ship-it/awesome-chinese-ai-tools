#!/usr/bin/env python3
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/"codex-skill-not-triggering"/"index.html"

class CodexTriggerArticleTest(unittest.TestCase):
    def setUp(self): self.body=PAGE.read_text(encoding="utf-8")
    def test_search_intent_and_five_layer_diagnosis_are_explicit(self):
        self.assertIn("Codex Skill 安装了却不自动触发",self.body)
        for phrase in ("发现失败","安装失败","自动触发未确认","完成失败或部分完成","环境阻断"):
            self.assertIn(phrase,self.body)
    def test_article_uses_recorded_versions_and_case(self):
        compatibility=json.loads((ROOT/"data"/"compatibility.json").read_text(encoding="utf-8"))
        self.assertIn("skills CLI <i>1.5.22</i>",self.body)
        self.assertIn(compatibility["results"]["codexActivation"]["clientVersion"].removeprefix("codex-cli "),self.body)
        self.assertIn("../cases/chinese-typography-codex.md",self.body)
    def test_article_preserves_evidence_boundaries(self):
        for phrase in ("不是准确率","不能归因给 Skill","其他 Codex 版本、Claude Code 或 Cursor","不是“所有中文排版任务都会触发”的保证"):
            self.assertIn(phrase,self.body)
        self.assertNotIn("必定触发",self.body)
    def test_article_has_complete_social_and_structured_metadata(self):
        for token in ('rel="canonical"','property="og:title"','property="og:description"','property="og:image"','name="twitter:card"','type="application/ld+json"'):
            self.assertIn(token,self.body)
        payload=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',self.body,re.S).group(1))
        self.assertEqual(len(payload["@graph"][1]["mainEntity"]),3)

if __name__=="__main__": unittest.main()
