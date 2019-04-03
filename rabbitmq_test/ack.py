import aio_pika
from asyncio import get_event_loop


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process(requeue=True):
        print(message.body)
        # raise Exception('test')


async def main():
    connection = await aio_pika.connect_robust(url='amqp://guest:guest@127.0.0.1:5672/',
                                               loop=get_event_loop())
    channel = await connection.channel()
    queue1 = await channel.declare_queue('test', durable=True)
    queue2 = await channel.declare_queue('test2', durable=True)
    # await queue.consume(process_message, timeout=5)
    message1 = await queue1.get()
    await process_message(message=message1)

    message2 = await queue2.get()
    await process_message(message=message2)

if __name__ == '__main__':
    get_event_loop().run_until_complete(main())