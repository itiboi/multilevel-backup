#!/usr/bin/env python
# coding=utf-8

from os import path
from datetime import date, timedelta

def folder_time(folder):
    """Get day timestamp of a folder as date."""
    stamp = path.getmtime(folder)
    return date.fromtimestamp(stamp)

def level_backup_needed(upper_first, lower_last, min_diff):
    """Check whether backup of this increment level is needed."""
    if not path.exists(lower_last):
        return False

    if path.exists(upper_first):
        # Nur durchführen wenn Zeitraum verstrichen
        time_upper = folder_time(upper_first)
        time_lower = folder_time(lower_last)
        return (time_lower - time_upper) >= min_diff
    else:
        # Erstes Backup des höheren Levels
        return True

class RsnapshotManager(object):
    _daily_count = 5
    _weekly_count = 4

    def __init__(self, backup_root='/home/tim/backup/rsnapshot/'):
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

        delta = date.today() - folder_time(self.daily_first)
        return delta >= self.daily_diff

    @property
    def is_weekly_needed(self):
        return level_backup_needed(self.weekly_first, self.daily_last, self.weekly_diff)

    @property
    def is_monthly_needed(self):
        return level_backup_needed(self.monthly_first, self.weekly_last, self.monthly_diff)

    def perform_sync(self):
        print('Performing sync')

    def perform_daily(self):
        print('Performing daily backup')

    def perform_weekly(self):
        print('Performing weekly backup')

    def perform_monthly(self):
        print('Performing monthly backup')

def perform_backup(backup_manager=None):
    """Perform actual backup. Relies on a backup manager for information retrieving and backup performing."""

    if backup_manager is None:
        backup_manager = RsnapshotManager()

    # Testen ob Backup generell nötig
    if not backup_manager.is_daily_needed:
        # Abbruch, heute schon Backup gemacht
        print('Abort: Daily backup already performed')
        return

    # Sync durchführen
    backup_manager.perform_sync()

    # Ggf. Weekly Backup durchführen
    if backup_manager.is_weekly_needed:
        # Ggf. vorher Monthly Backup durchführen
        if backup_manager.is_monthly_needed:
            backup_manager.perform_monthly()

        backup_manager.perform_weekly()

    backup_manager.perform_daily()

if __name__ == '__main__':
    perform_backup()
