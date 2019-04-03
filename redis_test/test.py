from redis import Redis
from time import sleep
import asyncio


async def redis_loop():
    r = Redis(host='localhost', port=6379)
    while True:
        msg = r.lpop('hpfeeds')
        if msg:
            print(msg)
        else:
            await asyncio.sleep(1)


if __name__ == '__main__':
    # redis_loop()
    asyncio.get_event_loop().run_until_complete(redis_loop())

    # r = Redis(host='192.168.34.91', port=6379)
    # r.sadd('ips', 'aaa')
    # print(r.scard('aaaaa'))
    # print(r.sismember('ips', '192.168.10.1'))
    # r.sadd('ips', 'aaa')