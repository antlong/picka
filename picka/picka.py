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

import english


__docformat__ = 'restructuredtext en'

connect = \
    sqlite3.connect(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'db.sqlite'))
connect.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
cursor = connect.cursor()
_max_counts = {}
_rewhite = re.compile(r"\s+")
_rewhitesub = partial(_rewhite.sub, "")


def _get_max(tablename):
    if tablename in _max_counts:
        return _max_counts[tablename]
    cursor.execute('SELECT MAX(_ROWID_) FROM {} LIMIT 1'.format(tablename))
    _max_counts[tablename] = cursor.fetchone()[0]
    return _max_counts[tablename]


def initial(with_period=False):
    """Returns a randomly chosen letter, with a trailing period if desired.

        :parameters: with_period: (bool)
            Whether or not to add a trailing period.

    """
    letter = _random.choice(string.ascii_uppercase)
    return "{0:s}.".format(letter) if with_period else letter


def female():
    """Returns a randomly chosen female first name."""
    cursor.execute('SELECT name FROM female WHERE id =?', [
        _random.randint(1, _get_max("female"))])
    return cursor.fetchone()[0].decode("utf-8")


def male():
    """Returns a randomly chosen male first name."""
    cursor.execute('SELECT name FROM male WHERE id =?', [
        _random.randint(1, _get_max("male"))])
    return cursor.fetchone()[0].decode("utf-8")


def surname():
    """Returns a randomly chosen surname."""
    cursor.execute('SELECT name FROM surname WHERE id =?', [
        _random.randint(1, _get_max("surname"))])
    return cursor.fetchone()[0].decode("utf-8")


def age(minimum=1, maximum=99):
    """
    Returns a random age, from a range.

    :parameters:
        min: (integer)
            The lowest integer to use in the range
        max: (integer)
            The highest integer to use in the range

    :tip:
        If min and max are empty, 1 and 99 will be used.

    """

    return '%.i'.format(_random.randint(
        minimum, maximum) if minimum and maximum else _random.randint(
        1, 100))


def month():
    return _random.choice(calendar.month_name[1:])


def birthday(min_year=1900, max_year=2012):
    rmonth = _random.randrange(1, 13)
    birthday_month = calendar.month_name[rmonth]
    birthday_year = _random.randrange(min_year, max_year + 1)
    birthday_day = calendar.monthrange(birthday_year, rmonth)[1]
    return birthday_month, birthday_day, birthday_year


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


