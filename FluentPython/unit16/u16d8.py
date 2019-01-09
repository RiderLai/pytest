from u16d5 import coroutine


class DemoException(Exception):
    def __init__(self):
        pass


@coroutine
def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:
            print('*** DemoException handled. Continuing... ')
        else:
            print('-> coroutine received: {!r}'.format(x))
    raise RuntimeError('This line should never run')
