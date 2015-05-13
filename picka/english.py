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


import picka_utils as _utils
import name as _name
__docformat__ = 'restructuredtext en'
_max_counts = _utils.row_counts

_query = _utils.query

class NameGenerator(string.Formatter):
    def get_value(self, key, args, kwargs):
        return getattr(_name, key)()


ftr = NameGenerator()


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

