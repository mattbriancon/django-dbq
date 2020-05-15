import datetime
import pytest

import dbq
import dbq.tasks
import dbq.exceptions


class TestDecoratorValidation:
    def test_queue_must_be_in_settings(self):
        with pytest.raises(
            dbq.exceptions.ValidationException, match="queue must be in"
        ):
            dbq.task(queue="dogs")


class TestDecoratorCronValidation:
    def test_only_hours_fails_validation(self):
        with pytest.raises(
            dbq.exceptions.ValidationException, match="both hours and minutes"
        ):
            dbq.task(queue="test", hours=range(24))

    def test_only_hours_fails_validation_minutes_empty(self):
        with pytest.raises(
            dbq.exceptions.ValidationException, match="both hours and minutes"
        ):
            dbq.task(queue="test", hours=range(24), minutes=[])

    def test_only_minutes_fails_validation(self):
        with pytest.raises(
            dbq.exceptions.ValidationException, match="both hours and minutes"
        ):
            dbq.task(queue="test", minutes=range(60))

    def test_only_minutes_fails_validation_hours_empty(self):
        with pytest.raises(
            dbq.exceptions.ValidationException, match="both hours and minutes"
        ):
            dbq.task(queue="test", hours=[], minutes=range(60))

    def test_hours_bounds(self):
        with pytest.raises(dbq.exceptions.ValidationException, match="0 <= hour <= 23"):
            dbq.task(queue="test", hours=[-1], minutes=range(60))

        with pytest.raises(dbq.exceptions.ValidationException, match="0 <= hour <= 23"):
            dbq.task(queue="test", hours=[24], minutes=range(60))

        with pytest.raises(dbq.exceptions.ValidationException, match="0 <= hour <= 23"):
            dbq.task(queue="test", hours=range(25), minutes=range(60))

    def test_minutes_bounds(self):
        with pytest.raises(dbq.exceptions.ValidationException, match="0 <= minute <= 59"):
            dbq.task(queue="test", hours=range(24), minutes=[-1])

        with pytest.raises(dbq.exceptions.ValidationException, match="0 <= minute <= 59"):
            dbq.task(queue="test", hours=range(24), minutes=[60])

        with pytest.raises(dbq.exceptions.ValidationException, match="0 <= minute <= 59"):
            dbq.task(queue="test", hours=range(24), minutes=range(61))

    def test_hours_and_minutes_are_deduplicated(self):
        @dbq.task(queue="test", hours=[1, 1, 1], minutes=[1, 1, 1])
        def myfunc():
            pass

        assert isinstance(myfunc, dbq.tasks.Task)
        assert myfunc.times == [datetime.time(1, 1)]


class TestIntegration:

    def test_something(self):
        @dbq.task(queue="test")
        def long_running_work(thing: str) -> str:
            """something awesome"""
            print(f"hello! {thing}")



# # cron/scheduled task
# @dbq.task(queue="another", hours=range(24), minutes=range(60))
# def scheduled() -> str:
#     pass


# # async
# long_running_work('thing1').delay()

# # sync
# long_running_work('thing2').run()
