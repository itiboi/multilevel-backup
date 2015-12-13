import re


def backup_root_from_config(config):
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


def intervals_from_config(config):
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
