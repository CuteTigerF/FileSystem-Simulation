from file_system import manager
from multiprocessing.connection import Listener, wait
import threading
import time


def main():

    fsm = manager.FileSystemManager()

    address = ('localhost', 7000)

    print('Listening:', address[0])

    while True:

        with Listener(address, authkey=b'secret password') as listener:

            with listener.accept() as conn:

                print('connection accepted from', listener.last_accepted)

                msg = conn.recv()

                fsm.input(msg)

                result = fsm.output()

                conn.send(str(result))


if __name__ == '__main__':
    main()
