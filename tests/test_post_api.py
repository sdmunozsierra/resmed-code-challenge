from datetime import datetime, timezone
from email.contentmanager import raw_data_manager
from re import S
import time
from collections import OrderedDict
from distutils.command.clean import clean
import unittest
from post_api import chronological_order
import json


class ApiData():
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.json_data = None
        self.headers = None

    def _parse_data(self):
        """[Parses raw data into a dictionary]
        """
        if isinstance(self.raw_data, dict):
            print("Data is already a dictionary")
            self.json_data = self.raw_data
        # Here we can add extra types check. Useful for decoding web data.
        # EX:
        # if isinstance(self.raw_data, str):
        #     str.decode(self.raw_data, 'utf-8')  # we can also try different decoders
        else:
            try:
                self.json_data = json.dumps(self.raw_data)
                print("Parsed data as dictionary")
            # Here we can add extra parsing if needed.
            except:
                print("Could not parse data into dictionary")
                return 1

    def _extract_headers(self):
        """[]
        """
        headers = set()
        for item in self.json_data.keys():
            for k in self.json_data[item][0].keys():
                headers.add(k)
        self.headers = headers

    def _convert_to_ordered_dict(self, key="publicationDate", reversed=True):
        """[Convert dictionary to OrderedDict by key. Defaults to publicationDate]

        :param key: [Field name that containes a date in format: May 2, 2020 6:07:03 AM], defaults to "publicationDate"
        :type key: str
        :param reversed: [Set to True to use reverse chronological order
        :type reversed: boolean
        """
        ordered1 = []
        # This orders by Date
        try:
            # iterate each key (sports)
            for i in self.json_data:
                # iterate item within the list (games)
                #current_sport = i
                ordered_games = OrderedDict()
                for j in self.json_data[i]:
                    # Assert that we're a dictionary
                    assert(isinstance(j, dict))
                    # Find dateField in dictionary
                    if key in j:
                        j[key] = self._parse_date(j[key])
                    # Parse the date before sorting
                    temp1, temp2 = None
                    try:
                        temp1 = OrderedDict(
                            sorted(self.json_data[i].items(), key=lambda t: t[0]))
                    except Exception as e:
                        print("temp1")
                        print(e)
                    try:
                        temp2 = OrderedDict(
                            sorted(j.items(), key=lambda t: t[0]))
                    except Exception as e:
                        print("temp2")
                        print(e)
                    # Append to ordered_games
                    ordered_games.append[temp1, temp2]
                    print(ordered_games)
                # Update ordered1
                ordered1.append(ordered_games)
        except Exception as e:
            print(e)

        # This orders by Sport:
        ordered2 = OrderedDict(
            sorted(self.json_data.items(), key=lambda t: t[0]))
        print("Ordered1:")
        print(ordered1)
        print("Ordered2")
        print(ordered2)
        return 1

    def order_by_key(self, key, reverse=True):
        self._parse_data()
        self._extract_headers()

    def main(self):
        self._parse_data()
        self._convert_to_ordered_dict()


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_chronological_order(self):
        response_data = {"f1Results": [{"publicationDate": "May 9, 2020 8:09:03 PM", "seconds": 5.856, "tournament": "Silverstone Grand Prix", "winner": "Lewis Hamilton"}, {"publicationDate": "Apr 14, 2020 8:09:03 PM", "seconds": 7.729, "tournament": "VTB RUSSIAN GRAND PRIX", "winner": "Valtteri Bottas"}, {"publicationDate": "Mar 15, 2020 8:09:03 PM", "seconds": 5.856, "tournament": "Spa BELGIAN GRAND PRIX", "winner": "Lewis Hamilton"}], "nbaResults": [{"gameNumber": 6, "looser": "Heat", "mvp": "Lebron James", "publicationDate": "May 9, 2020 9:15:15 AM", "tournament": "NBA playoffs", "winner": "Lakers"}, {"gameNumber": 5, "looser": "Lakers", "mvp": "Jimmy Butler", "publicationDate": "May 7, 2020 3:15:00 PM", "tournament": "NBA playoffs", "winner": "Heat"}, {"gameNumber": 4, "looser": "Heat", "mvp": "Anthony Davis", "publicationDate": "May 5, 2020 1:34:15 PM",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                "tournament": "NBA playoffs", "winner": "Lakers"}, {"gameNumber": 3, "looser": "Lakers", "mvp": "Jimmy Butler", "publicationDate": "May 3, 2020 9:15:33 PM", "tournament": "NBA playoffs", "winner": "Heat"}, {"gameNumber": 2, "looser": "Heat", "mvp": "Anthony Davis", "publicationDate": "May 2, 2020 6:07:03 AM", "tournament": "NBA playoffs", "winner": "Lakers"}], "Tennis": [{"looser": "Schwartzman ", "numberOfSets": 3, "publicationDate": "May 9, 2020 11:15:15 PM", "tournament": "Roland Garros", "winner": "Rafael Nadal"}, {"looser": "Stefanos Tsitsipas ", "numberOfSets": 3, "publicationDate": "May 9, 2020 2:00:40 PM", "tournament": "Roland Garros", "winner": "Novak Djokovic"}, {"looser": "Petra Kvitova", "numberOfSets": 3, "publicationDate": "May 8, 2020 4:33:17 PM", "tournament": "Roland Garros", "winner": "Sofia Kenin"}]}
        data = ApiData(response_data)
        # clean_data.order_by_key("temp")
        data.main()
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
