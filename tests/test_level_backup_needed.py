#!/usr/bin/env python
# coding=utf-8

from multilevelbackup.helpers import level_backup_needed
from datetime import datetime, timedelta

import os
import pytest

#
# Test data
#

example_deltas = [
    timedelta(days=1),
    timedelta(days=5),
    timedelta(days=20)
]

#
# Test helper
#


@pytest.fixture(scope='function')
def lower_folder(tmpdir):
    return str(tmpdir.mkdir('lower'))


@pytest.fixture(scope='function')
def upper_folder(tmpdir):
    return str(tmpdir.mkdir('upper'))


def backup_needed(lower_folder, upper_folder, delta, lower_date, upper_date):
    """Set timestamp to folder and checks whether function result matches given result."""
    os.system('touch -t {time:%Y%m%d%H%M.%S} {file}'.format(time=lower_date, file=lower_folder))
    os.system('touch -t {time:%Y%m%d%H%M.%S} {file}'.format(time=upper_date, file=upper_folder))
    return level_backup_needed(upper_folder, lower_folder, delta)

#
# Actual tests
#


@pytest.mark.parametrize('delta', example_deltas)
def test_non_existing_lower(lower_folder, upper_folder, delta):
    non_existing_lower = os.path.join(lower_folder, 'lower')
    assert not level_backup_needed(upper_folder, non_existing_lower, delta)


@pytest.mark.parametrize('delta', example_deltas)
def test_non_existing_upper(lower_folder, upper_folder, delta):
    non_existing_upper = os.path.join(upper_folder, 'upper')
    assert level_backup_needed(non_existing_upper, lower_folder, delta)


@pytest.mark.parametrize('delta', example_deltas)
def test_non_existing_both(lower_folder, upper_folder, delta):
    non_existing_lower = os.path.join(lower_folder, 'lower')
    non_existing_upper = os.path.join(upper_folder, 'upper')
    assert not level_backup_needed(non_existing_upper, non_existing_lower, delta)


@pytest.mark.parametrize('delta, lower_date, upper_date', [
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
])
def test_delta_under_min(lower_folder, upper_folder, delta, lower_date, upper_date):
    assert not backup_needed(lower_folder, upper_folder, delta, lower_date, upper_date)


@pytest.mark.parametrize('delta, lower_date, upper_date', [
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
])
def test_delta_equals_min(lower_folder, upper_folder, delta, lower_date, upper_date):
    assert backup_needed(lower_folder, upper_folder, delta, lower_date, upper_date)


@pytest.mark.parametrize('delta, lower_date, upper_date', [
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
])
def test_delta_over_min(lower_folder, upper_folder, delta, lower_date, upper_date):
    assert backup_needed(lower_folder, upper_folder, delta, lower_date, upper_date)


@pytest.mark.parametrize('day_offset', example_deltas)
def test_delta_negative(lower_folder, upper_folder, day_offset):
    delta = timedelta(days=2)
    now = datetime.now()
    date_before = now - day_offset
    assert not backup_needed(lower_folder, upper_folder, delta, date_before, now)


@pytest.mark.parametrize('delta, lower_date, upper_date', [
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
])
def test_delta_under_full_day(lower_folder, upper_folder, delta, lower_date, upper_date):
    assert backup_needed(lower_folder, upper_folder, delta, lower_date, upper_date)
