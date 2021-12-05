import concurrent.futures
from time import sleep
import abc


class Data(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_content(self):
        pass


class RealData(Data):

    def __init__(self, count, c):
        print("making Read data(", count, ",", c, ") BEGIN")
        self.content = ""
        for i in range(count):
            self.content += c
            sleep(0.2)
        print("making Read data(", count, ",", c, ") END")

    def get_content(self):
        return self.content


class Host:

    def __init__(self):
        self.thread_pool = concurrent.futures.ThreadPoolExecutor()

    def request(self, count, char):
        return self.thread_pool.submit(self.call, count, char)

    @staticmethod
    def call(count, char):
        return RealData(count, char)


def main():
    print("Main BEGIN")
    host = Host()
    data1 = host.request(10, "A")
    data2 = host.request(20, "B")
    data3 = host.request(30, "C")

    print("main otherJob BEGIN")
    sleep(3.0)
    print("main otherJob END")

    print("data1=", data1.result().get_content())
    print("data2=", data2.result().get_content())
    print("data3=", data3.result().get_content())

    print("Main END")


main()
