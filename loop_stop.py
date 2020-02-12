from sys import exit
from asyncio import get_event_loop, sleep, ensure_future


async def coro():
    i = 1
    while True:
        print(1)
        i += 1
        await sleep(1)


if __name__ == '__main__':
    loop = get_event_loop()
    ensure_future(coro(), loop=loop)
    try:
        loop.run_forever()
    except:
        print(loop.is_running())
        loop.stop()
        print(loop.is_running())
        loop.close()
        print(loop.is_running())
    else:
        exit(0)
