import signal

from django.core.management.base import BaseCommand, CommandError

import dbq.workers


class Command(BaseCommand):
    def add_arguments(self, parser):
        subparsers = parser.add_subparsers()
        worker_cmd = subparsers.add_parser("worker")
        worker_cmd.set_defaults(worker_class=dbq.workers.TaskRunner)
        worker_cmd.add_argument("--queue", action="append", dest="queues")

        cron_cmd = subparsers.add_parser("cron")
        cron_cmd.set_defaults(worker_class=dbq.workers.Cron)

    def handle(self, *args, **options):
        # TODO handle sigint and call shutdown to gracefully close processes
        print(args)
        print(options)
        # worker = options["worker_class"].from_options(options)
        # worker.run()
        # worker.shutdown()
