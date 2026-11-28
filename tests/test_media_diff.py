import unittest

from media_diff import diff_manifests


def record(path, duration):
    return {"file": path, "filename": path.rsplit("/", 1)[-1], "duration_seconds": duration}


class DiffTests(unittest.TestCase):
    def test_detects_added_removed_changed_and_unchanged(self):
        before = [record("footage/a.mp4", 10), record("footage/b.mp4", 20), record("footage/old.mp4", 5)]
        after = [record("footage/a.mp4", 11), record("footage/b.mp4", 20), record("footage/new.mp4", 7)]
        result = diff_manifests(before, after)
        self.assertEqual(result["summary"], {"added": 1, "removed": 1, "changed": 1, "unchanged": 1})
        self.assertEqual(result["added"][0]["filename"], "new.mp4")
        self.assertEqual(result["removed"][0]["filename"], "old.mp4")
        self.assertEqual(result["changed"][0]["before"]["duration_seconds"], 10)
        self.assertEqual(result["changed"][0]["after"]["duration_seconds"], 11)


if __name__ == "__main__":
    unittest.main()
