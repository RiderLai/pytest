# -*- coding: utf-8 -*-
"""Hpfeeds 协议栈 AsyncIO 基础实现
"""
from json import dumps
from struct import pack
from hashlib import sha1
from logging import getLogger
from asyncio import Protocol, Transport

from hpfeeds_test.hpfeeds.base import OperationCode, FeedPacker, FeedUnpacker, BadClientException


class HpFeeds(Protocol):
    """hpfeeds 协议核心基类

    此类封装了 hpfeeds 协议绝大部分的基本操作和事件。

    使用前请注意查看每个函数的注释，写有“请不要覆盖此函数！”的函数为提供基础功能的函数，如非特殊情况请不要覆盖。

    整个连接过程从连接到断开将依次触发下列事件函数：
        client_connected => (各种类型消息事件) => connection_closed => client_disconnected

    在收到合法且完整的消息后，本基类会在简单处理数据后触发各种类型消息事件：
        on_error                “错误” 消息事件
        on_info                 “信息” 消息事件
        on_auth                 “认证” 消息事件
        on_publish              “发布” 消息事件
        on_subscribe            “订阅” 消息事件
        on_unsubscribe          “取消订阅” 消息事件
    """

    def __init__(self):
        """构造器
        """
        self._remote = None
        self._transport = None
        self._logger = getLogger()

        self._packer = FeedPacker()
        self._unpacker = FeedUnpacker()

        self._handlers = {
            OperationCode.ERROR.value: self._on_error,
            OperationCode.INFO.value: self._on_info,
            OperationCode.AUTH.value: self._on_auth,
            OperationCode.PUBLISH.value: self._on_publish,
            OperationCode.SUBSCRIBE.value: self._on_subscribe,
            OperationCode.UNSUBSCRIBE.value: self._on_unsubscribe
        }

    def connection_made(self, transport: Transport) -> None:
        """新连接建立事件

        请不要覆盖此函数！

        此函数将在新连接建立时处理一些必要的事务。
        当必要的事务处理完成后，此方法将调用client_connected(self, transport)方法
        """
        self._transport = transport
        remote = self._transport.get_extra_info(r"peername")
        if isinstance(remote, tuple):
            self._remote = r":".join(
                str(item)
                for item in remote
            )
        else:
            self._remote = remote

        self.client_connected(transport)

    def client_connected(self, transport: Transport) -> None:
        """新客户端已连接事件函数

        此方法为空的虚函数，将在connection_made()函数进行必要的数据处理后被调用。

        如果需要对新连接的客户端进行操作，请重写此方法。
        """
        pass

    def connection_lost(self, exc: Exception) -> None:
        """丢失连接事件

        请不要覆盖此函数！

        此函数将在连接丢失时处理一些必要的事务。

        注：此方法一定会调用close()方法关闭连接并清理接收缓冲区。

        当必要的事务处理完成后，此方法将调用client_disconnected(self, exc)方法
        """
        self.close()
        self._logger.info(r"client: {} connection lost. exc:{}.".format(
            self._remote, exc
        ))

        self.client_disconnected(exc)

    def client_disconnected(self, exc: Exception) -> None:
        """当前客户端已丢失事件函数

        此方法为空的虚函数，将在connection_lost()函数进行必要的数据处理后被调用。

        注：此方法调用前本基类已调用close()方法关闭连接并清理接收缓冲区。

        如果需要对此事件进行一定的响应，请重写此方法。
        """
        pass

    def data_received(self, received_data: bytes) -> None:
        """接收到数据事件

        请不要覆盖此函数！

        此函数将在接收到数据时自动将数据放入缓冲区，并尝试对缓冲区内的数据进行解包；

        如果缓冲区内的数据可以被解包，则将其数据放入事件处理器进行进一步的处理。
        """
        self._unpacker.extend(received_data)

        try:
            for operation_code, data in self._unpacker:
                self.message_handler(operation_code, data)
        except BadClientException:
            self._logger.warning(r"Disconnecting bad client: {}".format(self._remote))
            self.close()
        except Exception as ex:
            self._logger.error(r"Unknown exception catched. program maybe have bug: %s", ex, exc_info=ex)
            self.close()

    def message_handler(self, operation_code, data):
        """消息处理器

        请不要覆盖此函数！

        此函数负责将收到的消息投入对应的事件初处理器中；

        对应的事件初处理器将会进行初步的数据分离与格式化后触发对应的事件函数。
        """
        handler = self._handlers.get(operation_code.value)

        if handler:
            handler(data)
        else:
            self._logger.warning(r"Operation %s has no corresponding handler.", operation_code)

    def _on_error(self, body: bytes) -> None:
        """``错误`` 消息处事件初处理器

        * 请不要覆盖此函数！

        此函数将对 ``错误`` 消息进行初步的处理，提取出消息中的 msg 字段，

        完成后将交由 ``on_error(self, msg)`` 进行进一步的处理。
        """
        view = memoryview(body)

        msg = view.tobytes().decode(r"utf-8")

        return self.on_error(msg)

    def on_error(self, msg: str) -> None:
        """``错误`` 消息事件

        此方法为空的虚函数，将在事件初处理器函数进行必要的数据处理后被调用。
        """
        pass

    def _on_info(self, body: bytes) -> None:
        """``信息`` 消息处事件初处理器

        * 请不要覆盖此函数！

        此函数将对 ``信息`` 消息进行初步的处理，提取出消息中的 name 和 rand 字段，

        完成后将交由 ``on_info(self, name, rand)`` 进行进一步的处理。
        """
        view = memoryview(body)

        length = view[0] + 1
        name = view[1:length].tobytes().decode(r"utf-8")
        rand = int.from_bytes(view[length:].tobytes(), byteorder=r"little")

        return self.on_info(name, rand)

    def on_info(self, name: str, rand: int) -> None:
        """``信息`` 消息事件

        此方法为空的虚函数，将在事件初处理器函数进行必要的数据处理后被调用。
        """
        pass

    def _on_auth(self, body: bytes) -> None:
        """``认证`` 消息处事件初处理器

        * 请不要覆盖此函数！

        此函数将对 ``认证`` 消息进行初步的处理，提取出消息中的 ident 和 pwd_hash 字段，

        完成后将交由 ``on_auth(self, ident, pwd_hash)`` 进行进一步的处理。
        """
        view = memoryview(body)

        length = view[0] + 1
        ident = view[1:length].tobytes().decode(r"utf-8")
        pwd_hash = view[length:].tobytes()

        return self.on_auth(ident, pwd_hash)

    def on_auth(self, ident: str, pwd_hash: bytes) -> None:
        """``认证`` 消息事件

        此方法为空的虚函数，将在事件初处理器函数进行必要的数据处理后被调用。
        """
        pass

    def _on_publish(self, body: bytes) -> None:
        """``发布`` 消息处事件初处理器

        * 请不要覆盖此函数！

        此函数将对 ``发布`` 消息进行初步的处理，提取出消息中的 ident、 channel 和 payload 字段，

        完成后将交由 ``on_publish(self, ident, channel, payload)`` 进行进一步的处理。
        """
        view = memoryview(body)

        length = view[0] + 1
        ident = view[1:length].tobytes().decode(r"utf-8")

        offset = length
        length += view[offset] + 1
        channel = view[offset + 1: length].tobytes().decode(r"utf-8")
        payload = view[length:].tobytes()

        return self.on_publish(ident, channel, payload)

    def on_publish(self, ident: str, channel: str, payload: bytes) -> None:
        """``发布`` 消息事件

        此方法为空的虚函数，将在事件初处理器函数进行必要的数据处理后被调用。
        """
        pass

    def _on_subscribe(self, body: bytes) -> None:
        """``订阅`` 消息处事件初处理器

        * 请不要覆盖此函数！

        此函数将对 ``订阅`` 消息进行初步的处理，提取出消息中的 ident 和 channel 字段，

        完成后将交由 ``on_subscribe(self, ident, channel)`` 进行进一步的处理。
        """
        view = memoryview(body)

        length = view[0] + 1
        ident = view[1:length].tobytes().decode(r"utf-8")
        channel = view[length:].tobytes().decode(r"utf-8")

        return self.on_subscribe(ident, channel)

    def on_subscribe(self, ident: str, channel: str) -> None:
        """``订阅`` 消息事件

        此方法为空的虚函数，将在事件初处理器函数进行必要的数据处理后被调用。
        """
        pass

    def _on_unsubscribe(self, body: bytes) -> None:
        """``取消订阅`` 消息处事件初处理器

        请不要覆盖此函数！

        此函数将对 ``取消订阅`` 消息进行初步的处理，提取出消息中的 ident 和 channel 字段，

        完成后将交由 ``on_unsubscribe(self, ident, channel)`` 进行进一步的处理。
        """
        view = memoryview(body)

        length = view[0] + 1
        ident = view[1:length].tobytes().decode(r"utf-8")
        channel = view[length:].tobytes().decode(r"utf-8")

        return self.on_unsubscribe(ident, channel)

    def on_unsubscribe(self, ident: str, channel: str) -> None:
        """``取消订阅`` 消息事件

        此方法为空的虚函数，将在事件初处理器函数进行必要的数据处理后被调用。
        """
        pass

    def write_hpfeeds(self, operation_code: OperationCode, data: object) -> None:
        """发送 HpFeeds 协议格式消息
        """
        data = self._packer.pack(operation_code, data)
        self._transport.write(data)

    def send_error(self, msg: str) -> None:
        """发送 ``错误`` 消息
        """
        self.write_hpfeeds(OperationCode.ERROR, msg)

    def send_info(self, name: str, rand: int) -> None:
        """发送 ``信息`` 消息
        """
        name = name.encode(r"utf-8")
        rand = rand.to_bytes(4, byteorder=r"little")
        data = pack(r"!B", len(name)) + name + rand

        self.write_hpfeeds(OperationCode.INFO, data)

    def send_auth(self, ident: str, rand: int, pwd: str) -> None:
        """发送 ``认证`` 消息

        注：密码需为明文，函数将在内部进行哈希并发送消息。
        """
        pwd = pwd.encode(r"utf-8")
        ident = ident.encode(r"utf-8")
        rand = rand.to_bytes(4, byteorder=r"little")

        pwd_hash = sha1(rand + pwd).digest()
        data = pack(r"!B", len(ident)) + ident + pwd_hash

        self.write_hpfeeds(OperationCode.AUTH, data)

    def send_publish(self, ident: str, channel: str, msg: object) -> None:
        """发送 ``发布`` 消息
        """
        ident = ident.encode(r"utf-8")
        channel = channel.encode(r"utf-8")
        if isinstance(msg, str):
            msg = msg.encode(r"utf-8")
        elif not isinstance(msg, bytes):
            msg = dumps(msg)

        data = pack(r"!B", len(ident)) + ident
        data += pack(r"!B", len(channel)) + channel
        data += msg

        self.write_hpfeeds(OperationCode.PUBLISH, data)

    def send_subscribe(self, ident: str, channel: str) -> None:
        """发送 ``订阅`` 消息
        """
        ident = ident.encode(r"utf-8")
        channel = channel.encode(r"utf-8")

        data = pack(r"!B", len(ident)) + ident + channel

        self.write_hpfeeds(OperationCode.SUBSCRIBE, data)

    def send_unsubscribe(self, ident: str, channel: str) -> None:
        """发送 ``取消订阅`` 消息
        """
        ident = ident.encode(r"utf-8")
        channel = channel.encode(r"utf-8")

        data = pack(r"!B", len(ident)) + ident + channel

        self.write_hpfeeds(OperationCode.UNSUBSCRIBE, data)

    def close(self):
        """关闭当前连接并释放缓冲区

        请不要覆盖此函数！

        此函数负责关闭当前连接并释放缓冲区中的所有数据；

        对应的事件初处理器将会进行初步的数据分离与格式化后触发对应的事件函数。

        当必要的事务处理完成后，此方法将调用 ``connection_closed(self)``方法
        """
        self._unpacker.clear()
        self._transport.close()

        self.connection_closed()

    def connection_closed(self):
        """当前连接已关闭事件

        此方法为空的虚函数，将在close()函数完成关闭连接和缓冲区释放完成后被调用。

        如果需要对此事件进行一定的响应，请重写此方法。

        注：此方法将在 client_disconnected() 函数前先被调用。
        """
        pass
