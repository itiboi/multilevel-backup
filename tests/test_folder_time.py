#!/usr/bin/env python
# coding=utf-8

from backup import folder_time
from datetime import date, datetime, timedelta
from nose.tools import istest, nottest, with_setup, raises, assert_equals

import os
import tempfile

#
# Test data
#

test_folder = None

test_dates = (
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

#
# Test helper
#

@nottest
def set_up_folder():
    global test_folder
    test_folder = tempfile.mkdtemp()

@nottest
def tear_down_folder():
    os.rmdir(test_folder)

@nottest
def set_time(time):
    """Set timestamp to folder."""
    os.system('touch -t {time:%Y%m%d%H%M.%S} {file}'.format(time=time, file=test_folder))

@nottest
def check_time(test_time, result_time):
    set_time(test_time)
    assert_equals(result_time, folder_time(test_folder))

#
# Actual tests
#

@istest
@raises(FileNotFoundError)
@with_setup(set_up_folder, tear_down_folder)
def test_non_existing():
    folder = os.path.join(test_folder, 'non_existing')
    folder_time(folder)

@istest
@with_setup(set_up_folder, tear_down_folder)
def test_time_simple():
    test_time = date(year=2015, month=5, day=23)
    check_time(test_time, test_time)

@istest
@with_setup(set_up_folder, tear_down_folder)
def test_time_full():
    for (test_time, result_time) in test_dates:
        yield check_time, test_time, result_time
