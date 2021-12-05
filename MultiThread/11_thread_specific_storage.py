import threading
from time import sleep


class Log:
    tl = threading.local()

    @staticmethod
    def open(name):
        Log.tl.f = open(name+"-log.txt", mode='w')

    @staticmethod
    def println(s):
        Log.tl.f.write(str(s))

    @staticmethod
    def close():
        Log.tl.f.close()


class ClientThread(threading.Thread):

    def __init__(self, name):
        super(ClientThread, self).__init__()
        self.name = name

    def run(self):
        Log.open(self.name)
        print(" Client thread start", self.name)
        for i in range(10):
            Log.println(i)
            sleep(0.1)

        Log.close()
        print(" Client thread end", self.name)


def main():
    ClientThread("Alice").start()
    ClientThread("Bobby").start()
    ClientThread("Chris").start()


main()
