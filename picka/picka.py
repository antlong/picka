#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Picka is a data generation and randomization module which aims to increase
coverage by increasing the amount of tests you _dont_ have to write
by hand.
By: Anthony Long
"""

from functools import partial
import string
import random as _random
import time
import re
import calendar


import picka_utils as _utils
from english import name as _name


__docformat__ = 'restructuredtext en'

_rewhite = re.compile(r"\s+")
_rewhitesub = partial(_rewhite.sub, "")
_query = _utils.query
_max_counts = _utils.row_counts

def male():
    return _name("{male}")

def female():
    return _name("{female}")

name = _name

###########
# User Data
###########
# Todo: Add IP Address generator


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
    return "{} {}".format(_query("name", "streetnames"), str(street_type()))


def street_type():
    """This function will return a random street type."""
    return _query("name", "us_street_types")


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
    return _query("city", "us_cities")


def city_with_state():
    """
    This function produces a city with a state.
    ie - city_with_state() = 'New York, NY'
    """
    return ', '.join(_query("city, state", "us_cities"))


def state_abbreviated():
    """
    This function produces just a state abbreviation.
    eg - state_abbreviated() = 'NY'
    """
    return _query("abbreviation", "states")


@_utils.deprecated("picka.zipcode(state)")
def postal_code():
    return zipcode()

def sum_of_ranges(*ranges):
    for r in ranges:
        for num in r:
            yield num


def zipcode(state=False):
    """This function will pick a zipcode randomnly from a list.
    eg - zipcode() = '11221'.
    """
    range_gen = []
    if state:
        _range = _query(custom='SELECT min, max from zipcodes where st = "{}";'.format(state), quantity=True)
        for r in _range:
            range_gen += range(r[0], r[1])
        return '%05d' % _random.choice(range_gen)
    else:
        range_gen += _query(custom='SELECT min, max from zipcodes ORDER BY RANDOM() LIMIT 1;', quantity=True)[0]
    print range_gen
    return '%05d' % _random.randint(range_gen[0], range_gen[1])





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