def business_title(abbreviated=False):
    """
    This will produce a random business title.

    :parameters:
        abbreviated: (boolean)
            Do you want abbreviated titles?

    This function will return business titles. \
    :tip: They are generic business titles.

    """
    abbs = ['COO', 'CEO', 'CFO', 'VP', 'EVP']
    primary = [
        'Lead',
        'Senior',
        'Direct',
        'Corporate',
        'Dynamic',
        'Future',
        'Product',
        'National',
        'Global',
        'Customer',
        'Investor',
        'Dynamic',
        'International',
        'Principal',
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


def career():
    """This function will produce a career."""
    cursor.execute('SELECT name FROM careers ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


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


def company_name():
    """This function will return a company name"""

    cursor.execute('SELECT name FROM companies \
        ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


def country():
    """This function will return a random country."""
    cursor.execute('SELECT name FROM countries \
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


def email(length=8, domain='@example.com'):
    """
    :Summary: Created a randomized email.
    :Usage: picka.email(length=8, domain='@foo.com')
    """

    return ''.join(_random.choice(string.ascii_lowercase) for _ in
                   xrange(length)) + domain


def fax_number():
    """
    :Summary: Returns a fax (phone) number.
    :Usage: picka.fax_number() >>> 755-463-6544
    """

    return phone_number()


def female_name():
    """
     :Summary: Returns a random female name.
     :Usage: picka.female_name() >>> 'Christy'
    """

    cursor.execute('SELECT name FROM female ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


def trash(picka_function):
    """
     :Summary: This method takes a function you pass in, and joins\
     the output with random punctuation.
     :Date: Tue Feb 22 15:31:12 EST 2011.
     :Usage: picka.trash(picka.name) >>> 'D#o}y>l~e^'
    """
    return ''.join([str(char) + _random.choice(str(string.punctuation))
                    for char in picka_function()])


def gender():
    """
    Returns a random gender.
    """

    return _random.choice(['Male', 'Female'])


def hyphenated_last_name():
    """
    This function will pick 2 random last names and hyphenate them.
    ie - hyphenated_last_name() = 'Perry-Jenkins'
    """

    return '{}-{}'.format(last_name(), last_name())


def language():
    """Picks a random language."""

    cursor.execute('SELECT name FROM languages ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


last_name = surname
last = last_name


def month_and_day():
    """
    Selects and month and day for you.
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


def name():
    """Picks a random male or female name."""
    return _random.choice([male(), female()])


def number(i):
    """
    This function will produce a random number with as many
    characters as you wish.
    """
    return ''.join(str(_random.randrange(0, 10)) for _ in xrange(i))


def password_alphabetical(i):
    """
    This function will return a randomized password consisting of letters.
    """

    return ''.join(_random.choice(string.ascii_letters) for _ in
                   range(i))


def password_numerical(i):
    """
    This function will return a random password consisting of numbers.
    """

    return ''.join(_random.choice(string.digits) for _ in xrange(i))


def password_alphanumeric(i):
    """
    This function will return an alphanumeric password.
    """

    chars = string.ascii_letters + string.digits
    return ''.join(_random.choice(chars) for _ in xrange(i))


def phone_number():
    """
    This function will produce a phone number randomnly.
    """

    x = ''.join(str(_random.randrange(0, 10)) for _ in xrange(10))
    y = '%s-%s-%s' % (x[0:3], x[3:6], x[6:])
    return y


def random_string(i):
    """
    This will allow you to enter an integer, and create 'i' amount
    of characters. ie: random_string(7) = DsEIzCd
    """

    return ''.join(_random.choice(string.ascii_letters) for _ in
                   xrange(i))


def salutation():
    """
    This function will return a 'Mr.' or 'Mrs.'
    """

    salutations = ('Mr.', 'Mrs.')
    return _random.choice(salutations)


def screename(service=''):
    """
    Makes screenames for the service you pick.
    The screenames conform to their rules, such as
    aol screenames are 3-16 in length with @aol.com on the end.
    Options include: nil, aol, aim, skype, google
    """

    def _make_name(a, b):
        return ''.join(_random.sample(
            string.ascii_letters, _random.choice(
                range(a, b)))
        )

    if service in ['', 'aim', 'aol']:
        return _make_name(3, 16)
    elif service is 'skype':
        return _make_name(6, 32)
    elif service is 'google':
        return _make_name(1, 19) + '@googletalk.com'
    else:
        return _make_name(8, 20)


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


def set_of_initials(i=3):
    """Returns initials with period seperators."""

    return [''.join(_random.choice(string.ascii_uppercase) + '.'
                    for _ in xrange(i))]


def social_security_number():
    """
    This function will produce a Mock Social Security Number.
    ie - social_security_number() = '112-32-3322'
    """

    return '%.3i-%.2i-%.4i' % (_random.randrange(999),
                               _random.randrange(99),
                               _random.randrange(9999))


def special_characters(i):
    """
    This function will pick x amount of special chars from the list below.
    ie - picka.special_characters() = '@%^$'.
    """

    return ''.join(_random.choice(string.punctuation) for _ in xrange(i))


def street_type():
    """This function will return a random street type."""

    cursor.execute('SELECT * FROM us_street_types \
        ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


def street_name():
    """
    This function will create a street name from either
    a male or female name, plus a street type.
    """

    return ' '.join((_random.choice([
        male_first(), female_name()]), street_type()))


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


def suffix():
    """This returns a suffix from a small list."""
    return _random.choice([
        'Sr.', 'Jr.', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'
    ])


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


def url(i, extension='.com'):
    """
    This function will create a website url, with a default of .com
    To use another extension, do picka.url(10, ".net")
    """

    return email(i, extension)


def state_abbreviated():
    """
    This function produces just a state abbreviation.
    eg - state_abbreviated() = 'NY'
    """

    cursor.execute('SELECT * FROM us_cities_with_states \
        ORDER BY RANDOM() LIMIT 1;')
    return (cursor.fetchone()[0])[-2:]


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


def foreign_characters(i):
    foreign_chars = (
        u'ƒŠŒŽšœžŸÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ'
    )
    return ''.join(_random.choice(foreign_chars) for _ in xrange(i))


def mac_address():
    mac = [
        0x00, 0x16, 0x3e,
        _random.randint(0x00, 0x7f),
        _random.randint(0x00, 0xff),
        _random.randint(0x00, 0xff)
    ]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def rbg():
    return [_random.randint(0, 257) for _ in xrange(3)]


def rbga(a=0):
    x = rbg()
    x.append(a) if isinstance(a, (int, long)) else x.append(_random.randint(0, 257))
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
        # noinspection PyPackageRequirements
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
    """
    Based on the standard barcode specifications. Valid options are:
    EAN-8 - 8 numerical digits.
    EAN-13 - 13 numerical digits.

    Unsupported, but in-progress:

    UPC-A - Used on products at the point of sale
    UPC-B - Developed for the US National Drug Code; used to identify drugs
    UPC-E - Used on smaller products where 12 digits don’t fit
    UPC-5 - Used as a supplemental code to indicate the price of retail books
    """
    if specification == "EAN-8":
        return '{:02}{:06}'.format(
            _random.randrange(0, 20),
            _random.randrange(0, 1000000)
        )
    if specification == "EAN-13":
        # For some reason this was returning a space
        # in the third position sometimes.
        return ''.join('{:02}{:011}'.format(
            _random.randrange(0, 20),
            _random.randrange(0, 100000000000))
        )


def mime_type():
    """Returns tuple, left is suffix, right is media type/subtype.
    """
    cursor.execute('SELECT extension,name FROM mimes WHERE id =?', [
        _random.randint(1, _get_max("mimes"))])
    return cursor.fetchone()


def male_full_name():
    return english.name("{male} {male} {surname}")


def male_full_name_w_middle_initial():
    return "{0} {1}".format(male(), initial())


female_first = female
female_middle = female
male_middle_name = male
male_middle = male
male_first = male
postal_code = zipcode