from multilevelbackup import DefaultBackupExecutor

import pytest


#
# Test helper
#


rsnapshot_conf_file = 'strange/folder/with/rsnapshot.conf'


@pytest.fixture(scope='function', params=[False, True], ids=['normal', 'dry'])
def backup_executor(request):
    return DefaultBackupExecutor(conf_file=rsnapshot_conf_file, dry_run=request.param), request.param


@pytest.fixture(scope='function')
def mock_call_process(mocker):
    return mocker.patch('subprocess.check_call')


def get_call_from_mock(mock_call_process):
    """:return Process call passed to mock as single string."""
    pos_args, keyword_args = mock_call_process.call_args
    program_call = pos_args[0] if pos_args is not None else keyword_args['args']
    return ' '.join(program_call)


def check_call(full_call, dry_run):
    """Check whether process call contains all basic arguments."""
    assert full_call.startswith('rsnapshot')
    assert full_call.find('-c ' + rsnapshot_conf_file) != -1
    if dry_run:
        assert full_call.find('-t') != -1
    else:
        assert full_call.find('-t') == -1


#
# Actual tests
#


def test_perform_sync(backup_executor, mock_call_process):
    executor, dry_run = backup_executor
    executor.perform_sync()

    full_call = get_call_from_mock(mock_call_process)
    check_call(full_call, dry_run=dry_run)
    assert full_call.find('sync') != -1


def test_perform_daily(backup_executor, mock_call_process):
    executor, dry_run = backup_executor
    executor.perform_daily()

    full_call = get_call_from_mock(mock_call_process)
    check_call(full_call, dry_run=dry_run)
    assert full_call.find('daily') != -1


def test_perform_weekly(backup_executor, mock_call_process):
    executor, dry_run = backup_executor
    executor.perform_weekly()

    full_call = get_call_from_mock(mock_call_process)
    check_call(full_call, dry_run=dry_run)
    assert full_call.find('weekly') != -1


def test_perform_monthly(backup_executor, mock_call_process):
    executor, dry_run = backup_executor
    executor.perform_monthly()

    full_call = get_call_from_mock(mock_call_process)
    check_call(full_call, dry_run=dry_run)
    assert full_call.find('monthly') != -1
