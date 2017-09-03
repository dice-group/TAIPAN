# -*- coding: utf-8 -*-
"""setup.py for the taipan project."""
from setuptools import find_packages, setup

setup(
    name='taipan',
    version="1.0.1",
    packages=find_packages(),
    scripts=[
        'bin/scidentifier',
        'bin/propertyrecommender'
    ],
    include_package_data=False,
    install_requires=[
        'numpy',
        'agdistispy',
        'SPARQLWrapper',
        'rdflib',
        'scipy',
        'scikit-learn',
        'foxpy',
        'python-dateutil'
    ],
)
