import pickle

from django.db import models


class PickleField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 1024)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, bytes):
            return pickle.loads(value)
        return value

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return pickle.loads(value)

    def get_prep_value(self, value):
        return pickle.dumps(value)


class Task(models.Model):
    function_path = models.CharField(max_length=1024)
    args = PickleField()
    kwargs = PickleField()

    queue = models.CharField(max_length=512)

    created_at = models.DateTimeField()
    available_after = models.DateTimeField()
