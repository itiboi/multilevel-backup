#!/usr/bin/env python
# coding=utf-8

from rsnapshotbackup import _folder_time
from datetime import date, datetime, timedelta

import os
import pytest

#
# Test helper
#


def check_time(folder, test_time, result_time):
    os.system('touch -t {time:%Y%m%d%H%M.%S} {file}'.format(time=test_time, file=folder))
    assert result_time == _folder_time(folder)

#
# Actual tests
#


@pytest.mark.xfail(raises=FileNotFoundError)
def test_non_existing(tmpdir):
    test_folder = str(tmpdir.join('non_existing'))
    _folder_time(test_folder)


@pytest.mark.parametrize("test_time, result_time", [
    (
        datetime(year=2015, month=5, day=23),
        date(year=2015, month=5, day=23)
    ),
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
])
def test_time_simple(tmpdir, test_time, result_time):
    test_folder = str(tmpdir)
    check_time(test_folder, test_time, result_time)
