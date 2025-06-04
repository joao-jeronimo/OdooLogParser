#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
from os.path import join, dirname

setup(
    packages=[
        'odoo_log_parser',
        ],
    scripts=[
        'Odoo-LogParser.py',
        ],
    )
