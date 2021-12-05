import threading
import time


class Helper:

    @staticmethod
    def handle(count, c):
        print("handle, ", count, ",", c, " Start")
        for i in range(count):
            print(c)
            time.sleep(0.1)
        print("handle, ", count, ",", c, " End")


class Host:
    def __init__(self):
        self.helper = Helper()

    def request(self, count, c):
        print("request, ", count, ",", c, " Start")
        threading.Thread(target=self.helper.handle, args=(count, c)).start()
        print("request, ", count, ",", c, " End")


def main():
    print("Start Main")
    host = Host()
    host.request(10, "A")
    host.request(20, "B")
    host.request(30, "C")
    print("End Main")


main()
