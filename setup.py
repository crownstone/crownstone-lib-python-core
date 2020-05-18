#!/usr/bin/env python3

from setuptools import setup, find_packages


print(find_packages(exclude=[]))

setup(
    name='crownstone-lib-python-core',
    version='0.0.0',
    packages=find_packages(exclude=[]),
    install_requires=list(package.strip() for package in open('requirements.txt')),
    classifiers=[
        'Programming Language :: Python :: 3.7'
    ]
)