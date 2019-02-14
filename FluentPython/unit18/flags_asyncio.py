import asyncio
import os
import sys
import time

import aiohttp

BASE_URL = 'http://flupy.org/data/flags'
POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
DEST_DIR = 'downloads/'


def save_flag(img, filename):
    if not os.path.exists(DEST_DIR):
        os.mkdir(DEST_DIR)

    with open(os.path.join(DEST_DIR, filename), 'wb') as fp:
        fp.write(img)


def show(cc):
    print(cc, end=' ')
    sys.stdout.flush()


def main(download_many):
    start = time.time()
    result = download_many(POP20_CC)
    elapse = time.time() - start
    msg = '\n{} flags downloaded in {:2f}s'
    print(msg.format(result, elapse))


@asyncio.coroutine
def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = yield from aiohttp.ClientSession().get(url)
    img = yield from resp.read()
    # resp.close()
    return img


@asyncio.coroutine
def download_one(cc):
    img = yield from get_flag(cc)
    save_flag(img, cc.lower() + '.gif')
    show(cc)
    return cc


def download_many(cc_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(cc) for cc in cc_list]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()

    return len(res)


if __name__ == '__main__':
    main(download_many)
