from os import path
from datetime import date


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
