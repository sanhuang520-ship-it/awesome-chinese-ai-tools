#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path

from check_internal_links import missing_links


ROOT = Path(__file__).resolve().parents[1]


class InternalLinksTest(unittest.TestCase):
    def test_published_site_has_no_missing_explicit_links(self):
        self.assertEqual([], missing_links(ROOT))

    def test_missing_relative_link_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text('<a href="missing/">broken</a>', encoding="utf-8")
            self.assertEqual(["index.html: missing missing/"], missing_links(root))


if __name__ == "__main__":
    unittest.main()
