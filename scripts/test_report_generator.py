#!/usr/bin/env python3
import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.ids=set(); self.scripts=[]; self._script=False
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.ids.add(attrs.get("id")); self._script=tag=="script"
    def handle_endtag(self, tag):
        if tag=="script": self._script=False
    def handle_data(self, data):
        if self._script: self.scripts.append(data)

class ReportGeneratorTest(unittest.TestCase):
    def setUp(self): self.body=(ROOT/"report"/"index.html").read_text(encoding="utf-8")
    def test_required_controls_and_local_only_claim(self):
        parser=Parser(); parser.feed(self.body)
        for item in ("report-form","environment","activation","completion","preview","download","copy","status"):
            self.assertIn(item, parser.ids)
        self.assertIn("不上传、不持久保存", self.body)
    def test_blocked_state_and_privacy_scanner_are_implemented(self):
        self.assertIn("completion.value='not-run'", self.body)
        self.assertIn("completion.value='unknown'", self.body)
        self.assertIn("activation.value='unknown'", self.body)
        self.assertIn("knownSkills.has(skill)", self.body)
        self.assertIn("github_pat", self.body)
        self.assertIn("navigator.clipboard.writeText", self.body)
        self.assertNotIn("fetch(", self.body)
        self.assertNotIn("localStorage", self.body)

    def test_inline_javascript_parses(self):
        parser=Parser(); parser.feed(self.body)
        self.assertEqual(len(parser.scripts), 1)
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as handle:
            handle.write(parser.scripts[0]); handle.flush()
            result=subprocess.run(["node", "--check", handle.name], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

if __name__ == "__main__": unittest.main()
