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

import picka


_connect = \
    _sqlite3.connect(_os.path.join(_os.path.abspath(
        _os.path.dirname(__file__)), 'canadian.sqlite'))
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
        _cursor.execute('SELECT abbreviated FROM directions WHERE id = ?', [
            _random.randint(1, _get_max("directions"))])
    else:
        _cursor.execute('SELECT "full" FROM directions WHERE id = ?', [
            _random.randint(1, _get_max("directions"))])
    return _cursor.fetchone()[0]


def street_name():
    _cursor.execute('SELECT name FROM street_names WHERE id =?', [
        _random.randint(1, _get_max("street_names"))])
    return _cursor.fetchone()[0].decode("utf-8")


def street_type(abbreviated=True):
    """Returns a Canadian street type."""
    if abbreviated:
        _cursor.execute('SELECT abbreviated FROM street_types WHERE id = ?', [
            _random.randint(1, _get_max("street_types"))])
    else:
        _cursor.execute('SELECT "full" FROM street_types WHERE id = ?', [
            _random.randint(1, _get_max("street_types"))])
    return _cursor.fetchone()[0].decode("utf-8")


def province():
    """Returns a list, full name and postal abbreviation"""
    _cursor.execute('SELECT abbreviation,en_name,fr_name FROM provinces WHERE id = ?', [
        _random.randint(1, _get_max("provinces"))])
    return _cursor.fetchone()


def town():
    _cursor.execute('SELECT name FROM towns WHERE id = ?', [
        _random.randint(1, _get_max("towns"))])
    return _cursor.fetchone()[0]


def postal(separator=False):
    """Returns a valid postal code"""
    _cursor.execute('SELECT code FROM postal_codes WHERE id = ?', [
        _random.randint(1, _get_max("postal_codes"))])
    code = _cursor.fetchone()[0]
    return code[:3] + str(separator) + code[3:] if separator else code


def city():
    """Returns a valid Canadian city"""
    _cursor.execute('SELECT name FROM cities WHERE id =?', [
        _random.randint(1, _get_max("cities"))])
    return _cursor.fetchone()[0].decode("utf-8")


def lat_long():
    _cursor.execute('SELECT lat,long FROM lat_and_longs \
        WHERE id = ?', [_random.randint(1, _get_max("lat_and_longs"))])
    return _cursor.fetchone()


def mailing_address():
    """Generate a mailing address in many formats.

    format 1:
        First line: The Addressee
        Second-last line: Civic Address
        Last line: Municipality Name, Province or Territory and Postal Code
    """
    data = {
        "first_line": picka.male_full_name(),
        "second_line": "%s %s %s" % (_random.randint(1, 9999), street_name(), street_type(False))
    }
    return data