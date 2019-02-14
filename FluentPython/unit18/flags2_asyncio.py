import asyncio
import os
from enum import Enum
from collections import namedtuple, Counter

import aiohttp
from aiohttp import web
import tqdm

HTTPStatus = Enum('Status', 'ok not_found error')
Result = namedtuple('Result', 'status cc')

BASE_URL = 'http://flupy.org/data/flags'
POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
DEST_DIR = 'downloads/'
DEFAULT_CONCUR_REQ = 5


class FetchError(Exception):
    def __init__(self, country_code):
        self.country_code = country_code


def save_flag(img, filename):
    if not os.path.exists(DEST_DIR):
        os.mkdir(DEST_DIR)

    with open(os.path.join(DEST_DIR, filename), 'wb') as fp:
        fp.write(img)


@asyncio.coroutine
def http_get(url):
    client = aiohttp.ClientSession()
    resp = yield from client.get(url)
    # yield from client.close()   堵住了 天呐
    if resp.status == 200:
        ctype = resp.headers.get('Content-type', '').lower()
        if 'json' in ctype or url.endswith('json'):
            result = yield from resp.json()
        else:
            result = yield from resp.read()
        return result
    elif resp.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.http.HttpProcessingError(
            code=resp.status, message=resp.reason,
            headers=resp.headers)


@asyncio.coroutine
def get_flag(cc):
    img = yield from http_get('{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower()))
    return img


@asyncio.coroutine
def get_country(cc):
    metadata = yield from http_get('{}/{cc}/metadata.json'.format(BASE_URL, cc=cc.lower()))
    return metadata['country']


@asyncio.coroutine
def download_one(cc, semaphorre):
    try:
        with (yield from semaphorre):
            img = yield from get_flag(cc)
        with (yield from semaphorre):
            country = yield from get_country(cc)
    except web.HTTPNotFound:
        status = HTTPStatus.not_found
    except Exception as exc:
        raise FetchError(cc) from exc
    else:
        country = country.replace(' ', '_')
        filename = '{}-{}.gif'.format(country, cc)
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, save_flag, img, filename)
        # save_flag(img, filename)
        status = HTTPStatus.ok

    return Result(status, cc)


@asyncio.coroutine
def downloader_coro(cc_list, concur_req):
    counter = Counter()
    semaphore = asyncio.Semaphore(concur_req)
    to_do = [download_one(cc, semaphore) for cc in sorted(cc_list)]
    to_do_iter = asyncio.as_completed(to_do)
    to_do_iter = tqdm.tqdm(to_do_iter, total=len(to_do))

    for future in to_do_iter:
        try:
            res = yield from future
        except FetchError as exc:
            country_code = exc.country_code
            try:
                error_msg = exc.__cause__.args[0]
            except IndexError:
                error_msg = exc.__cause__.__class__.__name__
            msg = '*** Error for {}: {}'
            print(msg.format(country_code, error_msg))
            status = HTTPStatus.error
        else:
            status = res.status

        counter[status] += 1

    return counter


def download_many(cc_list):
    loop = asyncio.get_event_loop()
    coro = downloader_coro(cc_list, DEFAULT_CONCUR_REQ)
    counts = loop.run_until_complete(coro)
    loop.close()
    return counts


download_many(POP20_CC)