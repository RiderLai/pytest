from hpfeeds.asyncio import ClientSession


async def hpfeeds_push():
    async with ClientSession(host='localhost', port='10000', ident='test', secret='test') as client:
        # for i in range(1000000):
        #     client.publish('test', b'hellommmmmmm')
        client.publish('test', b'hellommmmmmm')

if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(hpfeeds_push())