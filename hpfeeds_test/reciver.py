import redis
import asyncio
from hpfeeds.asyncio import ClientSession


async def hpfeeds_listening():
    r = redis.Redis()
    async with ClientSession(host='localhost', port='10000', ident='test', secret='test') as client:
        client.subscribe('test')
        i = 0
        async for ident, channel, pyload in client:
            r.rpush('hpfeeds', pyload)
            i += 1
            print(i)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(hpfeeds_listening())