#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='picka',
    version='0.9.4',
    description='Picka generates data for use in any application.',
    author='Anthony Long',
    author_email='antlong@gmail.com',
    packages=['picka'],
    url='http://antlong.com',
    package_data={'picka': ['*.sqlite', 'book_sherlock.txt']},
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python'],
    )

