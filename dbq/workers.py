import typing


class Worker:

    def __init__(self, queues: typing.List[str] = None):
        self.queues = queues

    def run(self):
        pass

    def shutdown(self):
        pass


class TaskRunner:
    pass


class Cron:
    pass
