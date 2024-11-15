#!/usr/bin/env python
"""
Simple, robust features for expediting application logging configuration
"""
import os
import sys
from setuptools import find_packages, setup

NAME = "prolog"
HERE = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(HERE, NAME, "__version__.py")) as f:
    exec(f.read(), about)


long_description = ""
readme = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.rst")
if os.path.exists(readme):
    with open(readme, "r") as f:
        long_description = f.read()

setup(
    name=NAME,
    version=about["__version__"],
    description=__doc__.strip(),
    long_description=long_description,
    author="David Krauth",
    author_email="dakrauth@gmail.com",
    url="https://github.com/dakrauth/prolog",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    license="MIT License",
    entry_points={"console_scripts": ["prolog=prolog.__main__:main"]},
    install_requires=["appdirs>=1.4.3"],
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Topic :: System :: Logging",
        "Topic :: Utilities",
    ],
)
