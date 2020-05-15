from django.core.management import call_command


class TestSubcommandWorker:
    def test_subcommand_exists(self):
        call_command("dbq", "worker")


class TestSubcommandCron:
    def test_subcommand_exists(self):
        call_command("dbq", "cron")
