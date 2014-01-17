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
import random
import time
import sqlite3
import os
import re
import calendar

__docformat__ = 'restructuredtext en'

connect = \
    sqlite3.connect(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'db.sqlite'))
cursor = connect.cursor()


def initial(with_trailing_period=False):
    """
    Returns a randomly chosen letter, with a trailing period if desired.

        :parameters: with_trailing_period: (bool)
            Whether or not to add a trailing period.
    """
    letter = random.choice(string.letters).upper()
    return (letter if not with_trailing_period else letter + '.')


def female_first():
    """Returns a randomly chosen female first name."""
    cursor.execute('SELECT name FROM female order by RANDOM() limit 1')
    return cursor.fetchone()[0]


def female_middle():
    """Returns a randomly chosen female middle name."""
    return female_first()


def male_first():
    """Returns a randomly chosen male first name."""
    cursor.execute('SELECT name FROM male order by RANDOM() limit 1')
    return cursor.fetchone()[0]


def male_middle():
    """Returns a randomly chosen male middle name."""
    return male_first()


def surnames():
    """Returns a randomly chosen surname."""

    cursor.execute('SELECT * FROM surname order by RANDOM() limit 1')
    return cursor.fetchone()[0]


def age(min=1, max=99):
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

    return '%.i' % ((random.randint(min, max + 1) if min
                    and max else random.randint(1, 100)))


def month():
    return random.choice(calendar.month_name)


def birthday(min_year=1900, max_year=2012):
    rmonth = random.randrange(1, 13)
    birthday_month = calendar.month_name[rmonth]
    birthday_year = random.randrange(min_year, max_year + 1)
    birthday_day = calendar.monthrange(birthday_year, rmonth)[1]
    return (birthday_month, birthday_day, birthday_year)


def apartment_number():
    """
    Returns an apartment type, with a number.

    :tip: There are many different types which could be returned.
    If you are looking for a specific format, you might be interested\
    in using string formatting instead.

    """

    type = random.choice(['Apt.', 'Apartment', 'Suite', 'Ste.'])
    letter = random.choice(string.ascii_letters).capitalize()
    directions = ['E', 'W', 'N', 'S']
    short = '{} {}'.format(type, random.randint(1, 999))
    long = '{} {}{}'.format(type, random.randint(1, 999), letter)
    alt = '{} {}-{}{}'.format(type, random.choice(directions),
                              random.randint(1, 999), letter)
    return random.choice([short, long, alt])


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
    return ((random.choice(abbs) if abbreviated else '{} {}'.format(
        random.choice(primary), random.choice(secondary))))


def calling_code():
    """
    Returns a calling code from a list of all known calling codes in \
    the world.
    """

    cursor.execute(
        'SELECT calling_code FROM countries_and_calling_codes \
        order by RANDOM() limit 1;')
    return cursor.fetchone()[0]


def calling_code_with_country(formatting=''):
    """Returns a country, with a calling code as a single string."""

    cursor.execute('select * from countries_and_calling_codes \
        order by random() limit 1;')
    (country, calling_code) = cursor.fetchone()
    if formatting is dict:
        return formatting({country: calling_code})
    return (formatting([country,
            calling_code]) if formatting else '{} {}'.format(country,
            calling_code))


def career():
    """This function will produce a carrer."""
    cursor.execute('SELECT name FROM careers order by RANDOM() limit 1;')
    return cursor.fetchone()[0]


def city():
    """This function will produce a city."""
    cursor.execute('SELECT city FROM american_cities \
        order by RANDOM() limit 1;')
    return cursor.fetchone()[0]


def city_with_state():
    """
    This function produces a city with a state.
    ie - city_with_state() = 'New York, NY'
    """

    cursor.execute('SELECT city, state FROM american_cities \
        order by RANDOM() limit 1;')
    return cursor.fetchone()


def company_name():
    """This function will return a company name"""

    cursor.execute('SELECT name from companies \
        order by RANDOM() limit 1;')
    return cursor.fetchone()[0]


def country():
    """This function will return a random country."""

    cursor.execute('SELECT country_names FROM countries \
        order by RANDOM() limit 1;')
    return cursor.fetchone()[0]


def creditcard(type):
    if type == 'visa':
        prefix = ['40240071']
    elif type == 'amex':
        prefix = ['34', '37']
    elif type == 'discover':
        prefix = ['6011']
    elif type == 'mastercard':
        prefix = ['51', '52', '53', '54', '55']
    prefix = random.choice(prefix)
    while len(prefix) < 15:
        prefix = prefix + str(random.randint(0, 9))
    return ''.join(prefix) + '0'


