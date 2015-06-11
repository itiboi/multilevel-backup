#!/usr/bin/env python
# coding=utf-8

from backup import perform_backup
from nose.tools import istest, assert_equals

tag_sync = 'sync'
tag_daily = 'daily'
tag_weekly = 'weekly'
tag_monthly = 'monthly'

class MonitoringBackupManager(object):
    def __init__(self, daily_needed, weekly_needed, monthly_needed):
        self.daily_needed = daily_needed
        self.weekly_needed = weekly_needed
        self.monthly_needed = monthly_needed
        self._performed_tasks = []

    @property
    def is_daily_needed(self):
        return self.daily_needed

    @property
    def is_weekly_needed(self):
        return self.weekly_needed

    @property
    def is_monthly_needed(self):
        return self.monthly_needed

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

@istest
def test_nothing_needed():
    mocked_manager = MonitoringBackupManager(False, False, False)
    perform_backup(mocked_manager)

    assert_equals([], mocked_manager.performed_tasks)

@istest
def test_daily_already_executed():
    mocked_manager = MonitoringBackupManager(False, True, True)
    perform_backup(mocked_manager)

    assert_equals([], mocked_manager.performed_tasks)

@istest
def test_only_daily():
    mocked_manager = MonitoringBackupManager(True, False, False)
    perform_backup(mocked_manager)

    assert_equals([tag_sync, tag_daily], mocked_manager.performed_tasks)

@istest
def test_daily_weekly():
    mocked_manager = MonitoringBackupManager(True, True, False)
    perform_backup(mocked_manager)

    assert_equals([tag_sync, tag_weekly, tag_daily], mocked_manager.performed_tasks)

@istest
def test_full():
    mocked_manager = MonitoringBackupManager(True, True, True)
    perform_backup(mocked_manager)

    assert_equals([tag_sync, tag_monthly, tag_weekly, tag_daily], mocked_manager.performed_tasks)

@istest
def test_monthly_without_weekly():
    mocked_manager = MonitoringBackupManager(True, False, True)
    perform_backup(mocked_manager)

    assert_equals([tag_sync, tag_daily], mocked_manager.performed_tasks)