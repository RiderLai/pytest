import time
from tornado import ioloop


def test():
    index = 0

    def inner():
        nonlocal index
        index += 1
        print('test', index, time.localtime())
        # time.sleep(1)

    return inner


def test2():
    print('test2', time.localtime())


if __name__ == '__main__':
    periodic_cb = ioloop.PeriodicCallback(test(), 1000)
    periodic_cb.start()

    periodic_test2 = ioloop.PeriodicCallback(test2, 1000)
    periodic_test2.start()

    ioloop.IOLoop.current().start()
