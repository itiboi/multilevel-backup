#!/usr/bin/env python
# coding=utf-8

from backup import level_backup_needed
from datetime import datetime, timedelta
from nose.tools import istest, nottest, with_setup, assert_true, assert_false, assert_equals

import os
import tempfile

_lower_folder = None
_upper_folder = None

_example_deltas = (
    timedelta(days=1),
    timedelta(days=5),
    timedelta(days=20)
)

# (delta, lower, upper)
_dates_delta_under_min = (
    (
        timedelta(days=5),
        datetime(year=2015, month=5, day=19),
        datetime(year=2015, month=5, day=15),
    ),
    (
        timedelta(days=20),
        datetime(year=2015, month=8, day=13),
        datetime(year=2015, month=7, day=25),
    ),
    (
        timedelta(days=12),
        datetime(year=2016, month=1, day=7),
        datetime(year=2015, month=12, day=28),
    )
)

# (delta, lower, upper)
_dates_delta_equals_min = (
    (
        timedelta(days=5),
        datetime(year=2015, month=3, day=20),
        datetime(year=2015, month=3, day=15),
    ),
    (
        timedelta(days=20),
        datetime(year=2015, month=11, day=14),
        datetime(year=2015, month=10, day=25),
    ),
    (
        timedelta(days=12),
        datetime(year=2016, month=1, day=10),
        datetime(year=2015, month=12, day=29),
    )
)

# (delta, lower, upper)
_dates_delta_over_min = (
    (
        timedelta(days=5),
        datetime(year=2015, month=2, day=27),
        datetime(year=2015, month=2, day=19),
    ),
    (
        timedelta(days=20),
        datetime(year=2015, month=4, day=15),
        datetime(year=2015, month=3, day=10),
    ),
    (
        timedelta(days=12),
        datetime(year=2016, month=1, day=17),
        datetime(year=2015, month=12, day=21),
    )
)

# (delta, lower, upper)
_dates_delta_under_full_day = (
    (
        timedelta(days=5),
        datetime(year=2015, month=3, day=20, hour=14, minute=4),
        datetime(year=2015, month=3, day=15, hour=23, minute=26),
    ),
    (
        timedelta(days=20),
        datetime(year=2015, month=11, day=14, hour=2, minute=25),
        datetime(year=2015, month=10, day=25, hour=10, minute=38),
    ),
    (
        timedelta(days=12),
        datetime(year=2016, month=1, day=10, hour=6, minute=4),
        datetime(year=2015, month=12, day=29, hour=6, minute=58),
    )
)

@nottest
def set_up_folder():
    global _lower_folder, _upper_folder
    _lower_folder = tempfile.mkdtemp()
    _upper_folder = tempfile.mkdtemp()

@nottest
def tear_down_folder():
    os.rmdir(_lower_folder)
    os.rmdir(_upper_folder)

def _set_time(folder, time):
    """Set timestamp to folder."""
    os.system('touch -t {time:%Y%m%d%H%M.%S} {file}'.format(time=time, file=folder))

def _check_delta(result, delta, lower, upper):
    """Set timestamp to folder and checks whether function result matches given result."""
    _set_time(_lower_folder, lower)
    _set_time(_upper_folder, upper)
    assert_equals(result, level_backup_needed(_upper_folder, _lower_folder, delta))

@istest
@with_setup(set_up_folder, tear_down_folder)
def test_non_existing_lower():
    non_existing_lower = os.path.join(_lower_folder, 'lower')
    for delta in _example_deltas:
        assert_false(level_backup_needed(_upper_folder, non_existing_lower, delta))

@istest
@with_setup(set_up_folder, tear_down_folder)
def test_non_existing_upper():
    non_existing_upper = os.path.join(_upper_folder, 'upper')
    for delta in _example_deltas:
        assert_true(level_backup_needed(non_existing_upper, _lower_folder, delta))

@istest
@with_setup(set_up_folder, tear_down_folder)
def test_non_existing_both():
    non_existing_lower = os.path.join(_lower_folder, 'lower')
    non_existing_upper = os.path.join(_upper_folder, 'upper')
    for delta in _example_deltas:
        assert_false(level_backup_needed(non_existing_upper, non_existing_lower, delta))

@istest
@with_setup(set_up_folder, tear_down_folder)
def test_delta_under_min():
    for (delta, lower, upper) in _dates_delta_under_min:
        yield _check_delta, False, delta, lower, upper

@istest
@with_setup(set_up_folder, tear_down_folder)
def test_delta_equals_min():
    for (delta, lower, upper) in _dates_delta_equals_min:
        yield _check_delta, True, delta, lower, upper

@istest
@with_setup(set_up_folder, tear_down_folder)
def test_delta_over_min():
    for (delta, lower, upper) in _dates_delta_over_min:
        yield _check_delta, True, delta, lower, upper

@istest
@with_setup(set_up_folder, tear_down_folder)
def test_delta_negative():
    delta = timedelta(days=2)
    now = datetime.now()
    for day_offset in _example_deltas:
        lower_date = now - day_offset
        yield _check_delta, False, delta, lower_date, now

@istest
@with_setup(set_up_folder, tear_down_folder)
def test_delta_under_full_day():
    for (delta, lower, upper) in _dates_delta_under_full_day:
        yield _check_delta, True, delta, lower, upper
