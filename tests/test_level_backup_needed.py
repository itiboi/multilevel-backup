#!/usr/bin/env python
# coding=utf-8

from backup import level_backup_needed
from datetime import datetime, timedelta

import os
import tempfile
import unittest

class LevelBackupNeededTest(unittest.TestCase):

    _min_diffs = (
        timedelta(days=1),
        timedelta(days=5),
        timedelta(days=20)
    )

    _dates_diff_under_min = (
        (
            timedelta(),  # min_diff
            datetime(),   # lower
            datetime(),   # upper
        )
    )

    def setUp(self):
        self.lower_folder = tempfile.mkdtemp()
        self.upper_folder = tempfile.mkdtemp()

    def tearDown(self):
        os.rmdir(self.lower_folder)
        os.rmdir(self.upper_folder)

    def test_non_existing_lower(self):
        non_existing_lower = os.path.join(self.lower_folder, 'lower')
        for min_diff in self._min_diffs:
            self.assertFalse(level_backup_needed(self.upper_folder, non_existing_lower, min_diff))

    def test_non_existing_both(self):
        non_existing_lower = os.path.join(self.lower_folder, 'lower')
        non_existing_upper = os.path.join(self.upper_folder, 'upper')
        for min_diff in self._min_diffs:
            self.assertFalse(level_backup_needed(non_existing_upper, non_existing_lower, min_diff))

    def test_non_existing_upper(self):
        non_existing_upper = os.path.join(self.upper_folder, 'upper')
        for min_diff in self._min_diffs:
            self.assertTrue(level_backup_needed(non_existing_upper, self.lower_folder, min_diff))

    def _set_time(self, folder, time):
        """Set timestamp to folder."""
        os.system('touch -t {time:%Y%m%d%H%M.%S} {file}'.format(time=time, file=folder))

    def test_diff_under_min(self):
        min_diff = max(self._min_diffs) + timedelta(days=1)
        for day_offset in self._min_diffs:
            lower_date = datetime.now() + day_offset
            self._set_time(self.lower_folder, lower_date)
            self.assertFalse(level_backup_needed(self.upper_folder, self.lower_folder, min_diff))

    def test_diff_equals_min(self):
        for day_offset in self._min_diffs:
            lower_date = datetime.now() + day_offset
            self._set_time(self.lower_folder, lower_date)
            self.assertTrue(level_backup_needed(self.upper_folder, self.lower_folder, day_offset))

    def test_diff_over_min(self):
        for day_offset in self._min_diffs:
            lower_date = datetime.now() + day_offset + timedelta(days=5)
            self._set_time(self.lower_folder, lower_date)
            self.assertTrue(level_backup_needed(self.upper_folder, self.lower_folder, day_offset))

    def test_diff_negative(self):
        min_diff = timedelta(days=2)
        for day_offset in self._min_diffs:
            lower_date = datetime.now() - day_offset
            self._set_time(self.lower_folder, lower_date)
            self.assertFalse(level_backup_needed(self.upper_folder, self.lower_folder, min_diff))

    def test_diff_under_day(self):
        pass

    def test_diff_over_day(self):
        pass