def cvv(i):
    """Returns a cvv, based on the length you provide.
    :Usage: picka.cvv(3) or picka.cvv(4)
    """

    return '{}'.format(random.randint(111, (999 if i == 3 else 9999)))


def email(length=8, domain='@example.com'):
    """
    :Summary: Created a randomized email.
    :Usage: picka.email(length=8, domain='@foo.com')
    """

    return ''.join(random.choice(string.ascii_lowercase) for i in
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

    cursor.execute('SELECT name FROM female order by RANDOM() limit 1;')
    return cursor.fetchone()[0]


def _foreign_characters(a, b):
    """
    This function will pick x amount of foreign chars\
    from the list below, where a is min, and b is max.
    """

    pass


def trash(picka_function):
    """
     :Summary: This method takes a function you pass in, and joins\
     the output with random punctuation.
     :Date: Tue Feb 22 15:31:12 EST 2011.
     :Usage: picka.trash(picka.name) >>> 'D#o}y>l~e^'
    """
    return ''.join([str(char) + random.choice(str(string.punctuation))
                   for char in picka_function()])


def male_full_name():
    return '{} {}'.format(male_first(), surnames())


def male_full_name_w_middle_initial(with_period=False):
    """Returns name, middile initial and last name."""

    return '{} {} {}'.format(male_first(), initial(with_period),
                             surnames())


def gender():
    """
    Returns a random gender.
    """

    return random.choice(['Male', 'Female'])


def hyphenated_last_name():
    """
    This function will pick 2 random last names and hyphenate them.
    ie - hyphenated_last_name() = 'Perry-Jenkins'
    """

    return '{}-{}'.format(last_name(), last_name())


def language():
    """Picks a random language."""

    cursor.execute('SELECT name from languages order by RANDOM() limit 1;')
    return cursor.fetchone()[0]


def last_name():
    """
    This function will return a last name from a list.
    ie - last_name() = 'Smith'.
    """

    return surnames()


def male_middle_name():
    """Picks a middle name from a list of male names."""

    return male_first()


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
        return '%s %s' % (month_choice, random.randrange(1, 32))
    if month_choice in 'February':
        return '%s %s' % (month_choice, random.randrange(1, 29))
    else:
        return '%s %s' % (month_choice, random.randrange(1, 31))


def month_and_day_and_year(start=1900, end=2010):
    """
    Selects a monday, day and year for you.
    Logic built in to handle day in month.
    To change month do (a, b). b has +1 so the
    last year in your range can be selected. Default is 1900, 2010.
    """

    return '%s %s' % (month_and_day(), random.randrange(start, end + 1))


def name():
    """Picks a random male or female name."""
    return random.choice([male_first(), female_first()])


def number(i):
    """
    This function will produce a random number with as many
    characters as you wish.
    """
    return ''.join(str(random.randrange(0, 10)) for x in xrange(i))


def password_alphabetical(i):
    """
    This function will return a randomized password consisting of letters.
    """

    return ''.join(random.choice(string.ascii_letters) for x in
                   range(i))


def password_numerical(i):
    """
    This function will return a random password consisting of numbers.
    """

    return ''.join(random.choice(string.digits) for x in range(i))


def password_alphanumeric(i):
    """
    This function will return an alphanumeric password.
    """

    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for x in range(i))


def phone_number():
    """
    This function will produce a phone number randomnly.
    """

    x = ''.join(str(random.randrange(0, 10)) for i in xrange(10))
    y = '%s-%s-%s' % (x[0:3], x[3:6], x[6:])
    return y


def random_string(i):
    """
    This will allow you to enter an integer, and create 'i' amount
    of characters. ie: random_string(7) = DsEIzCd
    """

    return ''.join(random.choice(string.ascii_letters) for x in
                   xrange(i))


def salutation():
    """
    This function will return a 'Mr.' or 'Mrs.'
    """

    salutations = ('Mr.', 'Mrs.')
    return random.choice(salutations)


def screename(service=''):
    """
    Makes screenames for the service you pick.
    The screenames conform to their rules, such as
    aol screenames are 3-16 in length with @aol.com on the end.
    Options include: nil, aol, aim, skype, google
    """

    def _make_name(a, b):
        return ''.join(random.sample(string.ascii_letters,
                       random.choice(range(a, b))))

    if service in ('', 'aim', 'aol'):
        name = _make_name(3, 16)
        if service == 'aol':
            return name + '@aol.com'
        else:
            return name
    elif service is 'skype':
        name = _make_name(6, 32)
        return name
    elif service is 'google':
        name = _make_name(1, 19)
        return name + '@google.com'
    else:
        name = _make_name(8, 20)
        return name


