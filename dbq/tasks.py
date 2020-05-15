import datetime
import functools
import inspect
import operator
import typing

from . import exceptions, settings

# # async
# long_running_work('thing1').delay()

# # sync
# long_running_work('thing2').run()


class Runnable:
    def __init__(self, task: "Task", *args, **kwargs):
        self.task = task
        self.args = args
        self.kwargs = kwargs

    def delay(self):
        pass

    def run(self):
        return self.task.func(*self.args, **self.kwargs)


class Task:
    def __init__(
        self, func: typing.Callable, queue: str, times: typing.List[datetime.time],
    ):
        self.func = func
        self.queue = queue
        self.times = times

        # functools.update_wrapper(
        #     self.__call__,
        #     self.func,
        #     assigned=("__name__", "__qualname__", "__doc__", "__annotations__"),
        # )
        # def __call__(self, *args, **kwargs):
        #     return Runnable(self, *args, **kwargs)
        # self.__call__ = functools.wraps(func)(__call__).__get__(self)  # type: ignore
        # self.__call__.__signature__ = inspect.signature(self.func)


def task(
    *,
    queue: str,
    hours: typing.Collection[int] = None,
    minutes: typing.Collection[int] = None,
):
    if queue not in settings.QUEUES_SET:
        raise exceptions.ValidationException(
            "queue must be in the list of settings.DBQ_QUEUES"
        )

    if operator.xor(bool(hours), bool(minutes)):
        raise exceptions.ValidationException(
            "both hours and minutes must be specified (or neither)"
        )

    if hours and minutes:
        if len(hours) > 24 or any(h < 0 or h > 23 for h in hours):
            raise exceptions.ValidationException(
                "hours must be a collection of int where 0 <= hour <= 23"
            )

        if len(minutes) > 60 or any(m < 0 or m > 59 for m in minutes):
            raise exceptions.ValidationException(
                "minutes must be a collection of int where 0 <= minute <= 59"
            )

        times = sorted(
            datetime.time(hour, minute)
            for hour in set(hours)
            for minute in set(minutes)
        )
    else:
        times = []

    def decorator(func):
        task = Task(func, queue, times)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return Runnable(task, *args, **kwargs)

        wrapper._dbq_task = task
        return wrapper

        wrapper.__signature__ = inspect.signature(func)

    return decorator
