from time import sleep
import queue
import threading


class RealResult:

    def __init__(self, string):
        self.result_value = string

    def get_result_value(self):
        return self.result_value


class Servant:

    @staticmethod
    def make_string(count, fill_char):
        buffer = "" * count
        for i in range(count):
            buffer = buffer[:i] + fill_char + buffer[i+1:]
            sleep(0.1)

        return RealResult(buffer)

    @staticmethod
    def display_string(string):
        print("display string:", string)
        sleep(0.01)


class SchedulerThread(threading.Thread):

    def __init__(self, aqueue):
        super(SchedulerThread, self).__init__()
        self.queue = aqueue

    def invoke(self, request):
        self.queue.put(request)

    def run(self):
        while True:
            request = self.queue.get()
            request.execute()


class DisplayStringRequest:

    def __init__(self, servant, string):
        self.servant = servant
        self.string = string

    def execute(self):
        self.servant.display_string(self.string)


class MakeStringRequest:

    def __init__(self, servant, future, count, fill_char):
        self.count = count
        self.servant = servant
        self.future = future
        self.fill_char = fill_char

    def execute(self):
        result = self.servant.make_string(self.count, self.fill_char)
        self.future.set_result(result)


class FutureResult:

    def __init__(self):
        self.result = None
        self.ready = False
        self.cv = threading.Condition()

    def set_result(self, result):
        with self.cv:
            self.result = result
            self.ready = True
            self.cv.notify_all()

    def get_result_value(self):
        with self.cv:
            while not self.ready:
                self.cv.wait()
            return self.result.get_result_value()

        return self.result.get_result_value()


class Proxy:

    def __init__(self, scheduler, servant):
        self.scheduler = scheduler
        self.servant = servant

    def make_string(self, count, fill_char):
        future = FutureResult()
        self.scheduler.invoke(MakeStringRequest(self.servant, future, count, fill_char))
        return future

    def display_string(self, string):
        self.scheduler.invoke(DisplayStringRequest(self.servant, string))


class DisplayClientThread(threading.Thread):

    def __init__(self, name, active_object):
        super(DisplayClientThread, self).__init__()
        self.name = name
        self.active_object = active_object

    def run(self):
        for i in range(10**5):
            string = self.name + " " + str(i)
            self.active_object.display_string(string)
            sleep(0.2)


class MakerClientThread(threading.Thread):

    def __init__(self, name, active_object):
        super(MakerClientThread, self).__init__()
        self.name = name
        self.active_object = active_object
        self.fill_char = name[0]

    def run(self):
        for i in range(10**5):
            result = self.active_object.make_string(i, self.fill_char)
            sleep(0.1)
            value = result.get_result_value()
            print(self.name, ": value = ", value)


class ActiveObjectFactory:
    @staticmethod
    def create_active_object():
        servant = Servant()
        activation_queue = queue.Queue(maxsize=100)
        scheduler = SchedulerThread(activation_queue)
        proxy = Proxy(scheduler, servant)
        scheduler.start()
        return proxy


def main():
    active_object = ActiveObjectFactory.create_active_object()
    MakerClientThread("Alice", active_object).start()
    MakerClientThread("Bobby", active_object).start()
    DisplayClientThread("Chris", active_object).start()


main()
