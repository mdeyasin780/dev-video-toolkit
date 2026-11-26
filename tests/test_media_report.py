import unittest

from media_report import format_duration, markdown_report


class ReportTests(unittest.TestCase):
    def test_duration_format(self):
        self.assertEqual(format_duration(65.2), "1:05")
        self.assertEqual(format_duration(3661), "1:01:01")

    def test_report_contains_summary_and_error_section(self):
        report = markdown_report([
            {"filename": "clip.mp4", "duration_seconds": 65, "video": {"codec": "h264", "width": 320, "height": 240}, "audio": {"codec": "aac"}},
            {"file": "broken.mov", "error": "cannot decode"},
        ], "Daily Assets")
        self.assertIn("# Daily Assets", report)
        self.assertIn("`clip.mp4`", report)
        self.assertIn("Files needing attention", report)
        self.assertIn("cannot decode", report)


if __name__ == "__main__":
    unittest.main()
