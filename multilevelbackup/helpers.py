from os import path
from datetime import date

import re


def folder_time(folder):
    """
    Get day timestamp of a folder as date.

    :rtype datetime.date
    """
    stamp = path.getmtime(folder)
    return date.fromtimestamp(stamp)


def level_backup_needed(upper_first, lower_last, min_diff):
    """
    Check whether backup of this increment level is needed.

    :rtype bool
    """
    if not path.exists(lower_last):
        return False

    if path.exists(upper_first):
        # Only perform if enough time passed
        time_upper = folder_time(upper_first)
        time_lower = folder_time(lower_last)
        return (time_lower - time_upper) >= min_diff
    else:
        # First backup of higher level
        return True


def backup_root_from_rsnapshot_config(config):
    """
    Determine backup root from rsnapshot config.

    :return Backup root path
    :rtype str
    :raise ValueError: Raised if no backup root could be found
    """

    root_pattern = r'^snapshot_root\t+(?P<root>.+)$'

    match = re.search(root_pattern, config, re.MULTILINE)
    if match:
        return match.group('root')
    else:
        raise ValueError('No \'snapshot_root\' in rsnapshot config found')


def intervals_from_rsnapshot_config(config):
    """
    Determine intervals and their respective retaining count from rsnapshot config.

    :param config: Rsnapshot config file content
    :type config: str

    :return Interval names and their counts
    :rtype dict[str, int]
    :raise ValueError: Raised if no intervals could be found
    """

    retain_pattern = r'^retain\t+(?P<name>\w+)\t+(?P<count>\d+)$'

    intervals = {}
    for match in re.finditer(retain_pattern, config, re.MULTILINE):
        name = match.group('name')
        count = int(match.group('count'))
        intervals[name] = count

    if not intervals:
        raise ValueError('No backup intervals in rsnapshot config found')

    return intervals
