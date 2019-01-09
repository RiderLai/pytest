from u16d8 import DemoException
from u16d5 import coroutine


@coroutine
def demo_finally():
    print('-> coroutine started')
    try:
        while True:
            try:
                receive = yield
            except DemoException:
                print('*** DemoException handled. Continuing... ')
            else:
                print('-> coroutine receive:{!r}'.format(receive))
    finally:
        print('-> coroutine ending')
