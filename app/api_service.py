# Simple post api using aiohttp and asyncio
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
            print("Mydata!: {}\nIs type: {}".format(data, type(data)))
            return data


# async def main():
#     default_url = "https://ancient-wood-1161.getsandbox.com:443/results"
#     # Argparse to be called by command-line
#     parser = argparse.ArgumentParser(add_help=True)
#     parser.add_argument("-x", "--post", type=str, help="post data")
#     parser.add_argument("-u", "--urls", type=str,
#                         default=default_url, help="target url")
#     args = parser.parse_args()

#     if args.post:
#         my_post = args.post
#     if args.urls:
#         my_url = args.urls

#     # Create service
#     service = await ApiService(my_url, my_post)
#     # run one corutine
#     response_data = await asyncio.run(service.post_call())
#     print(response_data)
#     return response_data


# if __name__ == "__main__":
#     asyncio.run(main)
