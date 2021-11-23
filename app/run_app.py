import argparse
import asyncio
from api_service import ApiService
from filter_data import FilterData


async def main():
    # Argparse to be called by command-line
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-all", type=bool, default=True,
                        help="run all the components")
    args = parser.parse_args()

    if args.all:
        default_url = "https://ancient-wood-1161.getsandbox.com:443/results"
        default_filter = ["f1Results"]
        default_filter_multi = ["f1Results", "Tennis"]
        # Only pass one target url as list
        service = ApiService([default_url], [])
        responses = await service.post_call()
        for res in responses:
            print(res)
            filtered = FilterData(res)
            filtered._parse_data()
            filtered.convert_dates()
            filtered.order_by()
            result1 = filtered.filterBy(default_filter)
            result2 = filtered.filterBy(default_filter_multi)
            print("Result1: {}".format(result1))
            print("Result2: {}".format(result2))
        return


if __name__ == "__main__":
    asyncio.run(main())
