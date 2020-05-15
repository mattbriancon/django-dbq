from django.conf import settings

QUEUES_SORTED = sorted(settings.DBQ_QUEUES)
QUEUES_SET = set(QUEUES_SORTED)
# TODO when should old tasks be cleaned up?
