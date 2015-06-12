#!/usr/bin/env python
# coding=utf-8

from backup import RsnapshotManager
from datetime import datetime
from nose.tools import istest, nottest, with_setup, assert_true, assert_false

import os
import shutil
import tempfile

#
# Test data
#

test_folder = None
backup_manager = None

#
# Test helper
#

@nottest
def set_up_manager():
    global test_folder, backup_manager
    test_folder = tempfile.mkdtemp()
    backup_manager = RsnapshotManager(test_folder)

@nottest
def tear_down_manager():
    shutil.rmtree(test_folder)

@nottest
def create_folder(folder, timestamp):
    os.makedirs(folder)
    os.system('touch -t {time:%Y%m%d%H%M.%S} {file}'.format(time=timestamp, file=folder))

#
# Actual tests
#

@istest
@with_setup(set_up_manager, tear_down_manager)
def test_empty_folder():
    assert_true(backup_manager.is_daily_needed)
    assert_false(backup_manager.is_weekly_needed)
    assert_false(backup_manager.is_monthly_needed)

@istest
@with_setup(set_up_manager, tear_down_manager)
def test_daily_executed():
    create_folder(backup_manager.daily_first, datetime.now())

    assert_false(backup_manager.is_daily_needed)

@istest
@with_setup(set_up_manager, tear_down_manager)
def test_daily_old():
    create_folder(backup_manager.daily_first, datetime.now() - backup_manager.daily_diff)

    assert_true(backup_manager.is_daily_needed)

@istest
@with_setup(set_up_manager, tear_down_manager)
def test_weekly_first():
    create_folder(backup_manager.daily_last, datetime.now())

    assert_true(backup_manager.is_weekly_needed)

@istest
@with_setup(set_up_manager, tear_down_manager)
def test_weekly_executed():
    now = datetime.now()
    create_folder(backup_manager.daily_last, now)
    create_folder(backup_manager.weekly_first, now - backup_manager.daily_diff)

    assert_false(backup_manager.is_weekly_needed)

@istest
@with_setup(set_up_manager, tear_down_manager)
def test_weekly_old():
    now = datetime.now()
    create_folder(backup_manager.daily_last, now)
    create_folder(backup_manager.weekly_first, now - backup_manager.weekly_diff)

    assert_true(backup_manager.is_weekly_needed)

@istest
@with_setup(set_up_manager, tear_down_manager)
def test_monthly_first():
    create_folder(backup_manager.weekly_last, datetime.now())

    assert_true(backup_manager.is_monthly_needed)

@istest
@with_setup(set_up_manager, tear_down_manager)
def test_monthly_executed():
    now = datetime.now()
    create_folder(backup_manager.weekly_last, now)
    create_folder(backup_manager.monthly_first, now - backup_manager.weekly_diff)

    assert_false(backup_manager.is_monthly_needed)

@istest
@with_setup(set_up_manager, tear_down_manager)
def test_monthly_old():
    now = datetime.now()
    create_folder(backup_manager.weekly_last, now)
    create_folder(backup_manager.monthly_first, now - backup_manager.monthly_diff)

    assert_true(backup_manager.is_monthly_needed)
