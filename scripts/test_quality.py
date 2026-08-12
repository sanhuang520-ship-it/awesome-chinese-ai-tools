#!/usr/bin/env python3

import json
import tempfile
import unittest
from pathlib import Path

from check_quality import classify_files, runtime_network_evidence


ROOT = Path(__file__).resolve().parents[1]


class QualityDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "data" / "quality.json").read_text(encoding="utf-8"))

    def test_all_repository_owned_skills_are_covered(self):
        actual = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(actual, set(self.data["skills"]))

    def test_no_skill_claims_a_formal_certification(self):
        self.assertIn("no claim of formal security certification", self.data["method"])

    def test_only_documented_runtime_network_is_marked(self):
        networked = {name for name, item in self.data["skills"].items() if item["runtimeNetwork"]}
        self.assertEqual(networked, {"guofeng-threejs"})

    def test_chinese_labels_cover_every_quality_field(self):
        for name, item in self.data["skills"].items():
            with self.subTest(skill=name):
                self.assertTrue(item["filesZh"].strip())
                if item["sensitiveBoundary"] is not None:
                    self.assertTrue(item["sensitiveBoundaryZh"].strip())
                else:
                    self.assertIsNone(item["sensitiveBoundaryZh"])
                if item["runtimeNetwork"]:
                    self.assertTrue(item["networkDetailZh"].strip())

    def test_homepage_drawer_renders_quality_labels_with_certification_boundary(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        for phrase in ("data/quality.json", "静态质量与安全标签", "不是安全认证", "独立可执行脚本", "运行时网络", "重点边界"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, index)

    def test_quality_checker_covers_structure_and_link_escape(self):
        checker = (ROOT / "scripts" / "check_quality.py").read_text(encoding="utf-8")
        for phrase in ("frontmatter name does not match directory", "symbolic links require manual review", "missing or escaping local references"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, checker)

    def test_quality_checker_covers_file_layout_and_runtime_network_drift(self):
        checker = (ROOT / "scripts" / "check_quality.py").read_text(encoding="utf-8")
        for phrase in ("classify_files", "runtime_network_evidence", "runtime network evidence requires English and Chinese details"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, checker)

    def test_runtime_network_detection_ignores_markdown_links_but_finds_browser_imports(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            root = Path(directory)
            (root / "SKILL.md").write_text("[docs](https://example.com/docs)", encoding="utf-8")
            self.assertEqual([], runtime_network_evidence(root))
            (root / "demo.html").write_text(
                '<script type="module">import "https://cdn.example.com/pkg.js";</script>',
                encoding="utf-8",
            )
            evidence = runtime_network_evidence(root)
            self.assertEqual(["demo.html"], evidence)
            self.assertEqual("instructions+browser demos", classify_files(root))
            (root / "demo.html").write_text(
                '<script type="importmap">{"imports":{"pkg":"https://cdn.example.com/pkg.js"}}</script>',
                encoding="utf-8",
            )
            self.assertEqual(["demo.html"], runtime_network_evidence(root))

    def test_quality_document_records_versioned_reference_validation(self):
        quality = (ROOT / "QUALITY.md").read_text(encoding="utf-8")
        self.assertIn("skills-ref 0.1.1", quality)
        self.assertIn('agentskills validate "$skill"', quality)
        self.assertIn("不证明内容正确或跨客户端兼容", quality)


if __name__ == "__main__":
    unittest.main()
