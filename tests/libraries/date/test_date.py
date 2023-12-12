import unittest
from date_handler import DateHandler  # Assuming the class is in 'date_handler.py'

class TestDateHandler(unittest.TestCase):

    def test_default_format(self):
        dh = DateHandler('20230101')
        self.assertEqual(str(dh), '2023-01-01')

    def test_custom_format(self):
        dh = DateHandler('20230101')
        self.assertEqual(dh.format_date('%d-%m-%Y'), '01-01-2023')

    def test_last_friday(self):
        dh = DateHandler('20231130')  # 30th Nov 2023 is a Thursday
        dh.find_latest_friday()
        self.assertEqual(str(dh), '2023-11-24')  # Last Friday should be 24th Nov 2023

    def test_date_update(self):
        dh = DateHandler('20230101')
        dh.update_date('20231224')
        self.assertEqual(str(dh), '2023-12-24')

    def test_add_days(self):
        dh = DateHandler('20230101')
        dh.add_days(10)
        self.assertEqual(str(dh), '2023-01-11')

    def test_comparison(self):
        dh1 = DateHandler('20230101')
        dh2 = DateHandler('20230102')
        self.assertTrue(dh1 < dh2)
        self.assertFalse(dh1 > dh2)
        self.assertTrue(dh1 <= dh2)
        self.assertTrue(dh2 >= dh1)

    def test_invalid_date_format(self):
        with self.assertRaises(ValueError):
            DateHandler('01-2023-01')

if __name__ == '__main__':
    unittest.main()
