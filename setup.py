#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from setuptools import find_packages, setup

long_description = ''
readme = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.rst')
if os.path.exists(readme):
    with open(readme, 'r') as f:
        long_description = f.read()

VERSION = __import__('prolog').get_version()

setup(
    name='prolog,
    version=VERSION,
    description='',
    long_description=long_description,
    author=David Krauth',
    author_email='dakrauth@gmail.com',
    url='https://github.com/dakrauth/prolog',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    license='MIT License',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
