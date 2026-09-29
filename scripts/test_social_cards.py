#!/usr/bin/env python3

import json
import re
import unittest

from sync_social_cards import BASE, DEFAULT_IMAGE, explainer_pages, sync_page


class SocialCardsTest(unittest.TestCase):
    def test_all_first_party_explainers_have_synchronized_social_cards(self):
        pages = list(explainer_pages())
        self.assertEqual(13, len(pages))
        for name, path in pages:
            with self.subTest(skill=name):
                body = path.read_text(encoding="utf-8")
                self.assertEqual(body, sync_page(body, name))
                self.assertIn('<meta name="twitter:card" content="summary_large_image">', body)
                for field in ("og:image", "og:image:width", "og:image:height", "og:image:alt"):
                    self.assertEqual(1, body.count(f'property="{field}"'))
                for field in ("twitter:title", "twitter:description", "twitter:image", "twitter:image:alt"):
                    self.assertEqual(1, body.count(f'name="{field}"'))
                match = re.search(r'<script\s+type="application/ld\+json">(.*?)</script>', body, re.S)
                self.assertIsNotNone(match)
                data = json.loads(match.group(1))
                candidates = data.get("@graph", [data])
                primary = next(item for item in candidates if item.get("@type") not in {"FAQPage", "BreadcrumbList"})
                image = re.search(r'<meta property="og:image" content="([^"]+)">', body).group(1)
                self.assertEqual(image, primary["image"])

    def test_default_card_is_absolute_and_has_social_preview_dimensions(self):
        self.assertTrue(DEFAULT_IMAGE.startswith(BASE))
        self.assertTrue(DEFAULT_IMAGE.endswith("/og.png"))
        for name, path in explainer_pages():
            if name in {"guofeng-threejs", "chinese-web-themes"}:
                continue
            body = path.read_text(encoding="utf-8")
            self.assertIn(f'<meta property="og:image" content="{DEFAULT_IMAGE}">', body)
            self.assertIn('<meta property="og:image:width" content="1200">', body)
            self.assertIn('<meta property="og:image:height" content="630">', body)


if __name__ == "__main__":
    unittest.main()
