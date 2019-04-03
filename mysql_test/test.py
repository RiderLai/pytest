import json
import asyncio
import aiomysql
# import redis
import aioredis


async def test():
    connetcion = await aiomysql.connect(host='192.168.10.3', port=3306, user='root',
                                        password='dbapp@2017', db='honey',
                                        loop=asyncio.get_event_loop())
    cur = await connetcion.cursor()
    await cur.execute('SELECT type, value FROM whitelist')
    # print(cur.description)

    r = await cur.fetchall()
    result = {
        r[0][0]: json.loads(r[0][1]),
        r[1][0]: json.loads(r[1][1])
    }
    print(result)

    _redis = await aioredis.create_connection('redis://localhost', loop=asyncio.get_event_loop())
    while True:
        if await _redis.execute('scard', 'ips') is not len(result['ips']):
            await _redis.execute('del', 'ips')
            for ip in result['ips']:
                await _redis.execute('sadd', 'ips', ip)

        if await _redis.execute('scard', 'files') is not len(result['files']):
            await _redis.execute('del', 'files')
            for file in result['files']:
                await _redis.execute('sadd', 'files', file)

        if await _redis.execute('sismember', 'ips', '169.254.28.91'):
            print('aaa')

        await asyncio.sleep(3)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(test())