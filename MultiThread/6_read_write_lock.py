import random
import threading
from time import sleep


class ReadWriteLock:

    def __init__(self):
        self.reading_readers = 0
        self.waiting_writers = 0
        self.writing_writers = 0
        self.prefer_writer = True
        self.cv = threading.Condition()

    def read_lock(self):
        with self.cv:
            while self.writing_writers > 0 or (self.prefer_writer and self.waiting_writers > 0):
                self.cv.wait()

            self.reading_readers += 1

    def read_unlock(self):
        with self.cv:
            self.reading_readers -= 1
            self.prefer_writer = True
            self.cv.notify_all()

    def write_lock(self):
        with self.cv:
            self.waiting_writers += 1
            while self.reading_readers > 0 or self.writing_writers > 0:
                self.cv.wait()
            self.waiting_writers -= 1
            self.writing_writers += 1

    def write_unlock(self):
        with self.cv:
            self.writing_writers -= 1
            self.prefer_writer = False
            self.cv.notify_all()


class Data:

    def __init__(self, size):
        self.buffer = ["*"] * size
        self.lock = ReadWriteLock()

    def read(self):
        self.lock.read_lock()
        c = self.do_read()
        self.lock.read_unlock()
        return c

    def write(self, c):
        self.lock.write_lock()
        self.do_write(c)
        self.lock.write_unlock()

    def do_read(self):
        self.slowly()
        return self.buffer[:]

    def do_write(self, c):
        for i in range(len(self.buffer)):
            self.buffer[i] = c
            self.slowly()

    @staticmethod
    def slowly():
        sleep(0.1)


class ReaderThread(threading.Thread):

    def __init__(self, data):
        super(ReaderThread, self).__init__()
        self.data = data

    def run(self):
        print(" Reader thread start", self.name)
        for i in range(10000):
            read_buf = self.data.read()
            print(threading.current_thread().name + " reads " + "".join(read_buf))


class WriterThread(threading.Thread):

    def __init__(self, data, filler):
        super(WriterThread, self).__init__()
        self.data = data
        self.filler = filler
        self.index = 0

    def run(self):
        print(" Writer thread start", self.name)
        for i in range(10000):
            c = self.next_char()
            self.data.write(c)
            sleep(random.uniform(0, 0.1))

    def next_char(self):
        c = self.filler[self.index]
        self.index += 1
        if self.index >= len(self.filler):
            self.index = 0
        return c


def main():
    data = Data(19)
    WriterThread(data, "ABCDEFGHIJKLMNOP").start()
    WriterThread(data, "abcdefghijklmnop").start()
    ReaderThread(data).start()
    ReaderThread(data).start()
    ReaderThread(data).start()
    ReaderThread(data).start()
    ReaderThread(data).start()


main()
