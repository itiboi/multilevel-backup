from os import path
from datetime import date, timedelta

import subprocess
import shlex


def _folder_time(folder):
    """Get day timestamp of a folder as date."""
    stamp = path.getmtime(folder)
    return date.fromtimestamp(stamp)


def _level_backup_needed(upper_first, lower_last, min_diff):
    """Check whether backup of this increment level is needed."""
    if not path.exists(lower_last):
        return False

    if path.exists(upper_first):
        # Only perform if enough time passed
        time_upper = _folder_time(upper_first)
        time_lower = _folder_time(lower_last)
        return (time_lower - time_upper) >= min_diff
    else:
        # First backup of higher level
        return True


class DefaultSnapshotManager(object):
    """Provide information about current backup state."""
    _daily_count = 5
    _weekly_count = 4

    def __init__(self, backup_root):
        self.daily_first = path.join(backup_root, 'daily.0')
        self.daily_last = path.join(backup_root, 'daily.' + str(self._daily_count-1))
        self.daily_diff = timedelta(days=1)

        self.weekly_first = path.join(backup_root, 'weekly.0')
        self.weekly_last = path.join(backup_root, 'weekly.' + str(self._weekly_count-1))
        self.weekly_diff = timedelta(days=7)

        self.monthly_first = path.join(backup_root, 'monthly.0')
        self.monthly_diff = timedelta(days=28)

    @property
    def is_daily_needed(self):
        if not path.exists(self.daily_first):
            return True

        delta = date.today() - _folder_time(self.daily_first)
        return delta >= self.daily_diff

    @property
    def is_weekly_needed(self):
        return _level_backup_needed(self.weekly_first, self.daily_last, self.weekly_diff)

    @property
    def is_monthly_needed(self):
        return _level_backup_needed(self.monthly_first, self.weekly_last, self.monthly_diff)

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
    _rsnapshot_command_template = 'rsnapshot -c {file} {action}'

    def __init__(self, conf_file='rsnapshot.conf', dry_run=False):
        self.conf_file = conf_file
        self.dry_run = dry_run

    def perform_sync(self):
        print('-- Performing sync')

        if not self.dry_run:
            command = self._rsnapshot_command_template.format(file=self.conf_file, action='sync')
            subprocess.check_call(shlex.split(command))

    def perform_daily(self):
        print('\n-- Performing daily backup')

        if not self.dry_run:
            command = self._rsnapshot_command_template.format(file=self.conf_file, action='daily')
            subprocess.check_call(shlex.split(command))

    def perform_weekly(self):
        print('\n-- Performing weekly backup')

        if not self.dry_run:
            command = self._rsnapshot_command_template.format(file=self.conf_file, action='weekly')
            subprocess.check_call(shlex.split(command))

    def perform_monthly(self):
        print('\n-- Performing monthly backup')

        if not self.dry_run:
            command = self._rsnapshot_command_template.format(file=self.conf_file, action='monthly')
            subprocess.check_call(shlex.split(command))


def perform_backup(snapshot_manager=None, backup_executor=None):
    """Perform actual backup. Relies on a backup manager for information retrieving and backup performing."""

    # Use default manager if none given
    if snapshot_manager is None:
        snapshot_manager = DefaultSnapshotManager(backup_root='/home/tim/backup/rsnapshot/')

    # Use default backup executor if none given
    if backup_executor is None:
        backup_executor = DefaultBackupExecutor()

    tasks = snapshot_manager.upcoming_tasks

    # Test whether backup is needed in general
    if not tasks['daily']:
        print('Abort: Daily backup already performed')
        return

    # Perform sync (actual backup)
    backup_executor.perform_sync()

    # Perform monthly if needed
    if tasks['monthly']:
        backup_executor.perform_monthly()

    # Perform weekly if needed
    if tasks['weekly']:
        backup_executor.perform_weekly()

    # Perform daily
    backup_executor.perform_daily()
