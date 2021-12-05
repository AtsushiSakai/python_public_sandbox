import threading


class Gate:
    def __init__(self):
        self.counter = 0
        self.name = "Nobody"
        self.address = "Nowhere"
        self.cv = threading.Condition()

    def through(self, name, address):
        with self.cv:
            self.counter += 1
            self.name = name
            self.address = address
            self.check()

    def __str__(self):
        return "No." + str(self.counter) + ": " + self.name + ", " + self.address

    def check(self):
        if self.name[0] != self.address[0]:
            print("**** Broken *****", self.__str__())


class UserThread(threading.Thread):

    def __init__(self, gate, myname, myaddress):
        super(UserThread, self).__init__()
        self.gate = gate
        self.myname = myname
        self.myaddress = myaddress

    def run(self):
        print("start", self.myname)
        while True:
            self.gate.through(self.myname, self.myaddress)


def main():
    print("Testing Gate")
    gate = Gate()

    UserThread(gate, "Alice", "Alaska").start()
    UserThread(gate, "Bobby", "Brazil").start()
    UserThread(gate, "Chris", "Chnada").start()


main()
