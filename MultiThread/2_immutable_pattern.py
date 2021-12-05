import threading


class Gate:
    def __init__(self, name, address):
        self.counter = 0
        self._name = name
        self._address = address

    def through(self):
        self.counter += 1
        self.check()

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    def __str__(self):
        return "No." + str(self.counter) + ": " + self._name + ", " + self._address

    def check(self):
        if self.name[0] != self.address[0]:
            print("**** Broken *****", self.__str__())


class UserThread(threading.Thread):

    def __init__(self, gate):
        super(UserThread, self).__init__()
        self.gate = gate

    def run(self):
        print("start")
        while True:
            # self.gate.name = "aaa" # error
            self.gate.through()


def main():
    print("Testing Gate")
    gate = Gate("Alice", "Alaska")

    UserThread(gate).start()
    UserThread(gate).start()
    UserThread(gate).start()


main()