# -*- coding: utf-8 -*-
"""HPFeeds 协议基础模块

此模块中封装了与 HPFeeds 协议相关的模块与类
"""
from json import dumps
from enum import Enum, unique
from struct import pack, unpack


@unique
class OperationCode(Enum):
    """HPFeeds协议头部操作代码枚举
    """
    ERROR = 0x00
    INFO = 0x01
    AUTH = 0x02
    PUBLISH = 0x03
    SUBSCRIBE = 0x04
    UNSUBSCRIBE = 0x05


MAX_BUFF = 10 * (1024**2)
SIZES = {
    OperationCode.ERROR: 5 + MAX_BUFF,
    OperationCode.INFO: 5 + 256 + 20,
    OperationCode.AUTH: 5 + 256 + 20,
    OperationCode.PUBLISH: 5 + MAX_BUFF,
    OperationCode.SUBSCRIBE: 5 + 256 * 2,
    OperationCode.UNSUBSCRIBE: 5 + 256 * 2
}


class ArgumentException(Exception):
    """参数无效异常

    当向方法提供的参数之一无效时引发的异常
    """

    @property
    def name(self) -> str:
        """无效参数的名称
        """
        return self._name

    @property
    def value(self) -> object:
        """无效参数的值
        """
        return self._value

    def __init__(self, name: str=None, value: object=None):
        """构造器
        """
        super().__init__()

        self._name = name
        self._value = value


class BadClientException(Exception):
    """客户端异常

    由客户端不正确消息或响应引发的异常。
    """
    pass


class FeedPacker(object):
    """HpFeeds协议数据包编码器
    """

    def pack(self, operation_code: OperationCode, data: object) -> bytes:
        """将消息打包
        """
        if operation_code not in OperationCode:
            raise ArgumentException(r"operation_code", data)
        if not isinstance(data, (str, bytes)):
            data = dumps(data)
        if isinstance(data, str):
            data = data.encode(r"utf-8")

        return pack(r"!iB", 5 + len(data), operation_code.value) + data


class FeedUnpacker(object):
    """HpFeeds协议数据包解析器
    """

    def __init__(self):
        """构造器
        """
        self._buffer = bytearray()

    def __iter__(self):
        """返回一个迭代器对象
        """
        return self

    def __next__(self):
        """返回迭代器下一个项
        """
        return self.unpack()

    def clear(self):
        """清空内部缓冲区
        """
        self._buffer.clear()

    def extend(self, data: bytes) -> None:
        """向内部缓冲区追加数据
        """
        self._buffer.extend(data)

    def unpack(self) -> (OperationCode, bytes):
        """尝试对缓冲区的数据进行解包
        """
        buffer_length = len(self._buffer)
        if buffer_length < 5:
            raise StopIteration(r"No Message.")

        # 提取出 HpFeed 消息头
        header = bytes(self._buffer[:5])
        length, operation_code = unpack(r"!iB", header)
        if length > SIZES.get(operation_code, MAX_BUFF):
            raise BadClientException(r"Not respecting MAXBUF.", header)

        if buffer_length < length:
            raise StopIteration(r"No Message.")

        # 提取出 HpFeed 消息正文
        data = bytes(self._buffer[5:length])
        del self._buffer[:length]

        try:
            operation_code = OperationCode(operation_code)
        except ValueError:
            raise BadClientException(r"Unknown Operation Code.", header + data)

        return operation_code, data
