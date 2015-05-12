#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os
import unittest
from types import *

import picka

connect = \
    sqlite3.connect(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'db.sqlite'))
cursor = connect.cursor()


def test_phone_number():
    n = picka.phone_number()
    assert type(n) is StringType
    assert n[3], n[7] == "-"


def test_last_name():
    name = picka.last_name()
    assert len(name) >= 1
    assert type(name) is UnicodeType, "%s is not a unicode object." % name


def test_random_string():
    s = picka.random_string(8)
    assert len(s) == 8
    assert type(s) is StringType, "%r is not a string."


def test_initial():
    x = picka.initial()
    y = picka.initial(period=True)
    assert "." not in x
    assert len(x) == 1
    assert type(x) is StringType
    assert type(picka.initial(x)) is StringType
    assert y[-1] == "."


def test_sentence():
    assert type(picka.sentence()) is StringType


def test_sentence_actual():
    x = picka.sentence_actual(min_words=3, max_words=3)
    assert len(x.split()) == 3


def test_timezone_offset():
    assert picka.timezone_offset()


def test_rbga():
    assert len(picka.rbga()) == 4
    assert len(picka.rbga(a=255)) == 4
    assert picka.rbga(a=0)[3] == 0
    assert picka.rbga(a=255)[3] == 255


def test_language():
    assert len(picka.language()) > 0

assert picka.timezone_offset_country()
assert picka.screename()
assert picka.number(10)
assert picka.month()
assert picka.month_and_day_and_year()
assert picka.special_characters(8)
assert picka.postal_code()
assert picka.apartment_number()
assert picka.gender()
assert picka.salutation()
assert picka.creditcard('visa')
assert picka.male_middle_name()
assert picka.city()
assert picka.male_full_name_w_middle_initial()
assert picka.state_abbreviated()
assert picka.street_name()
assert picka.initial()
assert picka.calling_code_with_country()
assert picka.surname()
assert picka.business_title()
assert picka.male_middle()
assert picka.trash(picka.male_first)
assert picka.female_first()
assert picka.calling_code()
assert picka.male_first()
assert picka.timestamp()
assert picka.hyphenated_last_name()
assert picka.fax_number()
assert picka.male_full_name()
assert picka.password_alphanumeric(8)
#assert picka.birthday()
assert picka.social_security_number()
assert picka.set_of_initials()
assert picka.female_middle()
assert picka.month_and_day()
assert picka.password_alphabetical(8)
assert picka.name()
assert picka.cvv(3)
assert picka.country()
assert picka.age()
assert picka.city_with_state()
assert picka.email()
assert picka.female_name()
assert picka.street_type()
assert picka.suffix()
assert picka.url(10)
assert picka.password_numerical(10)
assert picka.street_address()
assert picka.language()
assert len(picka.barcode("EAN-8")) == 8


def test_barcode():
    x = picka.barcode("EAN-13")
    assert len(x) == 13

# assert picka.locale()
assert picka.mime_type()

if __name__ == '__main__':
    unittest.main()