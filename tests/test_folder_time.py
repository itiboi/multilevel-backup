#!/usr/bin/env python
# coding=utf-8

from backup import folder_time
from datetime import date, datetime, timedelta
from nose.tools import raises

import os
import tempfile
import unittest

class FolderTimeTest(unittest.TestCase):

    _test_dates = (
        (
            datetime(year=2015, month=5, day=23, hour=5, minute=52, second=16),
            date(year=2015, month=5, day=23)
        ),
        (
            datetime(year=1978, month=1, day=23, hour=5, minute=0, second=16),
            date(year=1978, month=1, day=23)
        ),
        (
            datetime.today().replace(hour=20, minute=41, second=42, microsecond=485) + timedelta(days=20),
            date.today() + timedelta(days=20)
        )
    )

    def setUp(self):
        self.test_folder = tempfile.mkdtemp()

    def tearDown(self):
        os.rmdir(self.test_folder)

    @raises(FileNotFoundError)
    def test_non_existing(self):
        folder = os.path.join(self.test_folder, 'non_existing')
        folder_time(folder)

    def _set_time(self, time):
        """Set timestamp to folder."""
        os.system('touch -t {time:%Y%m%d%H%M.%S} {file}'.format(time=time, file=self.test_folder))

    def _test_time(self, test_time, result_time):
        self._set_time(test_time)
        self.assertEqual(result_time, folder_time(self.test_folder))

    def test_time_simple(self):
        test_time = date(year=2015, month=5, day=23)
        self._test_time(test_time, test_time)

    def test_time_complete(self):
        for (test_time, result_time) in self._test_dates:
            self._test_time(test_time, result_time)
