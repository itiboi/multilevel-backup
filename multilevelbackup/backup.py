from os import path
from datetime import date, timedelta

import subprocess
import shlex

from .helpers import folder_time, level_backup_needed
from .config import intervals_from_config, backup_root_from_config


class DefaultSnapshotManager(object):
    """Provide information about current backup state."""

    def __init__(self, backup_root, daily_count=7, weekly_count=4):
        self.daily_first = path.join(backup_root, 'daily.0')
        self.daily_last = path.join(backup_root, 'daily.' + str(daily_count-1))
        self.daily_diff = timedelta(days=1)

        self.weekly_first = path.join(backup_root, 'weekly.0')
        self.weekly_last = path.join(backup_root, 'weekly.' + str(weekly_count-1))
        self.weekly_diff = timedelta(days=7)

        self.monthly_first = path.join(backup_root, 'monthly.0')
        self.monthly_diff = timedelta(days=28)

    @staticmethod
    def create_from_rsnapshot_conf(conf_file):
        config = open(conf_file, 'r').read()

        backup_root = backup_root_from_config(config)
        intervals = intervals_from_config(config)

        if 'daily' not in intervals or 'weekly' not in intervals:
            raise ValueError('No \'daily\' or \'weekly\' interval in rsnapshot config found')

        return DefaultSnapshotManager(backup_root=backup_root,
                                      daily_count=intervals['daily'],
                                      weekly_count=intervals['weekly'])

    @property
    def is_daily_needed(self):
        if not path.exists(self.daily_first):
            return True

        delta = date.today() - folder_time(self.daily_first)
        return delta >= self.daily_diff

    @property
    def is_weekly_needed(self):
        return level_backup_needed(self.weekly_first, self.daily_last, self.weekly_diff)

    @property
    def is_monthly_needed(self):
        return level_backup_needed(self.monthly_first, self.weekly_last, self.monthly_diff)

    @property
    def upcoming_tasks(self):
        """Dictionary which tasks should be performed today (daily=True/False, weekly=True/False, monthly=True/False)"""

        tasks = {'daily': False, 'weekly': False, 'monthly': False}
        if self.is_daily_needed:
            tasks['daily'] = True

        if tasks['daily'] and self.is_weekly_needed:
            tasks['weekly'] = True

        if tasks['weekly'] and self.is_monthly_needed:
            tasks['monthly'] = True

        return tasks


class DefaultBackupExecutor(object):
    _rsnapshot_command_template = 'rsnapshot {dry} -c {file} {{action}}'

    def __init__(self, conf_file, dry_run=False):
        dry_run_arg = '-t' if dry_run else ''
        self._command_template = self._rsnapshot_command_template.format(dry=dry_run_arg, file=conf_file)

    def perform_sync(self):
        print('-- Performing sync')

        command = self._command_template.format(action='sync')
        subprocess.check_call(shlex.split(command))

    def perform_daily(self):
        print('\n-- Performing daily backup')

        command = self._command_template.format(action='daily')
        subprocess.check_call(shlex.split(command))

    def perform_weekly(self):
        print('\n-- Performing weekly backup')

        command = self._command_template.format(action='weekly')
        subprocess.check_call(shlex.split(command))

    def perform_monthly(self):
        print('\n-- Performing monthly backup')

        command = self._command_template.format(action='monthly')
        subprocess.check_call(shlex.split(command))


def perform_backup(manager, executor):
    """
    Perform actual backup. Relies on a backup manager for information retrieving and backup performing.
    """

    tasks = manager.upcoming_tasks

    # Test whether backup is needed in general
    if not tasks['daily']:
        print('Abort: Daily backup already performed')
        return

    # Perform sync (actual backup)
    executor.perform_sync()

    # Perform monthly if needed
    if tasks['monthly']:
        executor.perform_monthly()

    # Perform weekly if needed
    if tasks['weekly']:
        executor.perform_weekly()

    # Perform daily
    executor.perform_daily()
