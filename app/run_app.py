import argparse
import asyncio
from api_service import ApiService
from filter_data import FilterData

# Change default settings for the app
DEFAULT_URLS = "https://ancient-wood-1161.getsandbox.com:443/results"


def parse_arguments():
    # Argparse to be called by command-line
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--all", type=bool, default=True,
                        help="Run all the functions.")
    parser.add_argument("-u", "--urls", type=str,
                        help="Target urls as a comma separated list")
    parser.add_argument("-x", "--post", type=str,
                        help="Send post request. Append extra json data")
    parser.add_argument("-o", "--order", type=str,
                        help="Order by key containing date. Set false to reverse order")
    parser.add_argument("-r", "--order-reverse", type=str,
                        help="Order by key containing date. Set false to reverse order")
    parser.add_argument("-f", "--filter", type=str,
                        help="Filter by keyword. Eg: f1Results")
    parser.add_argument("-d", "--data", type=str,
                        help="Override data.")
    parser.add_argument("-l", "--locale", type=str,
                        help="Set locale")
    return parser.parse_args()


async def main():
    args = parse_arguments()
    my_urls = my_post = my_order = my_ov = my_filter = my_locale = None

    # Parse params
    if args.urls:
        my_urls = args.urls.split(",")
        if not isinstance(my_urls, list):
            my_urls = [my_urls]
    if args.post:
        my_post = args.post
    if args.order:
        my_order = args.order
    if args.order_reverse:
        my_ov = args.order_reverse
    if args.filter:
        my_filter = args.filter.split(",")
    if args.locale:
        my_locale = args.locale

    # Default values
    if not my_urls:
        my_urls = [DEFAULT_URLS]
    if not my_post:
        my_post = []
    if my_order and my_ov:
        print("only one ordering is allowed")
        return 1

    # Parameter assertions
    assert(isinstance(my_urls, list))
    assert(isinstance(my_post, list))

    # Make async calls
    my_service = ApiService(my_urls, my_post)
    responses = await my_service.post_call()

    # Manupulate Response data
    for res in responses:
        DATA = FilterData(res)
        DATA._parse_data()
        DATA.convert_dates()

        # Order by publicationDate
        if my_order:
            DATA.order_by(my_order, reverse=False)
        if my_ov:
            DATA.order_by(my_ov, reverse=True)

        DATA.convert_dates_strings()

        if my_locale:
            # TODO update locale
            pass
        if my_filter:
            assert(isinstance(my_filter, list))
            result = DATA.filterBy(my_filter)
            print(result)
            break
        print(DATA)

if __name__ == "__main__":
    asyncio.run(main())
