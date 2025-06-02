#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
from os.path import join, dirname

setup(
    name='OdooLogParser',
    version="0.0.1",
    description="Log Parser for Odoo logs, including a test digest generator",
    author="João Jerónimo",
    author_email="joao.jeronimo.pro@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        ],
    install_requires=[
        ],
    python_requires='>=3.9',
    extras_require={},
    tests_require=[],
    packages=[
        'odoo_log_parser',
        ],
    scripts=[
        #'Usl-BackupBot.py',
        ],
    )
