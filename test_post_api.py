import unittest
from post_api import chronological_order
import json

class ApiData():
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.json_data = None
        self.headers = None

    def _parse_data(self):
        """[Parses raw data into a list of lists with values]
        """
        if isinstance(self.raw_data, str):
            try:
                print("Creating dictionary")
                self.json_data = json.dumps(self.raw_data)
            except:
                print("Could not parse data into dictionary")
                return 0
        elif isinstance(self.raw_data, dict):
            print("Data is already a dictionary")
            self.json_data = self.raw_data
        else:
            print("Data is not a dictionary")
            return 0

    def _extract_headers(self):
        """[]
        """
        headers = set()
        for item in self.json_data.keys():
            for k in self.json_data[item][0].keys():
                headers.add(k)
        self.headers = headers

    def order_by_key(self, key, reverse=True):
        self._parse_data()
        self._extract_headers()
        pass

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
        data = {"f1Results":[{"publicationDate":"May 9, 2020 8:09:03 PM","seconds":5.856,"tournament":"Silverstone Grand Prix","winner":"Lewis Hamilton"},{"publicationDate":"Apr 14, 2020 8:09:03 PM","seconds":7.729,"tournament":"VTB RUSSIAN GRAND PRIX","winner":"Valtteri Bottas"},{"publicationDate":"Mar 15, 2020 8:09:03 PM","seconds":5.856,"tournament":"Spa BELGIAN GRAND PRIX","winner":"Lewis Hamilton"}],"nbaResults":[{"gameNumber":6,"looser":"Heat","mvp":"Lebron James","publicationDate":"May 9, 2020 9:15:15 AM","tournament":"NBA playoffs","winner":"Lakers"},{"gameNumber":5,"looser":"Lakers","mvp":"Jimmy Butler","publicationDate":"May 7, 2020 3:15:00 PM","tournament":"NBA playoffs","winner":"Heat"},{"gameNumber":4,"looser":"Heat","mvp":"Anthony Davis","publicationDate":"May 5, 2020 1:34:15 PM","tournament":"NBA playoffs","winner":"Lakers"},{"gameNumber":3,"looser":"Lakers","mvp":"Jimmy Butler","publicationDate":"May 3, 2020 9:15:33 PM","tournament":"NBA playoffs","winner":"Heat"},{"gameNumber":2,"looser":"Heat","mvp":"Anthony Davis","publicationDate":"May 2, 2020 6:07:03 AM","tournament":"NBA playoffs","winner":"Lakers"}],"Tennis":[{"looser":"Schwartzman ","numberOfSets":3,"publicationDate":"May 9, 2020 11:15:15 PM","tournament":"Roland Garros","winner":"Rafael Nadal"},{"looser":"Stefanos Tsitsipas ","numberOfSets":3,"publicationDate":"May 9, 2020 2:00:40 PM","tournament":"Roland Garros","winner":"Novak Djokovic"},{"looser":"Petra Kvitova","numberOfSets":3,"publicationDate":"May 8, 2020 4:33:17 PM","tournament":"Roland Garros","winner":"Sofia Kenin"}]}
        clean_data = ApiData(data)
        clean_data.order_by_key("temp")
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()