def sentence(num_words=20, chars=''):
    """
    Returns a sentence based on random words from The Adventures of
    Sherlock Holmes that is no more than `chars` characters in length
    or `num_words` words in length.
    """
    word_list = _Book.get_text().split()
    words = ' '.join(random.choice(word_list) for x in
                     xrange(num_words))
    return (words if not chars else words[:chars])


_rewhite = re.compile(r"\s+")
_rewhitesub = partial(_rewhite.sub, "")


def sentence_actual(min_words=3, max_words=1000):
    """
    Returns a sentence from The Adventures of Sherlock Holmes
    that contains at least `min_words` and no more than `max_words`.
    """
    for sentence in _Book.gen_random_sentences():
        words = _rewhite.split(sentence)
        words = filter(None, map(_rewhitesub, words))
        sentence = " ".join(words)
        if sentence.endswith(("Mr.", "Mrs.", "Dr.", "Ms.", "Prof.")):
            continue
        if min_words <= len(sentence.split()) <= max_words:
            return sentence
    raise Exception("Couldn't find a sentence between {0} and {1} words long".format(   
                    min_words, max_words))


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
            i = random.randint(0, max_index)
            yield sentences[i]
            

def _split_sentences(text):
    # from pyteaser: https://github.com/xiaoxu193/PyTeaser
    # see `pyteaser.split_sentences()`
    fragments = re.split('(?<![A-Z])([.!?]"?)(?=\s+\"?[A-Z])', text)
    return map("".join, izip(*[iter(fragments[:-1])] * 2))
    
        
def set_of_initials(i=3):
    """Returns initials with period seperators."""

    return [''.join(random.choice(string.ascii_uppercase) + '.'
            for x in xrange(i))]


def social_security_number():
    """
    This function will produce a Mock Social Security Number.
    ie - social_security_number() = '112-32-3322'
    """

    return '%.3i-%.2i-%.4i' % (random.randrange(999),
                               random.randrange(99),
                               random.randrange(9999))


def special_characters(i):
    """
    This function will pick x amount of special chars from the list below.
    ie - picka.special_characters() = '@%^$'.
    """

    return ''.join(random.choice(string.punctuation) for x in xrange(i))


def street_type():
    """This function will return a random street type."""

    cursor.execute('SELECT * FROM street_types \
        order by RANDOM() limit 1;')
    return cursor.fetchone()[0]


def street_name():
    """
    This function will create a street name from either
    a male or female name, plus a street type.
    """

    return ' '.join((random.choice([
        male_first(), female_name()]), street_type()))


def street_address():
    """This function will produce a complete street address."""

    return random.choice(
        [
            '%d-%d %s' % (
                random.randrange(999),
                random.randrange(999),
                street_name()
            ),
            '%d %s' % (
                random.randrange(999),
                street_name()
            ),
            '%s %d, %s' % (
                'P.O. Box',
                random.randrange(999),
                street_name()
            )
        ]
    )


def suffix():
    """This returns a suffix from a small list."""

    return random.choice(
        [
            'Sr.', 'Jr.', 'II', 'III', 'IV', 'V'
        ]
    )


def timestamp(style=False):
    """
    This is a convenience function for creating timestamps.
    Default when empty, is "12:28:59PM 07/20/10" or "%H:%M:%S%p %D".
    To change this, pass in your format as an arg.
    """

    if not style:
        return time.strftime('%H:%M:%S%p %D', time.localtime())
    else:
        return time.strftime(style, time.localtime())


def timezone_offset():
    """
    This function will select the value of a timezone offsets,
    such as GMT, GMT+4, etc.
    """

    return random.choice(
        [
            [
                'GMT+' + str(random.randint(1, 12))
            ],
            [
                'GMT'
            ],
            [
                'GMT' + str(random.randint(-12, -1))
            ]
        ]
    )[0]


def timezone_offset_country():
    """This function will select the country part of a timezone."""

    return random.choice(
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

    cursor.execute('SELECT * FROM american_cities_with_states \
        order by RANDOM() limit 1;')
    return (cursor.fetchone()[0])[-2:]


def postal_code():
    """
    This function will pick a zipcode randomnly from a list.
    eg - zipcode() = '11221'.
    """

    cursor.execute('SELECT col_1 FROM zipcodes order by RANDOM() limit 1;'
                   )
    return cursor.fetchone()[0]

zipcode = postal_code


def foreign_characters(i):
    foreign_chars = (
        u'ƒŠŒŽšœžŸÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛ'
        u'ÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ'
    )
    return ''.join(random.choice(foreign_chars) for x in xrange(i))


def mac_address():
    mac = [
        0x00, 0x16, 0x3e,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]
    return ':'.join(map(lambda x: "%02x" % x, mac))
