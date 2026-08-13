#!/usr/bin/env python3
import unittest

from check_github_release import TAG, validate_release


class GithubReleaseCheckTest(unittest.TestCase):
    def valid_release(self):
        return {
            "tag_name": TAG,
            "draft": False,
            "prerelease": False,
            "name": "v1.2.0 — 可复现证据、安全审计与双语发现",
            "body": "10 项完成；旧失败保留；Claude Code 与 Cursor 待测；不是安全认证；Stars 仍为 7。",
        }

    def test_valid_public_release_passes(self):
        self.assertEqual([], validate_release(self.valid_release(), {"object": {"type": "tag", "sha": "tag-object"}}))

    def test_draft_prerelease_wrong_tag_and_weak_body_fail(self):
        release = self.valid_release()
        release.update({"tag_name": "v1.1.1", "draft": True, "prerelease": True, "body": "empty"})
        failures = validate_release(release, {"object": {"type": "commit", "sha": "ab44cd965d4167e6efb3849876ab5efef670f978"}})
        for phrase in ("release tag", "release is draft", "release is prerelease", "tag is not annotated", "release body missing"):
            self.assertTrue(any(phrase in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
