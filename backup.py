#!/usr/bin/env python
# coding=utf-8

import sys

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

daily_count = 5
weekly_count = 4

backup_root = '/home/tim/backup/rsnapshot/'
daily_first = path.join(backup_root, 'daily.0')
daily_last = path.join(backup_root, 'daily.' + str(daily_count-1))
daily_diff = timedelta(days=1)

weekly_first = path.join(backup_root, 'weekly.0')
weekly_last = path.join(backup_root, 'weekly.' + str(weekly_count-1))
weekly_diff = timedelta(days=7)

monthly_first = path.join(backup_root, 'monthly.0')
monthly_diff = timedelta(days=28)


if path.exists(daily_first) and (date.today() - folder_time(daily_first)) < daily_diff:
    # Abbruch, heute schon Backup gemacht
    print('Abort: Daily backup already performed')
    sys.exit()

# Sync durchführen
print('Performing sync')

# Ggf. Monthly Backup durchführen
if level_backup_needed(monthly_first, weekly_last, monthly_diff):
    print('Performing monthly backup')

# Ggf. Weekly Backup durchführen
if level_backup_needed(weekly_first, daily_last, weekly_diff):
    print('Performing weekly backup')

print('Performing daily backup')