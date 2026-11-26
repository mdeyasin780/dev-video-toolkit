import tempfile
import unittest
from pathlib import Path

from media_inventory import inventory


class InventoryTests(unittest.TestCase):
    def test_inventory_finds_supported_extension(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "notes.txt").write_text("ignore me")
            (root / "nested").mkdir()
            (root / "nested" / "clip.mp4").write_bytes(b"not a real media file")
            result = inventory(root, {".mp4"})
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["file"].split("/")[-1], "clip.mp4")
            self.assertIn("error", result[0])


if __name__ == "__main__":
    unittest.main()
