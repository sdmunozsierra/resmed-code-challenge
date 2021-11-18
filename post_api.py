# Simple post api using aiohttp and asyncio
import aiohttp
import asyncio

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
          print (data)

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