#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='Rev API Client',
      version='1.0',
      description='Rev Transcription Client - order transcripts and view status',
      author='Koemei',
      author_email='dev@koemei.com',
      url='https://www.koemei.com',
      packages=['rev'],
      license='Apache License 2.0',
      keywords='Rev transcription api Koemei',
      install_requires=[
          "requests >=2.0.0"
      ],
 )
