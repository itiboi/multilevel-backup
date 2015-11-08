#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='multilevel-backup',
    version='0.1.0',
    packages=find_packages(),
    scripts=['bin/multilevel-backup'],
    author='Tim Bolender',
    author_email='contact@timbolender.de',
    url='https://github.com/itiboi/multilevel-backup',
    license='',
    description='Simplifies the management of a multi-level backup structure with rsnapshot especially for not'
                'always-on devices.'
)
