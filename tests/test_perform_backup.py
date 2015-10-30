from multilevelbackup import perform_backup

tag_sync = 'sync'
tag_daily = 'daily'
tag_weekly = 'weekly'
tag_monthly = 'monthly'


class MonitoringBackupManager(object):
    def __init__(self, daily, weekly, monthly):
        self.tasks = {'daily': daily, 'weekly': weekly, 'monthly': monthly}
        self._performed_tasks = []

    @property
    def is_daily_needed(self):
        return self.tasks['daily']

    @property
    def is_weekly_needed(self):
        return self.tasks['weekly']

    @property
    def is_monthly_needed(self):
        return self.tasks['monthly']

    @property
    def upcoming_tasks(self):
        return self.tasks

    def perform_sync(self):
        self._performed_tasks.append(tag_sync)

    def perform_daily(self):
        self._performed_tasks.append(tag_daily)

    def perform_weekly(self):
        self._performed_tasks.append(tag_weekly)

    def perform_monthly(self):
        self._performed_tasks.append(tag_monthly)

    @property
    def performed_tasks(self):
        return self._performed_tasks


def test_nothing_needed():
    mocked_manager = MonitoringBackupManager(daily=False, weekly=False, monthly=False)
    perform_backup(manager=mocked_manager, executor=mocked_manager)

    assert [] == mocked_manager.performed_tasks


def test_daily_already_executed():
    mocked_manager = MonitoringBackupManager(daily=False, weekly=True, monthly=True)
    perform_backup(manager=mocked_manager, executor=mocked_manager)

    assert [] == mocked_manager.performed_tasks


def test_only_daily():
    mocked_manager = MonitoringBackupManager(daily=True, weekly=False, monthly=False)
    perform_backup(manager=mocked_manager, executor=mocked_manager)

    assert [tag_sync, tag_daily] == mocked_manager.performed_tasks


def test_daily_weekly():
    mocked_manager = MonitoringBackupManager(daily=True, weekly=True, monthly=False)
    perform_backup(manager=mocked_manager, executor=mocked_manager)

    assert [tag_sync, tag_weekly, tag_daily] == mocked_manager.performed_tasks


def test_full():
    mocked_manager = MonitoringBackupManager(daily=True, weekly=True, monthly=True)
    perform_backup(manager=mocked_manager, executor=mocked_manager)

    assert [tag_sync, tag_monthly, tag_weekly, tag_daily] == mocked_manager.performed_tasks


def test_monthly_without_weekly():
    mocked_manager = MonitoringBackupManager(daily=True, weekly=False, monthly=True)
    perform_backup(manager=mocked_manager, executor=mocked_manager)

    assert [tag_sync, tag_monthly, tag_daily] == mocked_manager.performed_tasks
