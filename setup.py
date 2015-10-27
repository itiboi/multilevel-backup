#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='multilevel-backup',
    version='0.1.0',
    packages=find_packages(),
    scripts=['bin/backup.py'],
    author='Tim Bolender',
    author_email='contact@timbolender.de',
    url='',
    license='',
    description='Python wrapper around rsnapshot which simplifies a multi-level backup setup'
)
