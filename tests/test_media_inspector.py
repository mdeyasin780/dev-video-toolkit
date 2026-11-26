import unittest

from media_inspector import _integer, _number


class NormalizationTests(unittest.TestCase):
    def test_number(self):
        self.assertEqual(_number("12.34567"), 12.346)
        self.assertIsNone(_number("not-a-number"))

    def test_integer(self):
        self.assertEqual(_integer("42"), 42)
        self.assertIsNone(_integer(None))


if __name__ == "__main__":
    unittest.main()
