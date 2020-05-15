import dbq
import dbq.tasks


def test_public_api():
    assert dbq.task == dbq.tasks.task
