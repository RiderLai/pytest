import time
import sys
import os
from enum import Enum
from collections import namedtuple, Counter
from concurrent import futures

import requests
import tqdm

HTTPStatus = Enum('Status', 'ok not_found error')
Result = namedtuple('Result', 'status cc')

BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'


def get_flag(cc):
    response = requests.get('{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower()))
    if response.status_code != 200:
        response.raise_for_status()
    return response.content


def save_flag(img, filename):
    if not os.path.exists(DEST_DIR):
        os.mkdir(DEST_DIR)

    with open(os.path.join(DEST_DIR, filename), 'wb') as fp:
        fp.write(img)


def download_one(cc, verbose=False):
    try:
        img = get_flag(cc)
    except requests.exceptions.HTTPError as exc:
        res = exc.response
        if res.status_code == 404:
            status = HTTPStatus.not_found
            msg = 'not found'
        else:
            raise
    else:
        save_flag(img, '{}.gif'.format(cc.lower()))
        status = HTTPStatus.ok
        msg = 'ok'

    if verbose:
        print(cc, msg)

    return Result(status, cc)


def download_many(cc_list):
    counter = Counter()
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do_map = {}
        for cc in cc_list:
            future = executor.submit(download_one, cc)
            to_do_map[future] = cc

        done_iter = futures.as_completed(to_do_map)
        done_iter = tqdm.tqdm(done_iter, total=len(cc_list))

        for future in done_iter:
            try:
                res = future.result()
            except requests.exceptions.HTTPError as exc:
                error_msg = 'HTTP {res.status_code} - {res.reason}'
                error_msg = error_msg.format(res=exc.response)
            except requests.exceptions.ConnectionError as exc:
                error_msg = 'Connection error'
            else:
                error_msg = ''
                status = res.status

            if error_msg:
                status = HTTPStatus.error
                cc = to_do_map[future]
                print('*** Error for {}: {}'.format(cc, error_msg))

            counter[status] += 1

    return counter


# from flags import POP20_CC
# counter = download_many(POP20_CC)
# print('-'*20)