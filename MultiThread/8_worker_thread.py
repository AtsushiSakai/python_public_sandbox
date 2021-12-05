import threading
import queue
import time
import random


class Channel:
    MAX_REQUEST = 100

    def __init__(self, threads):
        self.request_queue = queue.Queue(maxsize=self.MAX_REQUEST)
        self.thread_pool = []
        self.cv = threading.Condition()
        for i in range(threads):
            self.thread_pool.append(WorkerThread("Worker-" + str(i), self))

    def start_workers(self):
        for i in range(len(self.thread_pool)):
            self.thread_pool[i].start()

    def put_request(self, request):
        self.request_queue.put(request)
        # self.cv.notify_all()

    def take_request(self):
        request = self.request_queue.get()
        # self.cv.notify_all()
        return request


class Request:

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def execute(self):
        print(threading.current_thread().name+" executes"+self.__str__())
        time.sleep(random.uniform(0, 1))

    def __str__(self):
        return "[ Request from" + self.name + " No. "+str(self.number)+"]"


class ClientThread(threading.Thread):

    def __init__(self, name, channel):
        super(ClientThread, self).__init__()
        self.name = name
        self.channel = channel

    def run(self):
        print("start ClientThread", self.name)
        for i in range(100000):
            request = Request(threading.current_thread().name, i)
            self.channel.put_request(request)
            time.sleep(random.uniform(0, 1))
        print("stop ClientThread", self.name)


class WorkerThread(threading.Thread):

    def __init__(self, name, channel):
        super(WorkerThread, self).__init__()
        self.name = name
        self.channel = channel

    def run(self):
        print("start Worker thread", self.name)
        for i in range(10000):
            request = self.channel.take_request()
            request.execute()
        print("stop Worker thread", self.name)



def main():
    print("Start Main")
    channel = Channel(5)
    channel.start_workers()
    ClientThread("Alice", channel).start()
    ClientThread("Bobby", channel).start()
    ClientThread("Chris", channel).start()
    print("End Main")


main()
