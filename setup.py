from os import path

import foregrox
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='foreground_extraction',
    version=foregrox.__version__,
    description='Foreground extraction.',
    long_description=long_description,
    packages=find_packages(),
    test_suite='test'
)
