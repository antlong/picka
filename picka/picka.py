#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Picka is a data generation and randomization module which aims to increase
coverage by increasing the amount of tests you _dont_ have to write
by hand.
By: Anthony Long
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

from age import age, birthdate
import english
import picka_utils as _utils


__docformat__ = 'restructuredtext en'

connect = \
    sqlite3.connect(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'db.sqlite'))
connect.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
cursor = connect.cursor()
_max_counts = {}
_rewhite = re.compile(r"\s+")
_rewhitesub = partial(_rewhite.sub, "")


#######
# Utils
#######
def _get_max(tablename):
    if tablename in _max_counts:
        return _max_counts[tablename]
    cursor.execute('SELECT MAX(_ROWID_) FROM {} LIMIT 1'.format(tablename))
    _max_counts[tablename] = cursor.fetchone()[0]
    return _max_counts[tablename]


class _Book:
    """
    Keeps the text of a book and the split sentences of a book
    globally available. This means you don't have to read in
    all of a book's text every time you need  a sentence or a set of words.
    The book will only be read once. The sentences of the book will only
    be split apart once.
    """
    # TODO: I really think Sherlock is a bad source for sentences.
    # There are just too many weird quotes and fragments. Too much dialog.
    def __init__(self):
        pass

    _path = os.path.join(os.path.dirname(__file__),
                         "book_sherlock.txt")
    _text = _num_sentences = _sentences = None

    @classmethod
    def get_text(cls):
        if not cls._text:
            cls._text = open(cls._path).read()
        return cls._text

    @classmethod
    def get_sentences(cls):
        if not cls._sentences:
            text = cls.get_text()
            cls._sentences = _split_sentences(text)
            cls._num_sentences = len(cls._sentences)
        return cls._sentences

    @classmethod
    def gen_random_sentences(cls, no_more_than=1000000):
        sentences = cls.get_sentences()
        max_index = cls._num_sentences - 1
        for _ in xrange(no_more_than):
            i = _random.randint(0, max_index)
            yield sentences[i]


def _split_sentences(text):
    # from pyteaser: https://github.com/xiaoxu193/PyTeaser
    # see `pyteaser.split_sentences()`
    fragments = re.split('(?<![A-Z])([.!?]"?)(?=\s+\"?[A-Z])', text)
    return map("".join, izip(*[iter(fragments[:-1])] * 2))


#######
# Names
#######
class Name(object):
    """Picka.Name generates a full name object"""

    def __init__(self):
        pass


def salutation():
    """
    This function will return a 'Mr.' or 'Mrs.'
    """
    return _random.choice(['Mr.', 'Mrs.', 'Miss', 'Dr.', 'Prof.', 'Rev.'])


def male():
    """Returns a randomly chosen male first name."""
    cursor.execute('SELECT name FROM male WHERE id =?', [
        _random.randint(1, _get_max("male"))])
    return cursor.fetchone()[0].decode("utf-8")


def female():
    """Returns a randomly chosen female first name."""
    cursor.execute('SELECT name FROM female WHERE id =?', [
        _random.randint(1, _get_max("female"))])
    return cursor.fetchone()[0].decode("utf-8")


def initial(period=False):
    """Returns a randomly chosen letter, with a trailing period if desired.

    Args:
        with_period (bool): Whether or not to add a trailing period.

    Example:
      print picka.initial() => "B"

    >>> initial() in string.ascii_letters
    True
    >>> initial(period=True)[-1] == "."
    True

    """
    return "{0}{1}".format(random_string(), "." if period else "")


def set_of_initials(i=3):
    """Returns initials with period seperators."""

    return [''.join(_random.choice(string.ascii_uppercase) + '.'
                    for _ in xrange(i))]


def surname():
    """Returns a randomly chosen surname."""
    cursor.execute('SELECT name FROM surname WHERE id =?', [
        _random.randint(1, _get_max("surname"))])
    return cursor.fetchone()[0].decode("utf-8")


def hyphenated_last_name():
    """
    This function will pick 2 random last names and hyphenate them.
    ie - hyphenated_last_name() = 'Perry-Jenkins'
    """

    return '{}-{}'.format(last_name(), last_name())


def suffix():
    """This returns a suffix from a small list."""
    return _random.choice([
        'Sr.', 'Jr.', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'
    ])


@_utils.deprecated("picka.surname()")
def last_name():
    return surname()


@_utils.deprecated("picka.surname()")
def last():
    return last_name()


