import random
import threading
from queue import Queue
from time import sleep


class MakerThread(threading.Thread):

    def __init__(self, name, table):
        super(MakerThread, self).__init__()
        self.name = name
        self.id = 0
        self.table = table
        self.cv = threading.Condition()

    def next_id(self):
        with self.cv:
            self.id += 1
            return self.id

    def run(self):
        print(" Eater thread start", self.name)
        for i in range(10000):
            sleep(random.uniform(0, 3.0))
            cake = "[Cake No." + str(self.next_id()) + "]"
            print("[" + self.name + "]Put:" + cake)
            self.table.put(cake)


class EaterThread(threading.Thread):

    def __init__(self, name, table):
        super(EaterThread, self).__init__()
        self.name = name
        self.table = table

    def run(self):
        print(" Eater thread start", self.name)
        for i in range(10000):
            cake = self.table.get()
            print("[" + self.name + "]Get:" + cake)
            sleep(random.uniform(0, 3.0))


def main():
    table = Queue(maxsize=3)
    MakerThread("MakerThread-1", table).start()
    MakerThread("MakerThread-2", table).start()
    MakerThread("MakerThread-3", table).start()
    EaterThread("EaterThread-1", table).start()
    EaterThread("EaterThread-2", table).start()
    EaterThread("EaterThread-3", table).start()


main()
