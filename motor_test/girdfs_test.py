from asyncio import get_event_loop
from bson.objectid import ObjectId

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket


async def put_file():
    db = AsyncIOMotorClient().test
    fs = AsyncIOMotorGridFSBucket(db, 'files')

    # file_id = await fs.upload_from_stream('testFile', b"i'm fine3")
    # print(file_id)

    # await fs.upload_from_stream_with_id(ObjectId(),
    #                                     "testFile",
    #                                     b"i'm fine2")

    with open('ipip.datx', 'rb') as fp:
        content = fp.read()
        await fs.upload_from_stream('ipip.datx', content, chunk_size_bytes=15*1024*1024)


async def get_file():
    db = AsyncIOMotorClient(host='10.20.129.102', port=27017).mnemosyne3
    fs = AsyncIOMotorGridFSBucket(db, 'ttylog')

    # out_stream = await fs.open_download_stream_by_name('testFile')
    out_stream = await fs.open_download_stream(ObjectId("5cc279bfe20a7c593fbce276"))
    content = await out_stream.read()

    with open('a.ttylog', 'wb') as fp:
        fp.write(content)

    print(content)


if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(get_file())
