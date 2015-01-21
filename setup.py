#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" install corpus-creator """
from setuptools import setup, find_packages

from sys import exit

setup(
      ###########################################
      ## Metadata
      name="corpus_creator",
      version="0.0.1",
      description='corpus_creator',
      author='Albert Weichselbraun',
      author_email='albert.weichselbraun@htwchur.ch',
      url='https://github.com/AlbertWeichselbraun/corpus-creator',
      license="GPL3",
      package_dir={'': 'src'},

      ###########################################
      ## Run unittests
      test_suite='nose.collector',

      ###########################################
      ## Package List
      packages = find_packages('src'),

)
