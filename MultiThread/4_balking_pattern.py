import random
import threading
from time import sleep


class Data:
    def __init__(self, filename, content):
        self.cv_change = threading.Condition()
        self.cv_save = threading.Condition()
        self.filename = filename
        self.content = content
        self.changed = True

    def change(self, newContent):
        with self.cv_change:
            self.content = newContent
            self.changed = True

    def save(self):
        with self.cv_save:
            if not self.changed:
                return
            self.do_save()
            self.changed = False

    def do_save(self):
        print(threading.current_thread().name, " calls do Save. content=", self.content)
        with open(self.filename, 'a') as f:
            f.write(self.content)


class ChangerThread(threading.Thread):

    def __init__(self, name, data):
        super(ChangerThread, self).__init__()
        self.name = name
        self.data = data

    def run(self):
        print(" Client thread start", self.name)
        for i in range(10000):
            self.data.change("No." + str(i))
            sleep(random.uniform(0, 1.0))
            self.data.save()


class SaverThread(threading.Thread):

    def __init__(self, name, data):
        super(SaverThread, self).__init__()
        self.name = name
        self.data = data

    def run(self):
        print(" Server thread start", self.name)
        for i in range(10000):
            self.data.save()
            sleep(random.uniform(0, 3.0))


def main():
    data = Data("data.txt", "empty")
    ChangerThread("ChangerThread", data).start()
    SaverThread("SaveThread", data).start()


main()
