import time
import asyncio


async def test():
    while True:
        print('a')
        await asyncio.sleep(3)


def main(loop):
    asyncio.ensure_future(test(), loop=loop)
    time.sleep(3)
    print('b')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    main(loop)
    # loop.run_forever()
