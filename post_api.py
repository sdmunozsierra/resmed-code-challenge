# Simple post api using aiohttp and asyncio
import aiohttp
import asyncio
import json

async def post_call():
    url = "https://ancient-wood-1161.getsandbox.com:443/results"
    async with aiohttp.ClientSession() as session:
        post_tasks = []
        # prepare the coroutines that post
        # async for x in make_numbers(35691, 5000000):
        #     post_tasks.append(do_post(session, url, x))
        # run one corutine 
        post_tasks.append(do_simple_post(session, url))
        # now execute them all at once
        await asyncio.gather(*post_tasks)

async def do_simple_post(session, url, arg=None):
    async with session.post(url, json={}) as response:
        data = await response.text()
        print(data)
        #print(type(data))  # String
        chronological_order(data, "publishedDate")


def chronological_order(data, key, reverse=True):
    '''
    @param data: Data to be ordered
    @param key: Key on which to perform the order operation
    @param reverse: Set to true to enable reverse chronological order
    '''
    print("Ordering data by key {} in reverse order = {}".format(key, reverse))
    print(type(data))
    # For this specific api the key is publicationDate

    def extract_time(data, key):
        for sport in data:
            try:
                # Also convert to int since update_time will be string.  When comparing
                # strings, "10" is smaller than "2".
                return int(json[sport][key])
            except KeyError:
                return 0
    # sort by extract time
    data = json.loads(data)
    print("here")
    print(type(data))
    return data.sort(key=extract_time, reverse=reverse)

async def do_post(session, url, x):
    async with session.post(url, data ={
                "terms": 1,
                "captcha": 1,
                "email": "user%s@hotmail.com" % str(x),
                "full_name": "user%s" % str(x),
                "password": "123456",
                "username": "auser%s" % str(x)
          }) as response:
          data = await response.text()
          print("-> Created account number %d" % x)
          print (data)


if __name__ == "__main__":
    print ("Hello world!")
    # loop = asyncio.get_event_loop()
    # asyncio.ensure_future(post_call())
    # loop.run_forever()
    # loop.close()
    asyncio.run(post_call())