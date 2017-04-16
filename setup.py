# -*- coding: utf-8 -*-
"""setup.py for the taipan project."""
from setuptools import find_packages, setup

setup(
    name='taipan',
    version="1.0",
    packages=find_packages(),
    scripts=['bin/scidentifier'],
    include_package_data=False,
    install_requires=[
        'numpy',
        'agdistispy',
        'SPARQLWrapper'
    ],
)
