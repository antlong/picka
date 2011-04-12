"""
Picka is a data generation and randomization module which aims to increase
coverage by increasing the amount of tests you _dont_ have to write
by hand.
By: Anthony Long
"""
import sqlite3
import functools
import os
import random
__docformat__ = "restructuredtext en"
connect = sqlite3.connect(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db.sqlite'))
cursor = connect.cursor()

_QUERIES = {
    "albanian_male_names": "select male from albanian where male is not null;",
    "albanian_female_names": "select female from albanian where female is not null;",
    "albanian_surnames": "select surname from albanian where surname is not null;",
}


class _memoized(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            return self.func(*args)
    
    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__
    
    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


@_memoized
def _query(sql):
    cursor.execute(sql)
    return cursor.fetchall()


def age(min=1, max=99):
    return random.randint(min, max + 1)


def apartment_number():
    pass


def business_title():
    pass


def calling_code():
    pass


def calling_code_with_country():
    pass


def city():
    pass


def city_with_state():
    pass


def country():
    pass


def creditcard():
    pass


def cvv():
    pass


def email():
    pass


def fax_number():
    pass


def female_name():
    return random.choice(_query(_QUERIES['albanian_female_names']))[0]


def trash():
    pass


def male_full_name():
    return random.choice(_query(_QUERIES['albanian_male_names']))[0] + random.choice(_query(_QUERIES['albanian_surnames']))[0]


def male_full_name_w_middle_initial():
    pass


def gender():
    pass


def hyphenated_last_name():
    pass


def initial():
    pass


def language():
    pass


def last_name():
    return random.choice(_query(_QUERIES['albanian_surnames']))[0]


def male_middle_name():
    return random.choice(_query(_QUERIES['albanian_male_names']))[0]


def male_name():
    return random.choice(_query(_QUERIES['albanian_male_names']))[0]


def month():
    pass


def month_and_day():
    pass


def month_and_day_and_year():
    pass


def name():
    pass


def number():
    pass


def password_alphabetical():
    pass


def password_numerical():
    pass


def password_alphanumeric():
    pass


def phone_number():
    pass


def random_string():
    pass


def salutation():
    pass


def screename():
    pass


def sentence():
    pass


def set_of_initials():
    pass


def social_security_number():
    pass


def special_characters():
    pass


def street_type():
    pass


def street_name():
    pass


def street_address():
    pass


def suffix():
    pass


def timestamp():
    pass


def timezone_offset():
    pass


def timezone_offset_country():
    pass


def url():
    pass


def state_abbreviated():
    pass


def postal_code():
    pass
