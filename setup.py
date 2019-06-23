from os import path
from setuptools import setup, find_packages

import lib

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
   long_description = f.read()

setup(
   name='foreground-extraction',
   version=lib.__version__,
   description='Foreground extraction.',
   long_description=long_description,
   packages=find_packages(),
   test_suite='test'
)
