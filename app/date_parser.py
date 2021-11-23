import datetime

# LOCAL_TIMEZONE = datetime.datetime.now(datetime.timedelta(0))).settimezone().datetime.tzinfo


class DateParser:

    def __init__(self, str_date=None):
        self.str_date = str_date

    def _parse_date(self, str_date=None):
        """[Parse string to a OrderDict List]

        :param str_date: Date in String format "May 9, 2020 8:09:03 PM"
        :type str_date: [str]
        :return: [A Date object]
        :rtype: [MyDate]
        """
        converted = None
        if str_date:
            self.str_date = str_date
        try:
            converted = self.str_date.replace(",", "")
            converted = datetime.datetime.strptime(
                converted, "%B %d %Y %I:%M:%S %p")
        except Exception as e:
            print("Error converting date")
            print(e)
        print("Converted date: ", converted)
        return converted

    def _convert_to_24_hour(self, tm, ampm):
        """[Convert a time from 12 hours to 24 hours]

        :param tm: [time format: 8:09:03]
        :type tm: [str] enforce
        :param ampm: [AM or PM]
        :type ampm: [str]
        :returns: 
        """
        raw_input = tm + ampm  # hh:mm:ssAM/PM
        print(raw_input)
        t_splt = raw_input.split(':')
        conv = int(t_splt[0])
        print(type(conv))
        if t_splt[2][2:] == 'PM' and t_splt[0] != '12':
            t_splt[0] = str(12 + conv)
        elif conv == 12 and t_splt[2][2:] == 'AM':
            t_splt[0] = '00'
        t_splt[2] = t_splt[2][:2]
        return (':'.join(t_splt))

    def convert(self, str_date):
        return self._parse_date(str_date)


def main():
    # Argparse to be called by command-line
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-d", "--date", type=str, help="string date")
    parser.add_argument("-l", "--locale", type=str, help="filter")
    args = parser.parse_args()

    my_date, my_locale = None
    if args.date:
        # Format : str_date May 3, 2020 9:15:15 PM
        my_date = args.date
    if args.loocale:
        my_locale = args.locale

    if not my_date:
        print("Requires string date to be parsed")
        exit
    parser = DateParser(my_date)
    if my_locale:
        parser.set_locale(my_locale)
    return parser.convert()


if __name__ == "__main__":
    main()
