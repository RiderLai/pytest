import aio_pika
from asyncio import get_event_loop
from datetime import datetime


async def rabbitmq_publish(loop, key, message):
    connection = await aio_pika.connect_robust('amqp://test4:test4@127.0.0.1:5672/test3',
                                               # virtualhost='test2',
                                               loop=loop)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode(), timestamp=datetime.now().timestamp()),
            routing_key=key
        )


async def main():
    await rabbitmq_publish(loop=get_event_loop(),
                           key='test1',
                           message='test1_hello')
    await rabbitmq_publish(loop=get_event_loop(),
                           key='test2',
                           message='test2_hello')


if __name__ == '__main__':
    get_event_loop().run_until_complete(main())