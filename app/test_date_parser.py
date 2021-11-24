import unittest
import datetime

from date_parser import DateParser

class TestDateParserMethods(unittest.TestCase):

    def test_parse_date(self):
        data = DateParser()
        parsed_data = data.convert("May 9, 2020 8:09:03 PM")
        self.assertEqual(str(parsed_data), "2020-05-09 20:09:03")
        parsed_data = data.convert("May 9, PM")
        self.assertEqual(parsed_data, None)

    def test_parse_date_invalid(self):
        data = DateParser()
        parsed_data = data.convert("Maps 2020 PM")
        self.assertEqual(parsed_data, None)

    def test_parse_date_string(self):
        data = DateParser()
        my_date = datetime.datetime(2020, 3, 15, 20, 9, 3)
        parsed_data = data.convert_reverse(my_date)
        self.assertEqual(str(parsed_data), "Sun Mar 15 20:09:03 2020")

if __name__ == '__main__':
    unittest.main()

