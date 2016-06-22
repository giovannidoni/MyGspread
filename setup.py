#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='SCLgspread',
    version='0.0.00',
    description='Wrapper to write and read DataFrames in googledocs using gspread',
    author='Giovanni Doni',
    install_requires=['pandas', 'gspread', 'oauth2client'],
    packages=find_packages(),
    include_package_data=True
)
