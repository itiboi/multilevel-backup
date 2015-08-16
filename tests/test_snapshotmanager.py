#!/usr/bin/env python
# coding=utf-8

from backup import DefaultSnapshotManager
from datetime import datetime
from nose.tools import assert_true, assert_false, assert_equals
from unittest import TestCase
from unittest.mock import patch, PropertyMock

import os
import shutil
import tempfile


class LevelIndicatorTest(TestCase):
    """Test whether every level indicator works properly."""

    def setUp(self):
        self.test_folder = tempfile.mkdtemp()
        self.snapshot_manager = DefaultSnapshotManager(backup_root=self.test_folder)

    def tearDown(self):
        shutil.rmtree(self.test_folder)

    def _create_folder(self, folder, timestamp):
        os.makedirs(folder)
        os.system('touch -t {time:%Y%m%d%H%M.%S} {file}'.format(time=timestamp, file=folder))

    def test_empty_folder(self):
        assert_true(self.snapshot_manager.is_daily_needed)
        assert_false(self.snapshot_manager.is_weekly_needed)
        assert_false(self.snapshot_manager.is_monthly_needed)

    def test_daily_executed(self):
        self._create_folder(self.snapshot_manager.daily_first, datetime.now())

        assert_false(self.snapshot_manager.is_daily_needed)

    def test_daily_needed(self):
        self._create_folder(self.snapshot_manager.daily_first, datetime.now() - self.snapshot_manager.daily_diff)

        assert_true(self.snapshot_manager.is_daily_needed)

    def test_weekly_first(self):
        today = datetime.now()
        self._create_folder(self.snapshot_manager.daily_first, today - self.snapshot_manager.daily_diff)
        self._create_folder(self.snapshot_manager.daily_last, today - self.snapshot_manager.weekly_diff)

        assert_true(self.snapshot_manager.is_weekly_needed)

    def test_weekly_executed(self):
        today = datetime.now()
        self._create_folder(self.snapshot_manager.daily_last, today)
        self._create_folder(self.snapshot_manager.weekly_first, today - self.snapshot_manager.daily_diff)

        assert_false(self.snapshot_manager.is_weekly_needed)

    def test_weekly_almost_needed(self):
        today = datetime.now()
        self._create_folder(self.snapshot_manager.daily_last, today)
        self._create_folder(self.snapshot_manager.weekly_first, today - self.snapshot_manager.weekly_diff + self.snapshot_manager.daily_diff)

        assert_false(self.snapshot_manager.is_weekly_needed)

    def test_weekly_needed(self):
        today = datetime.now()
        self._create_folder(self.snapshot_manager.daily_last, today)
        self._create_folder(self.snapshot_manager.weekly_first, today - self.snapshot_manager.weekly_diff)

        assert_true(self.snapshot_manager.is_weekly_needed)

    def test_monthly_first(self):
        self._create_folder(self.snapshot_manager.weekly_last, datetime.now())

        assert_true(self.snapshot_manager.is_monthly_needed)

    def test_monthly_executed(self):
        today = datetime.now()
        self._create_folder(self.snapshot_manager.weekly_last, today)
        self._create_folder(self.snapshot_manager.monthly_first, today - self.snapshot_manager.daily_diff)

        assert_false(self.snapshot_manager.is_monthly_needed)

    def test_monthly_almost_needed(self):
        today = datetime.now()
        self._create_folder(self.snapshot_manager.weekly_last, today)
        self._create_folder(self.snapshot_manager.monthly_first, today - self.snapshot_manager.monthly_diff + self.snapshot_manager.daily_diff)

        assert_false(self.snapshot_manager.is_monthly_needed)

    def test_monthly_needed(self):
        today = datetime.now()
        self._create_folder(self.snapshot_manager.weekly_last, today)
        self._create_folder(self.snapshot_manager.monthly_first, today - self.snapshot_manager.monthly_diff)

        assert_true(self.snapshot_manager.is_monthly_needed)


@patch('backup.DefaultSnapshotManager.is_monthly_needed', new_callable=PropertyMock)
@patch('backup.DefaultSnapshotManager.is_weekly_needed', new_callable=PropertyMock)
@patch('backup.DefaultSnapshotManager.is_daily_needed', new_callable=PropertyMock)
class UpcomingTasksTest(TestCase):
    """Test whether return values of upcoming_tasks matches"""

    def _set_return_values(self, mocked_properties):
        """Set return values of given mocks to given value."""
        for mock in mocked_properties:
            mock.return_value = mocked_properties[mock]

    def test_first_backup(self, mock_daily, mock_weekly, mock_monthly):
        self._set_return_values({mock_daily: True, mock_weekly: False, mock_monthly: False})

        tasks = DefaultSnapshotManager().upcoming_tasks
        assert_equals(tasks, {'daily': True, 'weekly': False, 'monthly': False})

    def test_daily_weekly(self, mock_daily, mock_weekly, mock_monthly):
        self._set_return_values({mock_daily: True, mock_weekly: True, mock_monthly: False})

        tasks = DefaultSnapshotManager().upcoming_tasks
        assert_equals(tasks, {'daily': True, 'weekly': True, 'monthly': False})

    def test_full_backup(self, mock_daily, mock_weekly, mock_monthly):
        self._set_return_values({mock_daily: True, mock_weekly: True, mock_monthly: True})

        tasks = DefaultSnapshotManager().upcoming_tasks
        assert_equals(tasks, {'daily': True, 'weekly': True, 'monthly': True})

    def test_weekly_monthly_ignored(self, mock_daily, mock_weekly, mock_monthly):
        self._set_return_values({mock_daily: False, mock_weekly: True, mock_monthly: True})

        tasks = DefaultSnapshotManager().upcoming_tasks
        assert_equals(tasks, {'daily': False, 'weekly': False, 'monthly': False})

    def test_monthly_ignored(self, mock_daily, mock_weekly, mock_monthly):
        self._set_return_values({mock_daily: False, mock_weekly: False, mock_monthly: True})

        tasks = DefaultSnapshotManager().upcoming_tasks
        assert_equals(tasks, {'daily': False, 'weekly': False, 'monthly': False})

    def test_monthly_without_weekly_ignored(self, mock_daily, mock_weekly, mock_monthly):
        self._set_return_values({mock_daily: True, mock_weekly: False, mock_monthly: True})

        tasks = DefaultSnapshotManager().upcoming_tasks
        assert_equals(tasks, {'daily': True, 'weekly': False, 'monthly': False})
