import random
from queue import Queue
from time import sleep
import threading


class RequestQueue:
    def __init__(self):
        self.request_queue = Queue()
        self.cv_put = threading.Condition()
        self.cv_get = threading.Condition()

    def put_request(self, request):
        with self.cv_put:
            self.request_queue.put(request)
            self.cv_put.notify_all()

    def get_request(self):
        with self.cv_get:
            while self.request_queue.empty():
                self.cv_get.wait()
        return self.request_queue.get()


class Request:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "[ Request " + self.name + "]"

    def get_name(self):
        return self.name


class ClientThread(threading.Thread):

    def __init__(self, queue, name, address):
        super(ClientThread, self).__init__()
        self.name = name
        self.address = address
        self.queue = queue

    def run(self):
        print(" Client thread start", self.name)
        for i in range(10000):
            request = Request("No."+str(i))
            print(self.name, ":", request)
            self.queue.put_request(request)
            sleep(random.uniform(0, 1.0))


class ServerThread(threading.Thread):

    def __init__(self, queue, name, address):
        super(ServerThread, self).__init__()
        self.name = name
        self.address = address
        self.queue = queue

    def run(self):
        print(" Server thread start", self.name)
        for i in range(10000):
            request = self.queue.get_request()
            print(self.name, " handles ", request)
            sleep(random.uniform(0, 3.0))


def main():
    print("Testing Gate")
    request_queue = RequestQueue()
    ClientThread(request_queue, "Alice", 3212355).start()
    ServerThread(request_queue, "Bobby", 4534523).start()


main()