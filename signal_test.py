import sys
from time import sleep
from signal import signal, SIGINT, SIGTERM

from psutil import Process
from tornado.process import fork_processes

is_running = True
pid = None


def stop(code: int, frame=None):
    print('code: ', code)
    print('frame: ', frame)
    print('process stopped pid is ', pid)
    global is_running
    is_running = False


class Entry():

    def __init__(self):
        self._is_stopped = False
        self._is_start = False

        signal(SIGINT, self.stop)
        signal(SIGTERM, self.stop)

        self._pid = fork_processes(2)

    def start(self):
        self._is_start = True
        while self._is_start:
            print('%s is running...' % str(self._pid))
            sleep(1)

    def stop(self, code: int, frame=None):

        skip = self.relay_signal(code)

        if skip:
            print('mian process stopped')

        if not skip and not self._is_stopped:
            self._is_stopped = True
            self._is_start = False
            print('process stopped pid is ', str(self._pid))

        sys.exit(0)

    def relay_signal(self, code):
        children = Process().children()

        if children:
            for child in children:
                child.send_signal(code)
            return True
        return False


if __name__ == '__main__':
    # signal(SIGINT, stop)
    # signal(SIGTERM, stop)
    # pid = fork_processes(2)
    #
    # import time
    # import os
    # print(os.getpid())
    # while is_running:
    #     print('%s is running...' % pid)
    #     time.sleep(1)
    Entry().start()
