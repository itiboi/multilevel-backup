from multilevelbackup import DefaultSnapshotManager
from datetime import datetime
from unittest.mock import PropertyMock

import os
import pytest


#
# Test helper
#


@pytest.fixture(scope='function')
def snapshot_manager(tmpdir):
    return DefaultSnapshotManager(backup_root=str(tmpdir))


def create_folder(folder, timestamp):
    """Create folder with given timestamp."""
    os.makedirs(folder)
    os.system('touch -t {time:%Y%m%d%H%M.%S} {file}'.format(time=timestamp, file=folder))


@pytest.fixture(scope='function')
def mock_daily(mocker):
    return mocker.patch('multilevelbackup.DefaultSnapshotManager.is_daily_needed', new_callable=PropertyMock)


@pytest.fixture(scope='function')
def mock_weekly(mocker):
    return mocker.patch('multilevelbackup.DefaultSnapshotManager.is_weekly_needed', new_callable=PropertyMock)


@pytest.fixture(scope='function')
def mock_monthly(mocker):
    return mocker.patch('multilevelbackup.DefaultSnapshotManager.is_monthly_needed', new_callable=PropertyMock)


def mock_return_values(mocked_properties):
    """Set return values of given mocks to given value."""
    for mock in mocked_properties:
        mock.return_value = mocked_properties[mock]

#
# Actual level indicator tests
#


def test_indicator_empty_folder(snapshot_manager):
    assert snapshot_manager.is_daily_needed
    assert not snapshot_manager.is_weekly_needed
    assert not snapshot_manager.is_monthly_needed


def test_indicator_daily_executed(snapshot_manager):
    create_folder(snapshot_manager.daily_first, datetime.now())

    assert not snapshot_manager.is_daily_needed


def test_indicator_daily_needed(snapshot_manager):
    create_folder(snapshot_manager.daily_first, datetime.now() - snapshot_manager.daily_diff)

    assert snapshot_manager.is_daily_needed


def test_indicator_weekly_first(snapshot_manager):
    today = datetime.now()
    create_folder(snapshot_manager.daily_first, today - snapshot_manager.daily_diff)
    create_folder(snapshot_manager.daily_last, today - snapshot_manager.weekly_diff)

    assert snapshot_manager.is_weekly_needed


def test_indicator_weekly_executed(snapshot_manager):
    today = datetime.now()
    create_folder(snapshot_manager.daily_last, today)
    create_folder(snapshot_manager.weekly_first, today - snapshot_manager.daily_diff)

    assert not snapshot_manager.is_weekly_needed


def test_indicator_weekly_almost_needed(snapshot_manager):
    today = datetime.now()
    create_folder(snapshot_manager.daily_last, today)
    create_folder(snapshot_manager.weekly_first, today - snapshot_manager.weekly_diff + snapshot_manager.daily_diff)

    assert not snapshot_manager.is_weekly_needed


def test_indicator_weekly_needed(snapshot_manager):
    today = datetime.now()
    create_folder(snapshot_manager.daily_last, today)
    create_folder(snapshot_manager.weekly_first, today - snapshot_manager.weekly_diff)

    assert snapshot_manager.is_weekly_needed


def test_indicator_monthly_first(snapshot_manager):
    create_folder(snapshot_manager.weekly_last, datetime.now())

    assert snapshot_manager.is_monthly_needed


def test_indicator_monthly_executed(snapshot_manager):
    today = datetime.now()
    create_folder(snapshot_manager.weekly_last, today)
    create_folder(snapshot_manager.monthly_first, today - snapshot_manager.daily_diff)

    assert not snapshot_manager.is_monthly_needed


def test_indicator_monthly_almost_needed(snapshot_manager):
    today = datetime.now()
    create_folder(snapshot_manager.weekly_last, today)
    create_folder(snapshot_manager.monthly_first, today - snapshot_manager.monthly_diff + snapshot_manager.daily_diff)

    assert not snapshot_manager.is_monthly_needed


def test_indicator_monthly_needed(snapshot_manager):
    today = datetime.now()
    create_folder(snapshot_manager.weekly_last, today)
    create_folder(snapshot_manager.monthly_first, today - snapshot_manager.monthly_diff)

    assert snapshot_manager.is_monthly_needed


#
# Actual upcoming tasks tests
#


def test_upcoming_first_backup(mock_daily, mock_weekly, mock_monthly):
    mock_return_values({mock_daily: True, mock_weekly: False, mock_monthly: False})

    tasks = DefaultSnapshotManager(backup_root='').upcoming_tasks
    assert tasks == {'daily': True, 'weekly': False, 'monthly': False}


def test_upcoming_daily_weekly(mock_daily, mock_weekly, mock_monthly):
    mock_return_values({mock_daily: True, mock_weekly: True, mock_monthly: False})

    tasks = DefaultSnapshotManager(backup_root='').upcoming_tasks
    assert tasks == {'daily': True, 'weekly': True, 'monthly': False}


def test_upcoming_full_backup(mock_daily, mock_weekly, mock_monthly):
    mock_return_values({mock_daily: True, mock_weekly: True, mock_monthly: True})

    tasks = DefaultSnapshotManager(backup_root='').upcoming_tasks
    assert tasks == {'daily': True, 'weekly': True, 'monthly': True}


def test_upcoming_weekly_monthly_ignored(mock_daily, mock_weekly, mock_monthly):
    mock_return_values({mock_daily: False, mock_weekly: True, mock_monthly: True})

    tasks = DefaultSnapshotManager(backup_root='').upcoming_tasks
    assert tasks == {'daily': False, 'weekly': False, 'monthly': False}


def test_upcoming_monthly_ignored(mock_daily, mock_weekly, mock_monthly):
    mock_return_values({mock_daily: False, mock_weekly: False, mock_monthly: True})

    tasks = DefaultSnapshotManager(backup_root='').upcoming_tasks
    assert tasks == {'daily': False, 'weekly': False, 'monthly': False}


def test_upcoming_monthly_without_weekly_ignored(mock_daily, mock_weekly, mock_monthly):
    mock_return_values({mock_daily: True, mock_weekly: False, mock_monthly: True})

    tasks = DefaultSnapshotManager(backup_root='').upcoming_tasks
    assert tasks == {'daily': True, 'weekly': False, 'monthly': False}


def test_create_from_config():
    manager = DefaultSnapshotManager.create_from_rsnapshot_conf('tests/rsnapshot-minimal.conf')

    assert manager.daily_first == '/rsnapshot/minimal/config/root/daily.0'
    assert manager.daily_last == '/rsnapshot/minimal/config/root/daily.5'
    assert manager.weekly_first == '/rsnapshot/minimal/config/root/weekly.0'
    assert manager.weekly_last == '/rsnapshot/minimal/config/root/weekly.6'
    assert manager.monthly_first == '/rsnapshot/minimal/config/root/monthly.0'


def test_create_from_config_faulty():
    with pytest.raises(ValueError) as excinfo:
        manager = DefaultSnapshotManager.create_from_rsnapshot_conf('tests/rsnapshot-minimal-faulty.conf')
    assert 'interval' in str(excinfo.value)
