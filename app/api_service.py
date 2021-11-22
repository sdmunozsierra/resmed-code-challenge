# Simple post api using aiohttp and asyncio
from re import A
import aiohttp
import asyncio
import argparse


class ApiService:
    def __init__(self, urls=[], post_data=None):
        self.urls = urls
        self.post_data = post_data

    async def post_call(self):
        """[Send a post request to a url]

                :param url: [target url to send a post request]
                :type url: [str]
                :param x: [json_data to post]
                :type x: [dict]
                """
        async with aiohttp.ClientSession() as session:
            post_tasks = []
            if not self.post_data:
                self.post_data = {}
                # prepare the coroutines that post
                for i in self.urls:
                    post_tasks.append(self._do_post(
                        session, i, self.post_data))
            else:
                # prepare the coroutines that post
                merged = zip(self.urls, self.post_data)
                for k, v in (merged):
                    post_tasks.append(self._do_post(session, k, v))
            # now execute them all at once
            return await asyncio.gather(*post_tasks)

    async def _do_post(self, session, url, arg={}):
        async with session.post(url, json=arg) as response:
            data = await response.text()
            return data


async def main():
    """[Usage: api_service -urls "url1, url2" -x "pdata1, pdata2"]

    :return: [Response data]
    :rtype: [dict]
    """
    default_url = "https://ancient-wood-1161.getsandbox.com:443/results"

    # Argparse to be called by command-line
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--urls", type=str,
                        default=default_url, help="Urls")
    parser.add_argument("-x", "--post", type=str, default="",
                        help="post data json format")
    args = parser.parse_args()
    my_urls, my_post = [], []
    if args.urls:
        my_urls = args.urls
        my_urls.split(",")
        if not isinstance(my_urls, list):
            my_urls = [my_urls]
    if args.post:
        my_post = args.post
        my_post.split(",")
        if not isinstance(my_post, list):
            my_post = [my_post]

    # Create service
    service = ApiService(my_urls, my_post)
    # run as one corutine
    response_data = await service.post_call()
    print(response_data)
    return response_data


if __name__ == "__main__":
    asyncio.run(main())
