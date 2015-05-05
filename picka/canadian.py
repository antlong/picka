#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Picka is a data generation and randomization module which aims to increase
coverage by increasing the amount of tests you _dont_ have to write
by hand.
By: Anthony Long
"""

import random as _random
import sqlite3 as _sqlite3
import os as _os

_connect = \
    _sqlite3.connect(_os.path.join(_os.path.abspath(
        _os.path.dirname(__file__)), 'db.sqlite'))
_connect.text_factory = str
_cursor = _connect.cursor()
_max_counts = {}


def _get_max(tablename):
    if tablename in _max_counts:
        return _max_counts[tablename]
    _cursor.execute('SELECT MAX(_ROWID_) FROM {} LIMIT 1'.format(tablename))
    _max_counts[tablename] = _cursor.fetchone()[0]
    return _max_counts[tablename]


def direction(abbreviated=True):
    if abbreviated:
        _cursor.execute('SELECT abbreviated from ca_directions where id = ?', [
            _random.randint(1, _get_max("ca_directions"))])
    else:
        _cursor.execute('SELECT full from ca_directions where id = ?', [
            _random.randint(1, _get_max("ca_directions"))])
    return _cursor.fetchone().decode("utf-8")


def street_name():
    _cursor.execute('SELECT name FROM ca_street_names where id =?', [
        _random.randint(1, _get_max("ca_street_names"))])
    return _cursor.fetchone()[0].decode("utf-8")


def street_type(abbreviated=True):
    """Returns a Canadian street type."""
    if abbreviated:
        _cursor.execute('SELECT abbreviated from ca_street_types where id = ?', [
            _random.randint(1, _get_max("ca_streets"))])
    else:
        _cursor.execute('SELECT full from ca_street_types where id = ?', [
            _random.randint(1, _get_max("ca_street_types"))])
    return _cursor.fetchone()[0].decode("utf-8")


def province():
    """Returns a list, full name and postal abbreviation"""
    return _random.choice(
        [
            ["Ontario", "ON"],
            ["Quebec", "QC"],
            ["Nova Scotia", "NS"],
            ["New Brunswick", "NB"],
            ["Manitoba", "MB"],
            ["British Columbia", "BC"],
            ["Prince Edward Island", "PE"],
            ["Saskatchewan", "SK"],
            ["Alberta", "AB"],
            ["Newfoundland and Labrador", "NL"]
        ]
    )


def town():
    _cursor.execute('SELECT name from ca_towns where id = ?', [
        _random.randint(1, _get_max("ca_towns"))])
    return _cursor.fetchone()[0]


def postal():
    """Returns a valid postal code"""
    _cursor.execute('SELECT code from ca_postal_codes where id = ?', [
        _random.randint(1, _get_max("ca_postal_codes"))])
    return _cursor.fetchone()[0]


def city():
    """Returns a valid Canadian city"""
    _cursor.execute('SELECT name FROM ca_cities where id =?', [
        _random.randint(1, _get_max("ca_cities"))])
    return _cursor.fetchone()[0].decode("utf-8")


def lat_long():
    _cursor.execute('SELECT lat,long from ca_lat_and_longs \
        where id = ?', [_random.randint(1, _get_max("ca_cities"))])
    return _cursor.fetchone()
