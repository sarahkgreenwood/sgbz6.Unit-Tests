import unittest
from input_handler import validate_symbol, validate_chart_type, validate_time_series, validate_date

class TestStockVisualizerInputs(unittest.TestCase):

    def test_validate_symbol(self):
        self.assertTrue(validate_symbol('AAPL'))
        self.assertTrue(validate_symbol('GOOG'))
        self.assertTrue(validate_symbol('T'))
        self.assertFalse(validate_symbol('apple'))
        self.assertFalse(validate_symbol('AAPL123'))
        self.assertFalse(validate_symbol('TOOLONG'))

    def test_validate_chart_type(self):
        self.assertTrue(validate_chart_type('1'))
        self.assertTrue(validate_chart_type('2'))
        self.assertFalse(validate_chart_type('3'))
        self.assertFalse(validate_chart_type('Bar'))

    def test_validate_time_series(self):
        self.assertTrue(validate_time_series('1'))
        self.assertTrue(validate_time_series('2'))
        self.assertTrue(validate_time_series('3'))
        self.assertTrue(validate_time_series('4'))
        self.assertFalse(validate_time_series('5'))
        self.assertFalse(validate_time_series('Daily'))

    def test_validate_date(self):
        self.assertTrue(validate_date('2024-04-20'))
        self.assertFalse(validate_date('2024-4-20'))
        self.assertFalse(validate_date('20-04-2024'))
        self.assertFalse(validate_date('April 20, 2024'))

if __name__ == '__main__':
    unittest.main()
