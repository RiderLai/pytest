import os
import ssl
import sys
import socket
import asyncio

from tornado.process import fork_processes
from hpfeeds_test.hpfeeds.asyncio import HpFeeds
# from hpfeeds.asyncio.client import ClientSession
# from hpfeeds.asyncio.protocol import ClientProtocol


# class _Protocol(ClientProtocol):
#
#     def __init__(self, ident, secret):
#         super().__init__(ident, secret)
#
#     def connection_made(self, transport):
#         sock = transport.get_extra_info('socket')
#         sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
#         if sys.platform.startswith('linux'):
#             sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 10)
#             sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 5)
#             sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 3)
#         super().connection_made(transport)
#
#     def connection_ready(self):
#         # self.subscribe(self.ident, 'test')
#         print(1)
#
#     def connection_lost(self, exc):
#         super().connection_lost(exc)
#
#     def on_publish(self, ident, chan, data):
#         print(data.decode(), os.getpid())
#
#
# async def hpfeeds_listening():
#     async with ClientSession(host='localhost', port='10000', ident='test', secret='test') as client:
#         client.subscribe('test')
#
#         async for ident, channel, pyload in client:
#             print(pyload.decode(), os.getpid())


class HpfeedsClient(HpFeeds):
    """hpfeeds 协议客户端
    """

    def __init__(self, ident, secret, channels):
        """构造器
        """
        super().__init__()

        self._ident = ident
        self._secret = secret
        self._channels = channels

    def client_connected(self, transport) -> None:
        """新客户端已连接事件函数

        此方法为空的虚函数，将在connection_made()函数进行必要的数据处理后被调用。

        如果需要对新连接的客户端进行操作，请重写此方法。
        """
        self._logger.info(f"connected to: {self._remote}.")

    def client_disconnected(self, exc: Exception) -> None:
        """当前客户端已丢失事件函数

        此方法为空的虚函数，将在connection_lost()函数进行必要的数据处理后被调用。

        注：此方法调用前本基类已调用close()方法关闭连接并清理接收缓冲区。

        如果需要对此事件进行一定的响应，请重写此方法。
        """
        self._logger.info(f"connection lost. exc:{exc}.")

        # sys.exit(0)

    def on_error(self, msg: str) -> None:
        """``错误`` 消息事件

        此方法为空的虚函数，将在事件初处理器函数进行必要的数据处理后被调用。
        """
        self._logger.error('Error message from broker: {0}.'.format(msg))

        self.close()

    def on_info(self, name: str, rand: int) -> None:
        """``信息`` 消息事件

        此方法为空的虚函数，将在事件初处理器函数进行必要的数据处理后被调用。
        """
        self._logger.info(f"info message from: {name}, rand: {hex(rand)}")

        self.send_auth(self._ident, rand, self._secret)

        # 注册频道
        for channel in self._channels:
            self.send_subscribe(self._ident, channel)

    def on_publish(self, ident: str, channel: str, payload: bytes) -> None:
        """``发布`` 消息事件

        此方法为空的虚函数，将在事件初处理器函数进行必要的数据处理后被调用。
        """
        payload = payload.decode(r"utf-8")

        self._logger.info(f"publish to {channel} by {ident}: {payload}")
        print(os.getpid())
        print(f"publish to {channel} by {ident}: {payload}")

    #     # ensure_future(self.data_to_normalize(ident, channel, payload))
    #
    # async def data_to_normalize(self, ident, chan, data):
    #     """
    #     处理hpfeeds接受到的数据
    #     :param ident:
    #     :param chan:
    #     :param data:
    #     :return:
    #     """
    #     await normalize_save('hpfeeds',
    #                          submission_stamp=int(time.time()),
    #                          payload=data,
    #                          channel=chan,
    #                          ident=ident)


def hpfeeds_listening2(sock, pid, ssl):
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: HpfeedsClient('mnemosyne', 'ff2dbee287584c4d931a04b5165e9c71',
                                                        ['wordpot.events']), sock=sock, ssl=ssl,
                                  server_hostname='192.168.10.3')
    print(id(coro))
    print(pid)
    loop.run_until_complete(coro)
    # loop.run_forever()


if __name__ == '__main__':
    sock = socket.socket()
    sock.connect(('192.168.10.3', 10001))

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ssl_context.load_verify_locations('cert.pem')
    # os.fork()
    pid = fork_processes(3)
    # pid = 1
    hpfeeds_listening2(sock, pid, ssl_context)
    asyncio.get_event_loop().run_forever()

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