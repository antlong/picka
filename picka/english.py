#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Picka is a data generation and randomization module which aims to increase
coverage by increasing the amount of tests you _dont_ have to write
by hand.
By: Anthony Long
"""

import string
import random as _random
import sqlite3
import os

import picka


__docformat__ = 'restructuredtext en'

connect = \
    sqlite3.connect(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'db.sqlite'))
cursor = connect.cursor()
_max_counts = {}


class NameGenerator(string.Formatter):
    def get_value(self, key, args, kwargs):
        return getattr(picka, key)()


ftr = NameGenerator()


def _get_max(tablename):
    if tablename in _max_counts:
        return _max_counts[tablename]
    cursor.execute('SELECT MAX(_ROWID_) FROM {} LIMIT 1'.format(tablename))
    _max_counts[tablename] = cursor.fetchone()[0]
    return _max_counts[tablename]


def name(formatting="{male} {last}"):
    return ftr.format(formatting)


def initial(with_period=False):
    """
    Returns a randomly chosen letter, with a trailing period if desired.

        :parameters: with_period: (bool)
            Whether or not to add a trailing period.
    """
    letter = _random.choice(string.letters).upper()
    return letter if not with_period else letter + '.'


# todo picka.name(gender or surname)

def female_first():
    """Returns a randomly chosen female first name."""
    cursor.execute('SELECT name FROM female WHERE id =?', [
        _random.randint(1, _get_max("female"))])
    return cursor.fetchone()[0].decode("utf-8")

