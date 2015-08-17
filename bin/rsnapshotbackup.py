#!/usr/bin/env python
# coding=utf-8

from argparse import ArgumentParser
from rsnapshotbackup import DefaultBackupExecutor, perform_backup

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--dry-run', help='Only show what script would do', action='store_true')
    args = parser.parse_args()

    executor = DefaultBackupExecutor(dry_run=args.dry_run)
    perform_backup(backup_executor=executor)
