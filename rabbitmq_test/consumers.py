import aio_pika
import asyncio


async def queue_listening(queue) -> None:
    """
    单个队列的监听事件
    :param channel:队列名
    :return:
    """
    # async with queue.iterator() as queue_iter:
    #     async for message in queue_iter:
    #         async with message.process(requeue=True):
    #             print(message.body)

    async def on_message(message: aio_pika.IncomingMessage):
        print(message.body)
        await message.reject()

    await queue.consume(on_message)


async def main():
    connetion = await aio_pika.connect_robust(url='amqp://guest:guest@127.0.0.1:5672',
                                              # virtualhost='test',
                                              loop=asyncio.get_event_loop())
    channel = await connetion.channel()
    queue1 = await channel.declare_queue('test1', durable=True)
    queue2 = await channel.declare_queue('test2', durable=True)
    to_do = [queue_listening(queue1), queue_listening(queue2)]
    await asyncio.wait(to_do)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()