@_utils.deprecated("picka.name('{male}')")
def name():
    """Picks a random male or female name."""
    return _random.choice([male(), female()])


@_utils.deprecated("picka.name(format='{male}{middle}{last}'")
def male_full_name():
    return english.name("{male} {male} {surname}")


@_utils.deprecated("picka.name(format='{male}{initial}{last}', gender='M'")
def male_full_name_w_middle_initial():
    return english.name("{male} {initial}")


@_utils.deprecated("picka.name('{female}')")
def female_first():
    return female()


@_utils.deprecated("picka.name('{female}')")
def female_middle():
    return female()


@_utils.deprecated("picka.name('{female}')")
def female_name():
    """
     :Summary: Returns a random female name.
     :Usage: picka.female_name() >>> 'Christy'
    """
    return female()


@_utils.deprecated("picka.name('{male}')")
def male_middle_name():
    return male()


@_utils.deprecated("picka.name('{male}')")
def male_middle():
    return male()


@_utils.deprecated("picka.name('{male}')")
def male_first():
    return male()


###########
# User Data
###########
# Todo: Add IP Address generator
def email(length=8, domain='@example.com'):
    """
    :Summary: Created a randomized email.
    :Usage: picka.email(length=8, domain='@foo.com')
    """

    return ''.join(_random.choice(string.ascii_lowercase) for _ in
                   xrange(length)) + domain


def screename(*service):
    """
    Makes screenames for the service you pick.
    The screenames conform to their rules, such as
    aol screenames are 3-16 in length with @aol.com on the end.
    Options include: nil, aol, aim, skype, google
    """
    service = "aim" if not service else service

    def _make_name(a, b):
        return ''.join(_random.sample(
            string.ascii_letters, _random.choice(
                range(a, b)))
        )

    if service in ['aim', 'aol']:
        return _make_name(3, 16)
    elif service is 'skype':
        return _make_name(6, 32)
    elif service is 'google':
        return _make_name(1, 19) + '@googletalk.com'
    else:
        return _make_name(8, 20)


@_utils.deprecated("picka.password(format='numbers')")
def password_alphanumeric(i=8):
    return password(length=i, format="numbers")


@_utils.deprecated("picka.password(format='letters', length=8")
def password_alphabetical(i=8, case="mixed"):
    return password(case=case, length=i)


@_utils.deprecated("picka.password(format='numeric', length=8")
def password_numerical(i):
    return password(length=i)


def password(case='mixed', length=6, format='letters', special_chars=False):
    choices = ''
    if format in ['letters', 'alphanumeric']:
        cases = {
            'upper': string.ascii_uppercase,
            'mixed': string.ascii_letters,
            'lower': string.ascii_lowercase
        }
        choices += cases[case]
    if format in ['numbers', 'alphanumeric']:
        choices += string.digits
    if special_chars:
        choices += string.punctuation
    output = ''
    for _ in xrange(length):
        output += _random.choice(choices)
    return output


def url(i, extension='.com'):
    """
    This function will create a website url, with a default of .com
    To use another extension, do picka.url(10, ".net")
    """

    return email(i, extension)


def mac_address():
    mac = [
        0x00, 0x16, 0x3e,
        _random.randint(0x00, 0x7f),
        _random.randint(0x00, 0xff),
        _random.randint(0x00, 0xff)
    ]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def gender():
    """
    Returns a random gender.
    """

    return _random.choice(['Male', 'Female'])


