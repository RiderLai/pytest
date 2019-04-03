import asyncio

CRLF = b'\r\n'

_writers = {}


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    global _writers
    index = len(_writers)
    client = writer.get_extra_info('peername')
    print('{} join the room'.format(client))
    writer.write('{} hello'.format(client).encode() + CRLF)
    await writer.drain()

    for _writer in _writers.values():
        _writer.write('{} join the room'.format(client).encode() + CRLF)
        await _writer.drain()

    _writers[index] = writer

    while True:
        # writer.write('{}: '.format(client).encode())
        # await writer.drain()

        data = await reader.readline()
        for key, val in _writers.items():
            if key is index:
                continue
            val.write('{}: '.format(client).encode() + data)
            await val.drain()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handler,
                                '127.0.0.1', '6767', loop=loop)
    server = loop.run_until_complete(coro)
    host = server.sockets[0].getsockname()
    print('Serving on {}. Hit CRTL-C to stop.'.format(host))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())