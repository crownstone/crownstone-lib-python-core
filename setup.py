#!/usr/bin/env python3

from setuptools import setup, find_packages


print(find_packages(exclude=[]))

setup(
    name='crownstone-lib-python-core',
    version='0.0.0',
    packages=find_packages(exclude=[]),
    install_requires=[]
)