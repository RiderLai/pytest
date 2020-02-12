from asyncio import get_event_loop, sleep

from aioredis import create_connection, Redis, create_pool


# async def redis_loop():
#     r = Redis(host='localhost', port=6379)
#     while True:
#         msg = r.lpop('hpfeeds')
#         if msg:
#             print(msg)
#         else:
#             await asyncio.sleep(1)


async def test():
    # conn = await create_connection()
    # redis = Redis(conn)
    # redis.lpop()
    # settings = {
    #     'address': 'redis://127.0.0.1:6379',
    #     'password': None,
    #     'minsize': 1,
    #     'maxsize': 10,
    #     'db': 0,
    # }

    # await create_pool(**settings)
    conn = await create_connection('redis://127.0.0.1:6379')
    r = Redis(conn)
    print(await r.hget('a', 'c'))


if __name__ == '__main__':
    # redis_loop()
    # asyncio.get_event_loop().run_until_complete(redis_loop())

    # r = Redis(host='192.168.34.91', port=6379)
    # r.sadd('ips', 'aaa')
    # print(r.scard('aaaaa'))
    # print(r.sismember('ips', '192.168.10.1'))
    # r.sadd('ips', 'aaa')
    loop = get_event_loop()
    loop.run_until_complete(test())