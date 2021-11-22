# module that filters an api call
import argparse
import json


class FilterData():

    def __init__(self, raw_data):
        """[Filters ApiData and raw_data]

        :param raw_data: [ApiData from an api call]
        :type raw_data: [str]
        """
        self.raw_data = raw_data
        self.json_data = None
        self._parse_data()

    def _parse_data(self):
        """[Parses raw data into a dictionary]"""
        if isinstance(self.raw_data, dict):
            print("Data is already a dictionary")
            self.json_data = self.raw_data
            # Here we can add extra types check. Useful for decoding web data.
            # EX:
            # if isinstance(self.raw_data, str):
            #     str.decode(self.raw_data, 'utf-8')  # we can also try different decoders
        else:
            try:
                self.json_data = json.loads(self.raw_data)
                print("Parsed data as dictionary")
                # Here we can add extra parsing if needed.
            except:
                print("Could not parse data into dictionary")
                return 1
        assert(isinstance(self.json_data, dict))

    def _filter_generator(self, filter_string):
        """[Filter generator function]

        :param filter_string: [key to search for]
        :type filter_string: [str]
        :yield: [key, value]
        :rtype: [tuple]
        """
        for key, val in self.json_data.items():
            if filter_string not in key:
                continue
            yield key, val

    def _filter(self, filter_string):
        """[Filter function that returns a dictionary]

        :param filter_string: [key to search for]
        :type filter_string: [srt]
        :return: [dictionary with matches]
        :rtype: [dict]
        """
        filtered_dict = {
            k: v for (k, v) in self.json_data.items() if filter_string in k}
        return filtered_dict

    def filterBy(self, keys):
        """[Filter by one or more keys. Return matches as k,v]

        :param keys: [Keys to filter in the dictionary: Eg: f1Results]
        :type keys: [list]
        """
        self._parse_data()  # Data might be unparsed
        num_matches = 0  # Debugging or extra information
        filtered_results = []
        for k in keys:
            for key, val in self._filter_generator(k):
                # do something
                print("Found {}".format(key))
                filtered_results.append((key, val))
                num_matches += 1
        print("Found %d total matches" % num_matches)
        return filtered_results


def main():

    # Argparse to be called by command-line
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-d", "--data", type=str, help="data")
    parser.add_argument("-f", "--filter", type=str, help="filter")
    args = parser.parse_args()

    my_data, my_filter = None
    if args.data:
        print("parsing data...")
        my_data = args.data
    if args.filter:
        print("filtering...")
        my_filter = args.filter
        my_filter.replace(" ", ",").split(",")

    # Parse and Filter
    filter_data = FilterData(my_data)
    return filter_data.filterBy(my_filter)
