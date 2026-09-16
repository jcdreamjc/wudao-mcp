import unittest
from check_sources import compare, date_text, validate


class SourceCheckTests(unittest.TestCase):
    def setUp(self):
        self.dates = ["2026-09-15"]
        self.row = {"date": self.dates[0], "open": 10, "high": 12, "low": 9, "close": 11}

    def test_valid(self):
        self.assertEqual(validate([self.row], self.dates), [])

    def test_missing_date(self):
        self.assertIn("date_set_or_order_mismatch", validate([], self.dates))

    def test_duplicate(self):
        self.assertIn("duplicate_date", validate([self.row, self.row], self.dates))

    def test_nan(self):
        self.assertIn("invalid_price", validate([{**self.row, "close": float("nan")}], self.dates))

    def test_ohlc(self):
        self.assertIn("ohlc_order_invalid", validate([{**self.row, "close": 13}], self.dates))

    def test_date(self):
        self.assertEqual(date_text("20260915"), "2026-09-15")

    def test_failed_is_not_zero_difference(self):
        self.assertEqual(compare({"status": "passed"}, {"status": "failed"})["status"], "not_comparable")

    def test_compare(self):
        left = {"status": "passed", "items": [{"code": "600519", "rows": [self.row]}]}
        self.assertEqual(compare(left, left)["fieldsChecked"], 4)
        right = {"status": "passed", "items": [{"code": "600519", "rows": [{**self.row, "close": 11.03}]}]}
        self.assertEqual(compare(left, right)["status"], "differences_found")


if __name__ == "__main__":
    unittest.main()
