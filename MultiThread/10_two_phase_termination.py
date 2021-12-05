from time import sleep
import threading


class CountUpThread(threading.Thread):

    def __init__(self):
        super(CountUpThread, self).__init__()
        self.counter = 0
        self.shutdown_requested = False

    def shutdown_request(self):
        self.shutdown_requested = True

    def is_shutdown_requested(self):
        return self.shutdown_requested

    def run(self):
        print(" Client thread start", self.name)
        while not self.is_shutdown_requested():
            self.do_work()
        self.do_shutdown()

    def do_work(self):
        self.counter += 1
        print("do work: count = ", self.counter)
        sleep(0.5)

    def do_shutdown(self):
        print("do shutdown: count=", self.counter)


def main():
    t = CountUpThread()
    t.start()

    sleep(3.0)

    print("shutdown request")
    t.shutdown_request()

    print("min: join")
    t.join()

    print("Main END")


main()
