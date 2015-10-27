#!/usr/bin/env python
# coding=utf-8

from argparse import ArgumentParser
from multilevelbackup import DefaultBackupExecutor, perform_backup

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-c', '--config-file', help='config file for rsnapshot to use', required=True)
    parser.add_argument('-d', '--dry-run', help='only show what script would do', action='store_true')
    args = parser.parse_args()

    executor = DefaultBackupExecutor(conf_file=args.config_file, dry_run=args.dry_run)
    perform_backup(backup_executor=executor)
