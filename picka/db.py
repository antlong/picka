#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
db adds database support for data generation and randomization to picka.
Testers can create their templates that are indexed to generate test data for
testing new User and other tests where unique entry is necessary.
db supports storing lists of values that can be accessed sequentially or randomly.

Testers can continue testing with less thought on what will be a value for this run.
Those decision can be made when tests are developed and will not interrupt a test session.

By: Bernard Kuehlhorn
"""

from itertools import izip
from functools import partial
import string
import random as _random
import time
import sqlite3
import os
import re
import calendar
import linecache

__docformat__ = 'restructuredtext en'

def pattern_next(pattern, tester,sut):
    """ Return a unique string based on pattern and index stored in db.

    Look up pattern in database using sut and tester to manage different test
    environments and multiple testers.

    If pattern does not exist for tester and sut, it is added with zero index.

    pattern is formated with index to return a unique value.

    :param pattern: String of data to be made unique by index stored in database.
    :param tester:
    :param sut:
    :return: generated test dat
    """