def language():
    """Picks a random language."""

    cursor.execute('SELECT name FROM languages ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


def social_security_number(state="NY"):
    """Produces a US Social Security Number.

    Example:
      social_security_number() => '112-32-3322'

    >>> assert len(social_security_number()) == 11

    """
    x = _random.choice(_utils._ssn_prefixes(state))
    return '{0}-{1}-{2}'.format(
        _random.randrange(x[0], x[1] + 1),
        number(2),
        number(4)
    )


def drivers_license(state='NY'):
    """Generates drivers license numbers that adhere to the state license format.

    Args:
      state (str, optional): Two letter state code.

    Returns:
      str: generated license code.

    Examples:
        print drivers_license() => "I370162546092578729"
        print drivers_license("AL") => "2405831"

    >>> assert len(drivers_license()) > 0
    >>> assert len(drivers_license("OK")) in [9, 10]

    """
    lengths = {
        "AL": [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
        "AK": [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
        "AZ": [[1, 8], [2, 5], [0, 9]],
        "AR": [[0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9]],
        "CA": [[1, 7]],
        "CO": [
            [0, 9], [1, 3], [1, 4], [1, 5], [1, 6],
            [2, 2], [2, 3], [2, 4], [2, 5]
        ],
        "DE": [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
        "DC": [[0, 7], [0, 9]],
        "FL": [[1, 12]],
        "GA": [[0, 7], [0, 8], [0, 9]],
        "HI": [[1, 8], [0, 9]],
        "ID": [[2, 6], [2, 6, 1], [0, 9]],
        "IL": [[0, 11], [1, 12]],
        "IN": [[1, 9], [0, 9], [0, 10]],
        "IA": [[0, 9], [0, 3, 2, 4]],
        "KS": [[1, 1, 1, 1, 1], [1, 8], [0, 9]],
        "KY": [[1, 8], [1, 9], [0, 9]],
        "LA": [
            [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
            [0, 8], [0, 9]
        ],
        "ME": [[0, 7], [0, 7, 1], [0, 8]],
        "MD": [[1, 12]],
        "MA": [[1, 8], [0, 9]],
        "MI": [[1, 10], [1, 12]],
        "MN": [[1, 12]],
        "MS": [[0, 9]],
        "MO": [
            [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [1, 6, "R"],
            [0, 8, 2], [9, 1], [0, 9]
        ],
        "MT": [[1, 8], [0, 13], [0, 9], [0, 14]],
        "NE": [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
        "NV": [[0, 9], [0, 10], [0, 12], [1, 8]],
        "NH": [[0, 2, 3, 5]],
        "NJ": [[1, 14]],
        "NM": [[0, 8], [0, 9]],
        "NY": [[1, 7], [1, 18], [0, 8], [0, 9], [0, 16], [8, 0]],
        "NC": [
            [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
            [0, 8], [0, 9], [0, 10], [0, 11], [0, 12]
        ],
        "ND": [[3, 6], [0, 9]],
        "OH": [
            [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [2, 3], [2, 4],
            [2, 5], [2, 6], [2, 7], [0, 8]
        ],
        "OK": [[1, 9], [0, 9]],
        "OR": [
            [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
            [0, 8], [0, 9], [1, 6], [2, 5]
        ],
        "PA": [[0, 8]],
        "RI": [[0, 7], [1, 6]],
        "SC": [[0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11]],
        "SD": [[0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 12]],
        "TN": [[0, 7], [0, 8], [0, 9]],
        "TX": [[0, 7], [0, 8]],
        "UT": [[0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10]],
        "VT": [[0, 8], [0, 7, "A"]],
        "VI": [[1, 9], [1, 10], [1, 11], [0, 9]],
        "WA": [],
        "WV": [[0, 7], [1, 5], [2, 5], [1, 6], [2, 6]],
        "WI": [[1, 13]],
        "WY": [[0, 9], [0, 10]]
    }
    if state == "WA":
        i = _random.choice([_random.randint(1, 7), 12])
        return password(
            case="upper",
            length=i,
            format="alphanumeric",
            special_chars=False
        )
    n = _random.choice(lengths[state])
    s = ""
    s += random_string(length=n[0])
    s += number(length=n[1])

    if len(n) > 2:
        if state == "ID":
            s += random_string()
        if state == "IA":
            s += random_string(length=n[2])
            s += number(n[3])
        if state == "KS":
            s += random_string(n[2])
            s += number(n[3])
            s += random_string(n[4])
        if state == "MO":
            s += "R" if n[2] == "R" else random_string(n[2])
        if state == "NH":
            s += number(n[3])

    if state == "NV" and n == [1, 8]:
        s = s.replace(s[0], "X")
    if state == "VT" and n == [0, 7, "A"]:
        s = s.replace(s[-1], "A")
    return "{0}".format(s)


def business_title(abbreviated=False):
    """This will produce a random business title.

    :parameters:
        abbreviated: (boolean)
            Do you want abbreviated titles?

    This function will return business titles. \
    :tip: They are generic business titles.

    """
    abbs = ['COO', 'CEO', 'CFO', 'VP', 'EVP']
    primary = [
        'Lead', 'Senior', 'Direct', 'Corporate', 'Dynamic',
        'Future', 'Product', 'National', 'Global', 'Customer',
        'Investor', 'Dynamic', 'International', 'Principal'
    ]
    secondary = [
        'Supervisor',
        'Associate',
        'Executive',
        'Liason',
        'Officer',
        'Manager',
        'Engineer',
        'Specialist',
        'Director',
        'Coordinator',
        'Assistant',
        'Facilitator',
        'Agent',
        'Representative',
        'Strategist',
    ]
    return ((_random.choice(abbs) if abbreviated else '{} {}'.format(
        _random.choice(primary), _random.choice(secondary))))


def career():
    """This function will produce a career."""
    cursor.execute('SELECT name FROM careers ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


def company_name():
    """This function will return a company name"""

    cursor.execute('SELECT name FROM companies \
        ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


def creditcard(prefix='visa'):
    if prefix == 'visa':
        prefix = ['40240071']
    elif prefix == 'amex':
        prefix = ['34', '37']
    elif prefix == 'discover':
        prefix = ['6011']
    elif prefix == 'mastercard':
        prefix = ['51', '52', '53', '54', '55']
    while len(prefix) < 15:
        prefix += str(_random.randint(0, 9))
    return ''.join(prefix) + '0'


def cvv(i):
    """Returns a cvv, based on the length you provide.
    :Usage: picka.cvv(3) or picka.cvv(4)
    """

    return '{}'.format(_random.randint(111, (999 if i == 3 else 9999)))


# Address
def street_address():
    """This function will produce a complete street address."""

    return _random.choice(
        [
            '%d-%d %s' % (
                _random.randrange(999),
                _random.randrange(999),
                street_name()
            ),
            '%d %s' % (
                _random.randrange(999),
                street_name()
            ),
            '%s %d, %s' % (
                'P.O. Box',
                _random.randrange(999),
                street_name()
            )
        ]
    )


def street_name():
    """
    This function will create a street name from either
    a male or female name, plus a street type.
    """

    return ' '.join((_random.choice([
        male_first(), female_name()]), street_type()))


def street_type():
    """This function will return a random street type."""

    cursor.execute('SELECT * FROM us_street_types \
        ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


def apartment_number():
    """
    Returns an apartment type, with a number.

    :tip: There are many different types which could be returned.
    If you are looking for a specific format, you might be interested\
    in using string formatting instead.

    """
    _type = _random.choice(['Apt.', 'Apartment', 'Suite', 'Ste.'])
    letter = _random.choice(string.ascii_letters).capitalize()
    directions = ['E', 'W', 'N', 'S']
    short = '{} {}'.format(_type, _random.randint(1, 999))
    _long = '{} {}{}'.format(_type, _random.randint(1, 999), letter)
    alt = '{} {}-{}{}'.format(_type, _random.choice(directions),
                              _random.randint(1, 999), letter)
    return _random.choice([short, _long, alt])


def city():
    """This function will produce a city."""
    cursor.execute('SELECT city FROM us_cities \
        ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


def city_with_state():
    """
    This function produces a city with a state.
    ie - city_with_state() = 'New York, NY'
    """

    cursor.execute('SELECT city, state FROM us_cities \
        ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()


def state_abbreviated():
    """
    This function produces just a state abbreviation.
    eg - state_abbreviated() = 'NY'
    """

    cursor.execute('SELECT * FROM us_cities_with_states \
        ORDER BY RANDOM() LIMIT 1;')
    return (cursor.fetchone()[0])[-2:]


@_utils.deprecated("picka.zipcode(state)")
def postal_code():
    return zipcode()


def zipcode(state=False):
    """This function will pick a zipcode randomnly from a list.
    eg - zipcode() = '11221'.
    """
    if not state:
        cursor.execute('SELECT min,max FROM zipcodes')
    else:
        cursor.execute('SELECT min,max FROM zipcodes WHERE st = ?', [state])
    _range = _random.choice(cursor.fetchall())
    return '%05d' % _random.randint(_range[0], _range[1])


def country():
    # Todo: Use max row.
    """This function will return a random country."""
    cursor.execute('SELECT name FROM countries \
        ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


# Phone Data
def calling_code():
    """
    Returns a calling code from a list of all known calling codes in \
    the world.
    """

    cursor.execute(
        'SELECT calling_code FROM countries_and_calling_codes \
        ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


def calling_code_with_country():
    """Returns a country, with a calling code as a single string."""

    return cursor.execute('SELECT * FROM countries_and_calling_codes \
        ORDER BY random() LIMIT 1;')


def area_code(state=False):
    if state:
        cursor.execute('SELECT code FROM areacodes WHERE state = ? \
            ORDER BY RANDOM() LIMIT 1;', [state])
    else:
        cursor.execute('SELECT code FROM areacodes ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


def phone_number(state=False, formatting=False):
    """Generate a phone number. Conforms to NANP standards.

    :arg state: Bool
    :arg formatting: local, domestic, or international
    """

    def _gen():
        while True:
            n = str(_random.randint(2, 9)) + str(
                _random.randrange(10 ** (2 - 1), 10 ** 2))
            if n not in ["911", "555"]:
                break
        return n

    if formatting in ("local",):
        # 754-3010
        return "{0}-{1}".format(_gen(), number(4))
    elif formatting in ("domestic",):
        # (541) 754-3010
        return "({0}) {1}-{2}".format(area_code(state), _gen(), number(4))
    elif formatting in ("international",):
        # +1-541-754-3010
        return "+1-{0}-{1}-{2}".format(area_code(state), _gen(), number(4))
    else:
        # 204-371-1275
        return "{0}-{1}-{2}".format(area_code(state), _gen(), number(4))


@_utils.deprecated("picka.phone_number(formatting)")
def fax_number():
    """
    :Summary: Returns a fax (phone) number.
    :Usage: picka.fax_number() >>> 755-463-6544
    """

    return phone_number()


#############
# Time & Date
#############
def month():
    return _random.choice(calendar.month_name[1:])


def month_and_day():
    """Selects and month and day for you.
    There is logic to handle the days in the month correctly.
    """

    month_choice = month()
    if month_choice in [
        'January', 'March', 'May', 'July', 'August',
        'October', 'December'
    ]:
        return '%s %s' % (month_choice, _random.randrange(1, 32))
    if month_choice in 'February':
        return '%s %s' % (month_choice, _random.randrange(1, 29))
    else:
        return '%s %s' % (month_choice, _random.randrange(1, 31))


def month_and_day_and_year(start=1900, end=2010):
    """
    Selects a monday, day and year for you.
    Logic built in to handle day in month.
    To change month do (a, b). b has +1 so the
    last year in your range can be selected. Default is 1900, 2010.
    """

    return '%s %s' % (month_and_day(), _random.randrange(start, end + 1))


def timestamp(style=False):
    """
    This is a convenience function for creating timestamps.
    Default when empty, is "12:28:59PM 07/20/10" or "%H:%M:%S%p %D".
    To change this, pass in your format as an arg.
    """

    if not style:
        return time.strftime('%H:%M:%S%p %x', time.localtime())
    else:
        return time.strftime(style, time.localtime())


def timezone_offset():
    """
    This function will select the value of a timezone offsets,
    such as GMT, GMT+4, etc.
    """

    return _random.choice(
        [
            ['GMT+' + str(_random.randint(1, 12))],
            ['GMT'],
            ['GMT' + str(_random.randint(-12, -1))]
        ]
    )[0]


def timezone_offset_country():
    """This function will select the country part of a timezone."""

    return _random.choice(
        [
            'Eniwetoa',
            'Hawaii',
            'Alaska',
            'Pacific',
            'Mountain',
            'Central',
            'Eastern',
            'Atlantic',
            'Canada',
            'Brazilia',
            'Buenos Aries',
            'Mid-Atlantic',
            'Cape Verdes',
            'Greenwich Mean Time',
            'Dublin',
            'Berlin',
            'Rome',
            'Israel',
            'Cairo',
            'Moscow',
            'Kuwait',
            'Abu Dhabi',
            'Muscat',
            'Islamabad',
            'Karachi',
            'Almaty',
            'Dhaka',
            'Bangkok, Jakarta',
            'Hong Kong',
            'Beijing',
            'Tokyo',
            'Osaka',
            'Sydney',
            'Melbourne',
            'Guam',
            'Magadan',
            'Soloman Islands',
            'Fiji',
            'Wellington',
            'Auckland',
        ]
    )


######
# Misc
######
def trash(picka_function):
    """
     :Summary: This method takes a function you pass in, and joins\
     the output with random punctuation.
     :Date: Tue Feb 22 15:31:12 EST 2011.
     :Usage: picka.trash(picka.name) >>> 'D#o}y>l~e^'
    """
    return ''.join([str(char) + _random.choice(str(string.punctuation))
                    for char in picka_function()])


def number(length=1):
    """This function will produce a random number with as many
    characters as you wish.
    """
    return ''.join(str(_random.randrange(0, 10)) for _ in xrange(length))


def random_string(length=1, case='upper'):
    """
    This will allow you to enter an integer, and create 'i' amount
    of characters. ie: random_string(7) = DsEIzCd
    """
    choices = ''
    output = ''
    cases = {
        'upper': string.ascii_uppercase,
        'lower': string.ascii_lowercase,
        'mixed': string.ascii_letters
    }
    choices += cases[case]
    for _ in xrange(length):
        output += _random.choice(choices)
    return output


def sentence(num_words=20, chars=''):
    """
    Returns a sentence based on random words from The Adventures of
    Sherlock Holmes that is no more than `chars` characters in length
    or `num_words` words in length.
    """
    word_list = _Book.get_text().split()
    words = ' '.join(_random.choice(word_list) for _ in
                     xrange(num_words))
    return words if not chars else words[:chars]


def sentence_actual(min_words=3, max_words=1000):
    """
    Returns a sentence from The Adventures of Sherlock Holmes
    that contains at least `min_words` and no more than `max_words`.
    """
    for x in _Book.gen_random_sentences():
        words = _rewhite.split(x)
        words = filter(None, map(_rewhitesub, words))
        x = " ".join(words)
        if x.endswith(("Mr.", "Mrs.", "Dr.", "Ms.", "Prof.")):
            continue
        if min_words <= len(x.split()) <= max_words:
            return x
    raise Exception("Couldn't find a sentence between \
        {0} and {1} words long".format(min_words, max_words))


def foreign_characters(i):
    foreign_chars = (
        u'ƒŠŒŽšœžŸÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕ\
        ÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ'
    )
    return ''.join(_random.choice(foreign_chars) for _ in xrange(i))


def special_characters(i):
    """
    This function will pick x amount of special chars from the list below.
    ie - picka.special_characters() = '@%^$'.
    """

    return ''.join(_random.choice(string.punctuation) for _ in xrange(i))


def rbg():
    return [_random.randint(0, 256) for _ in xrange(3)]


def rbga(a=0):
    x = rbg()
    x.append(a) if isinstance(a, (
        int, long)) else x.append(_random.randint(0, 256))
    return x


# noinspection PyUnresolvedReferences
def image(filepath, length=100, width=100, a=0):
    """Generate a random colored image, with random text on it.
    Returns filepath for ease of use.

        :param: filepath: path to save image to.
        :type filepath: str
        :param length: length of the image
        :type length: int
        :param width: width of the image
        :type width: int
    """
    try:
        import Image
        import ImageDraw
    except ImportError as e:
        print e, "Please install PIL to use this functionality."
        return
    im = Image.new('RGBA', tuple((length, width)), tuple((rbga(a))))
    draw = ImageDraw.Draw(im)
    text = sentence_actual(1)
    draw.text((0, 0), text, fill=rbg())
    im.save(filepath)
    return filepath


def hex_color():
    def _chkarg(a):
        if isinstance(a, int):
            if a < 0:
                a = 0
            elif a > 255:
                a = 255
        elif isinstance(a, float):
            if a < 0.0:
                a = 0
            elif a > 1.0:
                a = 255
            else:
                a = int(round(a * 255))
        return a

    r, b, g = rbg()
    r = _chkarg(r)
    g = _chkarg(g)
    b = _chkarg(b)
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def barcode(specification="EAN-8"):
    """Based on the standard barcode specifications. Valid options are:
    EAN-8 - 8 numerical digits.
    EAN-13 - 13 numerical digits.
    UPC-A - Used on products at the point of sale

    Unsupported, but in-progress:
    UPC-B - Developed for the US National Drug Code; used to identify drugs
    UPC-E - Used on smaller products where 12 digits don’t fit
    UPC-5 - Used as a supplemental code to indicate the price of retail books
    """

    def _gen(i):
        upc_str = str(i)
        odd_sum = 0
        even_sum = 0
        for i, char in enumerate(upc_str):
            j = i + 1
            if j % 2 == 0:
                even_sum += int(char)
            else:
                odd_sum += int(char)
        total_sum = (odd_sum * 3) + even_sum
        mod = total_sum % 10
        check_digit = 10 - mod
        if check_digit == 10:
            check_digit = 0
        return upc_str + str(check_digit)

    if specification == "EAN-8":
        return _gen(number(7))

    if specification == "EAN-13":
        return _gen(number(12))

    if specification == "UPC-A":
        return _gen(number(11))


def mime_type():
    """Returns tuple, left is suffix, right is media type/subtype.
    """
    cursor.execute('SELECT extension,name FROM mimes WHERE id =?', [
        _random.randint(1, _get_max("mimes"))])
    return cursor.fetchone()
