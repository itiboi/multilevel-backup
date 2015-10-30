from multilevelbackup.helpers import backup_root_from_rsnapshot_config, intervals_from_rsnapshot_config

import pytest


def test_backup_root_missing():
    with pytest.raises(ValueError) as excinfo:
        backup_root_from_rsnapshot_config('')
    assert 'snapshot_root' in str(excinfo.value)


def test_backup_root():
    assert backup_root_from_rsnapshot_config('snapshot_root\t/just/a/little/test') == '/just/a/little/test'
    assert backup_root_from_rsnapshot_config('snapshot_root\t\t/other/test') == '/other/test'

    minimal_config = open('tests/rsnapshot-minimal.conf').read()
    assert backup_root_from_rsnapshot_config(minimal_config) == '/rsnapshot/minimal/config/root/'


def test_intervals():
    assert intervals_from_rsnapshot_config('retain\ttest\t6') == {'test': 6}
    assert intervals_from_rsnapshot_config('retain\ttest\t6\nretain\tnext\t2') == {'test': 6, 'next': 2}

    minimal_config = open('tests/rsnapshot-minimal.conf').read()
    assert intervals_from_rsnapshot_config(minimal_config) == {'first': 8, 'sec': 9, 'other': 10}

