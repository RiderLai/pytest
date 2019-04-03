import os
import sys
import socket
import asyncio

from hpfeeds.asyncio.client import ClientSession
from hpfeeds.asyncio.protocol import ClientProtocol


class _Protocol(ClientProtocol):

    def __init__(self, ident, secret):
        super().__init__(ident, secret)

    def connection_made(self, transport):
        sock = transport.get_extra_info('socket')
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        if sys.platform.startswith('linux'):
            sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 10)
            sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 5)
            sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 3)
        super().connection_made(transport)

    def connection_ready(self):
        self.subscribe(self.ident, 'test')

    def connection_lost(self, exc):
        super().connection_lost(exc)

    def on_publish(self, ident, chan, data):
        print(data.decode(), os.getpid())


async def hpfeeds_listening():
    async with ClientSession(host='localhost', port='10000', ident='test', secret='test') as client:
        client.subscribe('test')

        async for ident, channel, pyload in client:
            print(pyload.decode(), os.getpid())


def hpfeeds_listening2(sock):
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: _Protocol('test', 'test'), sock=sock)
    loop.run_until_complete(coro)
    loop.run_forever()


if __name__ == '__main__':
    sock = socket.socket()
    sock.connect(('127.0.0.1', 10000))
    os.fork()
    hpfeeds_listening2(sock)

    # pid = os.fork()
    # if pid:
    #     asyncio.get_event_loop().run_until_complete(hpfeeds_listening())
    # else:
    #     print('This is child process', os.getpid())

    # os.fork()
    # asyncio.get_event_loop().run_until_complete(hpfeeds_listening())

    # from tornado.process import fork_processes, task_id
    # from time import sleep
    # print(os.getpid())
    # pid = fork_processes(3)
    #
    # print(task_id(), os.getpid())
    # sleep(10)