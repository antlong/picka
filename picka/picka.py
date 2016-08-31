#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions that generate data in the color category.

Attributes:
  engine (Engine): The connection to the database.

Notes:
  Corresponding tests are found in picka/tests/test_colors.py
"""
from random import randint, randrange, choice, uniform
from socket import inet_ntoa
from struct import pack
from string import ascii_letters, ascii_uppercase, digits, punctuation, \
    ascii_lowercase
from math import cos, pi, sqrt, sin
from time import localtime, strftime
from calendar import month_name, monthrange
from datetime import datetime
from re import split, compile
from itertools import izip
from functools import partial
from os.path import join, dirname
from dateutil.relativedelta import relativedelta
from attrdict import AttrDict
from sqlalchemy import text
from LatLon import LatLon
from sqlalchemy import engine
import picka_utils as picka_utils

path = join(dirname(
    __file__) + "/data/db.sqlite")
engine = engine.create_engine("sqlite:///" + path, echo=False)


class InvalidRange(ValueError):
    """Raise when a specific subset of values in context of app is wrong"""

    def __init__(self, message, *args):
        self.message = message
        super(InvalidRange, self).__init__(message, *args)


def rgb(format="list"):
    if format == "list":
        return [randint(0, 256) for _ in xrange(3)]
    else:
        r, g, b = [str(randint(0, 256)) for _ in range(3)]
        return AttrDict({"r": r, "g": g, "b": b})


def rgba(format="list", a=0):
    if format == "list":
        x = rgb()
        x.append(a) if isinstance(a, (
            int, long)) else x.append(randint(0, 256))
        return x
    else:
        _rgb = rgb()
        _rgb["a"] = str(100 * float(randint(1, 256)) / float(256) / 100)[:4]
        return _rgb


def hex_color():
    """Generates a hex color.

    Returns:
      AttrDict (str): A dictionary with the generated colors.

    Examples:
      >>> hex_color()
      AttrDict({'r': '82', 'b': '37', 'hex': '525725', 'g': '87'})
      >>> hex_color().hex
      '525725'
    """
    s = ""

    color_choice = rgb()
    r = color_choice.r
    g = color_choice.g
    b = color_choice.b

    for x in [r, g, b]:
        s += hex(int(x))[2:4].zfill(2)

    return AttrDict({"hex": s.upper(), "r": r, "g": g, "b": b})


def html_name():
    """Generates a random html color name.

    Returns:
      name (str): The name of the picked color.
      hex (str): The corresponding hex code of the color.

    Examples:
      >>> html_name()
      AttrDict({u'hex': u'80008', u'name': u'purple'})
      >>> html_name().hex
      '808080'
    """
    res = engine.execute(
        "SELECT name, hex FROM html_colors ORDER BY RANDOM() LIMIT 1;"
    )

    return AttrDict([dict(d) for d in res.fetchall()][0])


def mime_type():
    """Generates a random mime type.

    Returns:
      name (str): The full name of the mime type.
      extension (str): The file extension of the mime type.

    Examples:
      >>> mime_type()
      AttrDict({u'name': u'application.x-excel', u'extension': u'.xlv'})
    """
    res = engine.execute("SELECT name, extension FROM mimes ORDER BY  \
                         random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


def ipv4():
    return inet_ntoa(pack('>I', randint(1, 0xffffffff)))


def ipv6():
    # Prefix/L: fd
    # Global ID: 641f04c2ce
    # Subnet ID: b81a
    # Combine/CID: fd64:1f04:c2ce:b81a::/64
    # IPv6 addresses: fd64:1f04:c2ce:b81a::/64:XXXX:XXXX:XXXX:XXXXStart
    # Range: fd64:1f04:c2ce:b81a:0:0:0:0
    # End Range: fd64:1f04:c2ce:b81a:ffff:ffff:ffff:ffff
    # No. of hosts: 18446744073709551616
    pass


def areacode(state=None):
    """Returns a random zipcode from a list of US zipcodes.

    Argument:
      state (str): 2 letter state abbreviation.

    Returns:
      areacode (unicode): 3 digit area code.

    Examples:
      >>> areacode()
      '810'
      >>> areacode('NY')
      '718'
    """
    if state:
        cmd = 'SELECT areacode, state FROM areacodes WHERE state = :_state ' \
              'ORDER BY RANDOM() LIMIT 1;'
        res = engine.execute(text(cmd), _state=state)
    else:
        res = engine.execute(
            'SELECT areacode, state FROM areacodes ORDER BY random() LIMIT 1;'
        )
    return AttrDict([dict(d) for d in res.fetchall()][0])


def calling_code(country=False):
    """Produces a calling code from a list of global calling codes.

    Returns:
      country (str): The country which corresponds to the calling code.
      calling_code (str): A variable length calling code.

    Example:
      >>> calling_code()
      AttrDict({u'calling_code': '961', 'country': u'Lebanon'})
      >>> calling_code("Denmark")
      AttrDict({u'calling_code': '45', 'country': u'Denmark'})
      >>> calling_code().country
      u'Guinea'
    """
    if country:
        cmd = 'SELECT country, calling_code FROM calling_codes WHERE ' \
            'country LIKE :_country LIMIT 1;'
        res = engine.execute(text(cmd), _country=country)
    else:
        res = engine.execute(
            'SELECT country, calling_code FROM calling_codes ORDER BY '
            'random() LIMIT 1;'
        )
    return AttrDict([dict(d) for d in res.fetchall()][0])


def number(length=1):
    """Produces a random number or the specified length, from 0-9.

    Argument:
      length int: The length of the string you want.

    Returns:
      str: A randomized number that corresponds to your length.

    Examples:
      >>> number()
      '9'
      >>> number(10)
      '1928520293'
    """
    return ''.join(str(randrange(0, 10)) for _ in range(length))


def phone_number(state=None):
    """Generates a phone number in multiple formats.

    Conforms to NANP standards.

    Argument:
      state (string): Returns a phone number from an areacode in this
      specified state.

    Returns:
      areacode (string): 3 digit area code.
      domestic (string): Phone number formatted to the domestic dial standard.
      international (string): Phone number formatted to the international
      dial standard.
      local (string): Phone number formatted to the local dial standard.
      plain (string): Phone number without formatting.
      standard (string): Phone number formatted to the standard dial standard.
      state (string): The state the phone number corresponds to.

    Examples:
      >>> phone_number()
      AttrDict({
        'areacode': '562',
        'domestic': '(562) 422-9802',
        'international': '+1-562-422-9802',
        'local': '422-9802',
        'plain': '5624229802',
        'standard': '562-422-9802'
        'state': u'CA',
      })
      >>> phone_number().state
      'NY'
      >>> phone_number().international
      '+1-574-720-9722'
      >>> phone_number("NY").domestic
      '718-288-1000'
    """
    data = {}
    valid_number = False
    invalid_prefixes = ["911", "555", "311", "411"]

    # If the number that we generate appears in the invalid_prefixes
    # list, then we will regenerate until the chosen number is not.
    a, b, c = (False,) * 3
    while not valid_number:
        a = str(areacode(state).areacode) if state else str(
            areacode().areacode)
        b = str(randint(2, 9)) + str(number(2))
        if a or b not in invalid_prefixes:
            break

    # Tack on 4 digits to the end.
    c = number(4)

    # Enter our data in to a dict.
    data["areacode"] = a
    data["local"] = "{0}-{1}".format(b, c)
    data["domestic"] = "({0}) {1}-{2}".format(a, b, c)
    data["international"] = "+1-{0}-{1}-{2}".format(a, b, c)
    data["standard"] = "{0}-{1}-{2}".format(a, b, c)
    data["plain"] = a + b + c

    if state:
        cmd = 'SELECT state FROM areacodes WHERE state = :_state'
        res = engine.execute(text(cmd), _state=state)
        for d in res.fetchall():
            data["state"] = d[0]

    return AttrDict(data)


def barcode(specification="EAN-8"):
    """Generates a barcode based on barcode specifications.

    Arguments:
      EAN-8 (str): 8 numerical digits.
      EAN-13 (str): 13 numerical digits.
      UPC-A (str): Used on products at the point of sale

    Notes:
      Unsupported, but in-progress:
      UPC-B - Developed for the US National Drug Code; used to identify drugs
      UPC-E - Used on smaller products where 12 digits dont fit
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


def screename(service="any"):
    # Todo: Re-write
    """
    Makes screenames for the service you pick.
    The screenames conform to their rules, such as
    aol screenames are 3-16 in length with @aol.com on the end.
    Options include: nil, aol, aim, skype, google
    """
    service = "aim" if not service else service

    def _make_name(a, b):
        s = ""
        length = choice(range(a, b))
        choices = ''.join([digits, ascii_letters])
        for _ in range(length):
            s += choice(choices)
        return s

    if service in ['aim', 'aol']:
        return _make_name(3, 16)

    if service == 'skype':
        pre = choice(ascii_uppercase)
        post = _make_name(5, 31)
        return pre + post

    if service is 'google':
        return _make_name(1, 19) + '@googletalk.com'

    return "any_make_name(8, 20)"


def foreign_characters(i):
    foreign_chars = (
        u'ƒŠŒŽšœžŸÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕ\
        ÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ'
    )
    return ''.join(choice(foreign_chars) for _ in range(i))


def special_characters(i):
    """
    This function will pick x amount of special chars from the list below.
    ie - picka.special_characters() = '@%^$'.
    """

    return ''.join(choice(punctuation) for _ in range(i))


def timezone_offset(dst=True, utc=True):
    # Todo: Set both to false by default.
    """Generates a random timezone offset.

    Arguments:
      dst (bool): Enable dst selection.
      utc (bool): Enable utc offset.

    Returns:
      dst: Returns a dst offset.
      utc: Returns a utc offset.

    Examples:
      >>> timezone_offset()
      {'utc': u'+06:30', 'dst': u'-03:00'}
      >>> timezone_offset(dst=False)
      {'utc': u'+10:00'}
      >>> timezone_offset(utc=False)
      {'dst': u'-03:00'}
      >>> timezone_offset(utc=False, dst=False)
      {}
      >>> timezone_offset(utc=False).dst
      '-4:30'
    """
    data = {}
    if dst:
        res = engine.execute("SELECT DISTINCT(dst) FROM timezones ORDER BY "
                             "random() LIMIT 1;")
        data["dst"] = res.fetchall()[0][0]

    if utc:
        res = engine.execute("SELECT DISTINCT(utc) FROM timezones ORDER BY "
                             "random() LIMIT 1;")
        data["utc"] = res.fetchall()[0][0]

    return AttrDict(data)


def timezone_offset_country():
    """Generates a random country from the timezone country list.

    Returns:
      country (str): Name of the generated country.

    Examples:
      >>> timezone_offset_country()
      AttrDict({'country': u'Maldives'})
      >>> timezone_offset_country().country
      AttrDict({'country': u'Maldives'})
    """
    res = engine.execute("SELECT country FROM timezones ORDER BY random() "
                         "LIMIT 1;")
    return AttrDict({"country": res.fetchall()[0][0]})


def lat_long(state="NY", radius=150000):
    """Generates a random latitude, and longitude.

    The lat and long will be within the radius, of the state of your choice.

    Note: The radius seems to need to be over 150,000 to produce a difference
    from the original lat and long.

    Arguments:
      state (str): The 2 letter abbreviation for the state of your choosing.
      radius (int): The radius which will be used to generate a lat and long
      inside of.

    Returns:
      abbrev (string): The 2 letter abbreviation of the chosen state.
      lat (string): A generated latitude of varying length.
      long (string): A generated longetude of varying length.

    Examples:
      >>> d_gen.lat_long("NY", 150000)
      AttrDict({
        u'lat': '41.9656885445',
        u'abbrev': u'NY',
        u'long': '-75.9459285158'
      })
      >>> lat_long("NY", 175000).lat
      '43.0438318157'
    """
    cmd = 'SELECT abbrev,lat,long FROM us_s_ll WHERE abbrev = :_st LIMIT 1;'
    res = engine.execute(text(cmd), _st=state)
    data = AttrDict([dict(d) for d in res.fetchall()][0])

    radius_in_degrees = radius / 111300

    x0 = float(data["long"])
    y0 = float(data["lat"])

    u = round(uniform(0.1, 1.0), 6)
    v = round(uniform(0.1, 1.0), 6)

    w = radius_in_degrees * sqrt(u)
    t = 2 * pi * v
    x = w * cos(t)
    y1 = w * sin(t)
    x1 = x / cos(y0)

    obj = LatLon(y0 + y1, x0 + x1).to_string()
    data["lat"] = obj[0]
    data["long"] = obj[1]

    return data


def month():
    """Generates a month.

    Returns:
      month (str): Full month name.

    Example:
      >>> month()
      'October'
    """
    return choice(month_name[1:])


def month_day():
    """Generates a month and day.

    Note:
      The chosen day will fall within the max days of the chosen month.

    Example:
      >>> month_day()
      'June 26'
    """

    data = AttrDict({"month": month()})

    if data.month in ['January', 'March', 'May', 'July', 'August', 'October',
                      'December']:
        data["day"] = str(randrange(1, 32))
    if data.month in 'February':
        data["day"] = str(randrange(1, 29))
    else:
        data["day"] = str(randrange(1, 31))
    return data


def month_day_year(start=1900, end=2010):
    """Generates a month, day and year.

    Arguments:
      start (int): Beginning of the range used for choosing a year.
      end (int): End of the range used for choosing a year.

    Returns:
      .month (str): The generated month.
      .day (str): The generated day.
      .year (str): The generated year.

    Examples:
      >>> month_day_year(start=1900, end=2015)
      AttrDict({'month': 'December', 'day': '21', 'year': '2009'})
    """
    data = month_day()
    data["year"] = str(randrange(start, end + 1))
    return AttrDict(data)


def timestamp(formatting=None):
    """Generates timestamps based on localtime().

    Note:
      This will create a timestamp for the current time.

    Argument:
      formatting (str): The strftime format you would like.

    Examples:
      >>> timestamp()
      '12:28:59PM 07/20/10'
      >>> timestamp("%H:%M:%S")
      '12:28:59'
    """

    if not formatting:
        return strftime('%H:%M:%S%p %x', localtime())
    else:
        return strftime(formatting, localtime())


def age(min_year=1900, max_year=2015):
    """Generates an age, and related data.

    Arguments:
      min_year (int): Minimum year to use in range.
      max_year (int): Maximum year to use in range.

    Returns:
      A dict containing multiple age related values.

    Raises:
      InvalidRange if min_year is less than max_year.

    Examples:
      >>> age()
      {
        'datetime': datetime.datetime(1916, 1, 5, 5, 47, 47, 564468),
        'day': '05',
        'month_digit': '1',
        'month_short': 'Jan',
        'period': 'AM',
        'pretty_date': 'January 05, 1916',
        'time': '05:01',
        'year': '1916',
        'years_old': '99',
      }
      >>> age().datetime.strftime("%B, %d %Y")
      'June, 20 2005'
      >>> age().day
      '09'
    """
    # The minimum year should be greater than the maximum year.
    if max_year < min_year:
        raise InvalidRange("min_year: %s must be greater than max_year: %s" % (
            min_year, max_year)
                           )

    d = {}
    date_now = datetime.now()
    _b = birthdate(min_year, max_year, custom_strftime="DTO")

    d["datetime"] = _b
    d["pretty_date"] = _b.strftime("%B %d, %Y")
    d["time"] = _b.strftime("%I:%M")
    d["period"] = _b.strftime("%p")
    d["years_old"] = str(relativedelta(date_now, _b).years)
    d["month_short"] = _b.strftime("%b")
    d["month_digit"] = _b.strftime("%m")
    d["day"] = _b.strftime("%d")
    d["year"] = _b.strftime("%Y")

    return AttrDict(d)


def name(sex=None):
    """Generates a name.

    Generates a name of a specified gender, or random gender.

    Argument:
      sex (str):
      sex='m'  Male
      sex='f'  Female
      sex=None Male or Female

    Returns:
      A string.

    Examples:
      >>> name("m")
      'Anthony'
      >>> name("f")
      'Jessica'
      >>> name()
      'Michael'
      >>> name()
      'Louise'
    """
    _first = [initial(period=True).upper(), set_of_initials(2)[0]]
    _middle = ["", initial(period=True), set_of_initials(2)[0]]
    _surname = [surname(), "%s-%s" % (surname(), surname())]
    if sex.lower.startswith("m"):
        _first.append(male())
        _middle.append(male())
    else:
        _first.append(female())
        _middle.append(female())
    return AttrDict({
        "first": unicode(choice(_first)),
        "middle": unicode(choice(_middle)),
        "last": unicode(choice(_surname))
    })


def male():
    """Generate a 'male' name.

    Returns:
      A string.

    Example:
      >>> name()
      'Anthony'
    """
    res = engine.execute("SELECT name FROM male ORDER BY random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


def birthdate(min_year=1900, max_year=2015, custom_strftime=None):
    """Generates a birthdate.

    Arguments:
      min_year (int): Minimum year to use in range.
      max_year (int): Maximum year to use in range.
      custom_strftime (str): Applies strftime to object.

    Returns:
      with custom_strftime (str):
      A string based on your strftime arguments.

      without custom_strftime (AttrDict):
      A datetime object which includes: datetime, month, day, and year

    Examples:
      >>> birthdate()
      datetime.datetime(1903, 12, 23, 10, 46, 55, 140438)
      >>> birthdate(max_year=1950)
      datetime.datetime(1928, 6, 20, 12, 26, 17, 27057)
      >>> birthdate(custom_strftime="%m/%d/%Y")
      '07/07/2002'
      >>> x = birthdate()
      >>> x.month, x.day, x.year
      (11, 1, 1981)
      >>> birthdate(custom_strftime="%B")
      'Februrary'
    """
    data = {}

    y = randrange(min_year, max_year + 1)
    m = randrange(1, 13)
    d = randrange(1, monthrange(y, m)[1] + 1)
    h = randint(1, 12)
    mn = randint(1, 59)
    s = randint(1, 59)
    ms = "%.6i" % randint(1, 999999)

    generated_datetime = datetime(y, m, d, h, mn, s, int(ms))

    if custom_strftime:
        if custom_strftime is not "DTO":
            return generated_datetime.strftime(custom_strftime)
        else:
            return generated_datetime

    data["datetime"] = generated_datetime
    data["year"] = generated_datetime.strftime("%Y")
    data["month"] = generated_datetime.strftime("%m")
    data["day"] = generated_datetime.strftime("%d")

    return AttrDict(data)


def email(length=8, domain='@example.com'):
    # todo: remove args on length and domain.
    """Generates an email address."""
    return AttrDict(
        {
            "length": length,
            "domain": domain,
            "email": ''.join(choice(
                ascii_lowercase) for _ in range(
                length)) + domain
        }
    )


def password(case='mixed', length=6, output_format='letters',
             special_chars=False):
    choices = ''
    if output_format in ['letters', 'alphanumeric']:
        cases = {
            'upper': ascii_uppercase,
            'mixed': ascii_letters,
            'lower': ascii_lowercase
        }
        choices += cases[case]
    if output_format in ['numbers', 'alphanumeric']:
        choices += digits
    if special_chars:
        choices += punctuation
    output = ''
    for _ in xrange(length):
        output += choice(choices)
    return output


def url(i, extension='.com'):
    """Produces a URL."""
    return email(i, extension)


def mac_address():
    """Produces a MAC address"""
    mac = [
        0x00, 0x16, 0x3e,
        randint(0x00, 0x7f),
        randint(0x00, 0xff),
        randint(0x00, 0xff)
    ]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def gender(extended=False):
    """Returns a random gender.

    Argument:
      extended (bool): Returns from Female or Male if False.
      if True, returns from 50+ genders.
    """
    if extended:
        res = engine.execute("SELECT gender FROM gender_extended "
                             "ORDER BY random() LIMIT 1;")
        return AttrDict([dict(x) for x in res.fetchall()][0])
    else:
        return choice(['Male', 'Female'])


def language():
    """Picks a random language."""
    res = engine.execute(
        "SELECT name FROM languages ORDER BY random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


def social_security_number(state="NY"):
    """Produces a US Social Security Number.

    Example:
      social_security_number() => '112-32-3322'

    >>> assert len(social_security_number()) == 11
    """
    x = choice(picka_utils.ssn_prefixes(state))
    return '{0}-{1}-{2}'.format(
        randrange(x[0], x[1] + 1),
        number(2),
        number(4)
    )


def drivers_license(state='NY'):
    """Generates drivers license numbers.

     The generated numbers adhere to the standard format for each
     state.

    Args:
      state (str, optional): Two letter state code.

    Returns:
      str: generated license code.

    Examples:
        >>> drivers_license()
        "I370162546092578729"
        >>> drivers_license("AL")
        "2405831"
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
        i = choice([randint(1, 7), 12])
        return password(
            case="upper",
            length=i,
            output_format="alphanumeric",
            special_chars=False
        )
    n = choice(lengths[state])
    s = ""
    s += picka_utils.random_string(length=n[0])
    s += number(length=n[1])

    if len(n) > 2:
        if state == "ID":
            s += picka_utils.random_string()
        if state == "IA":
            s += picka_utils.random_string(length=n[2])
            s += number(n[3])
        if state == "KS":
            s += picka_utils.random_string(n[2])
            s += number(n[3])
            s += picka_utils.random_string(n[4])
        if state == "MO":
            s += "R" if n[2] == "R" else picka_utils.random_string(n[2])
        if state == "NH":
            s += number(n[3])

    if state == "NV" and n == [1, 8]:
        s = s.replace(s[0], "X")
    if state == "VT" and n == [0, 7, "A"]:
        s = s.replace(s[-1], "A")
    return "{0}".format(s)


def business_title():
    """This will produce a random business title.

    :parameters:
        abbreviated: (boolean)
            Do you want abbreviated titles?

    This function will return business titles. \
    :tip: They are generic business titles.

    """
    primary = [
        'Lead', 'Senior', 'Direct', 'Corporate', 'Dynamic',
        'Future', 'Product', 'National', 'Global', 'Customer',
        'Investor', 'Dynamic', 'International', 'Principal'
    ]
    secondary = [
        'Supervisor', 'Associate', 'Executive', 'Liason', 'Officer',
        'Manager', 'Engineer', 'Specialist', 'Director', 'Coordinator',
        'Assistant', 'Facilitator', 'Agent', 'Representative', 'Strategist',
    ]
    return '{} {}'.format(choice(primary), choice(secondary))


def business_title_abbreviation():
    return choice(['COO', 'CEO', 'CFO', 'VP', 'EVP'])


def career():
    """This function will produce a career."""
    res = engine.execute("SELECT name FROM careers ORDER BY random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


def company_name():
    """This function will return a company name"""
    res = engine.execute(
        "SELECT name FROM companies ORDER BY random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


def creditcard(card_type=None):
    # Todo: docstring and return AttrDict
    card_types = {
        'amex': {
            'prefixes': ['34', '37'],
            'length': [15]
        },
        'diners-carte-blance': {
            'prefixes': [300, 301, 302, 304, 305],
            'length': [14],
        },
        'diners-international': {
            'prefixes': [36],
            'length': [14]
        },
        'diners-uscanada': {
            'prefixes': [54, 55],
            'length': [16]
        },
        'discover': {
            'prefixes': ['6011'] + [str(i) for i in range(622126, 622926)] + [
                '644', '645', '646', '647', '648', '649', '65'],
            'length': [16]
        },
        'jcb': {
            'prefixes': [str(i) for i in range(3528, 3590)],
            'length': [16]
        },
        'laser': {
            'prefixes': ['6304', '6706', '6771', '6709'],
            'length': range(16, 20)
        },
        'maestro': {
            'prefixes': [
                '5018', '5020', '5038', '6304', '6759',
                '6761', '6762', '6763'
            ],
            'length': range(12, 20)
        },
        'mastercard': {
            'prefixes': ['51', '52', '53', '54', '55'],
            'length': [16]
        },
        'solo': {
            'prefixes': ['6334', '6767'],
            'length': [16, 18, 19]
        },
        'switch': {
            'prefixes': [
                '4903', '4905', '4911', '4936', '564182',
                '633110', '6333', '6759'
            ],
            'length': [16, 18, 19]
        },
        'visa': {
            'prefixes': ['4'],
            'length': [16]
        },
        'visa-electron': {
            'prefixes': [
                '4026', '417500', '4508', '4844', '4913',
                '4917'
            ],
            'length': [16]
        }
    }

    def _return_int(*args):
        return [int(_i) for _i in list(*args)]

    card_name = card_type if card_type else choice(card_type.keys())
    if not card_type:
        card_name = choice(card_types.keys())

    length = card_types[card_name]['length'][0]
    result = choice(card_types[card_name]['prefixes'])

    result += ''.join(
        str(choice(range(10))) for _ in range(
            length - len(result) - 1)
    )

    total = sum(_return_int(result[-2::-2])) + sum(_return_int(
        ''.join([str(i * 2) for i in _return_int(result[::-2])]))
    )
    check_digit = ((total / 10 + 1) * 10 - total) % 10
    return '%s%s' % (result, check_digit)


def cvv(i):
    """Returns a cvv, based on the length you provide."""
    return '{}'.format(randint(111, (999 if i == 3 else 9999)))


def street_name():
    """Produces a street name."""
    res = engine.execute("SELECT name FROM streetnames "
                         "ORDER BY random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


def street_address():
    """This function will produce a complete street address."""
    return choice(
        [
            '%d-%d %s %s' % (
                randrange(999),
                randrange(999),
                street_name().name,
                street_type().name
            ),
            '%d %s %s' % (
                randrange(999),
                street_name().name,
                street_type().name
            ),
            '%s %d, %s %s' % (
                'P.O. Box',
                randrange(999),
                street_name().name,
                street_type().name
            )
        ]
    )


def street_type():
    """This function will return a random street type."""
    res = engine.execute("SELECT name FROM us_street_types "
                         "ORDER BY random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


def apartment_number():
    """
    Returns an apartment type, with a number.

    :tip: There are many different types which could be returned.
    If you are looking for a specific format, you might be interested\
    in using string formatting instead.
    """
    _type = choice(['Apt.', 'Apartment', 'Suite', 'Ste.'])
    letter = choice(ascii_letters).capitalize()
    directions = ['E', 'W', 'N', 'S']
    short = '{} {}'.format(_type, randint(1, 999))
    _long = '{} {}{}'.format(_type, randint(1, 999), letter)
    alt = '{} {}-{}{}'.format(_type, choice(directions),
                              randint(1, 999), letter)
    return AttrDict(
        {
            "apartment_number": choice([short, _long, alt])
        }
    )


def city():
    """This function will produce a city."""
    res = engine.execute("SELECT city FROM us_cities "
                         "ORDER BY random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


def city_with_state():
    """
    This function produces a city with a state.
    ie - city_with_state() = 'New York, NY'
    """
    res = engine.execute("SELECT city, state FROM us_cities "
                         "ORDER BY random() LIMIT 1;")
    return ', '.join(res.fetchall()[0])


def state_abbreviated():
    """
    This function produces just a state abbreviation.
    eg - state_abbreviated() = 'NY'
    """
    res = engine.execute("SELECT abbreviation FROM states "
                         "ORDER BY random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


def zipcode(state=None):
    """This function will pick a zipcode randomnly from a list.
    eg - zipcode() = '11221'.
    """
    range_gen = []
    state = state or state_abbreviated().abbreviation
    cmd = 'SELECT min, max FROM zipcodes WHERE st = :_state'
    res = engine.execute(text(cmd), _state=state)
    _range = res.fetchall()
    for r in _range:
        range_gen.extend(range(int(r[0]), int(r[1] + 1)))
    return '%05d' % choice(range_gen)


def country():
    """This function will return a random country."""
    res = engine.execute("SELECT country_name FROM countries "
                         "ORDER BY random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


def salutation():
    """This function will return a 'Mr.' or 'Mrs.'"""
    return choice(['Mr.', 'Mrs.', 'Miss', 'Dr.', 'Prof.', 'Rev.'])


def female():
    """Returns a randomly chosen female first name."""
    res = engine.execute("SELECT name FROM female ORDER BY random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


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
    return "{0}{1}".format(
        choice(ascii_uppercase), "." if period else ""
    )


def set_of_initials(i=3):
    """Returns initials with period seperators."""
    return [''.join(initial(True) for _ in xrange(i))]


def surname():
    """Returns a randomly chosen surname."""
    res = engine.execute("SELECT name FROM surname "
                         "ORDER BY random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


def hyphenated_last_name():
    """
    This function will pick 2 random last names and hyphenate them.
    ie - hyphenated_last_name() = 'Perry-Jenkins'
    """

    return '{}-{}'.format(surname(), surname())


def suffix():
    """This returns a suffix from a small list."""
    return choice(
        [
            'Sr.', 'Jr.', 'II', 'III', 'IV', 'V', 'VI',
            'VII', 'VIII', 'IX', 'X'
        ]
    )


def unit_type():
    res = engine.execute(
        "SELECT name, abbreviation FROM us_unit_types "
        "ORDER BY random() LIMIT 1;"
    )
    return AttrDict([dict(d) for d in res.fetchall()][0])


def ssn_prefixes(state):
    states = {
        "AL": [[416, 424]],
        "AK": [[574, 574]],
        "AR": [[429, 432], [676, 679]],
        "AZ": [[526, 527], [600, 601]],
        "CA": [[1, 7], [545, 573], [602, 626]],
        "CO": [[521, 524], [650, 653]],
        "CT": [[40, 49]],
        "DE": [[221, 222]],
        "FL": [[261, 267], [589, 595], [766, 772]],
        "GA": [[252, 260], [667, 675]],
        "HI": [[575, 576], [750, 751]],
        "ID": [[518, 519]],
        "IL": [[318, 361]],
        "IN": [[303, 317]],
        "IA": [[478, 485]],
        "KS": [[509, 515]],
        "KY": [[400, 407]],
        "LA": [[433, 439], [659, 665]],
        "ME": [[4, 7]],
        "MD": [[212, 220]],
        "MA": [[10, 34]],
        "MI": [[362, 386]],
        "MN": [[468, 477]],
        "MS": [[425, 428], [587, 588], [752, 755]],
        "MO": [[468, 500]],
        "MT": [[516, 517]],
        "NE": [[505, 508]],
        "NV": [[530, 680]],
        "NH": [[1, 3]],
        "NJ": [[135, 158]],
        "NM": [[525, 585], [648, 649]],
        "NY": [[50, 134]],
        "NC": [[237, 246], [681, 690]],
        "ND": [[501, 501]],
        "OH": [[268, 302]],
        "OK": [[440, 448]],
        "OR": [[540, 544]],
        "PA": [[159, 211]],
        "RI": [[035, 39]],
        "SC": [[247, 251], [654, 658]],
        "SD": [[504, 504]],
        "TN": [[408, 415], [756, 763]],
        "TX": [[449, 467], [627, 645]],
        "UT": [[528, 529], [646, 647]],
        "VT": [[8, 9]],
        "VI": [[223, 231], [232, 236]],
        "WA": [[531, 539]],
        "WV": [[232, 236]],
        "WI": [[387, 399]],
        "WY": [[520, 520]]
    }
    return states[state]


def random_string(length=1, case='upper'):
    """
    This will allow you to enter an integer, and create 'i' amount
    of characters. ie: random_string(7) = DsEIzCd
    """
    choices = ''
    output = ''
    cases = {
        'upper': ascii_uppercase,
        'lower': ascii_lowercase,
        'mixed': ascii_letters
    }
    choices += cases[case]
    for _ in xrange(length):
        output += choice(choices)
    return output


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

    import os
    _path = os.path.join(os.path.abspath(os.path.dirname(
        __file__)) + "/data/book_sherlock.txt")
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
            i = randint(0, max_index)
            yield sentences[i]


def _split_sentences(text):
    # from pyteaser: https://github.com/xiaoxu193/PyTeaser
    # see `pyteaser.split_sentences()`
    fragments = split('(?<![A-Z])([.!?]"?)(?=\s+\"?[A-Z])', text)
    return map("".join, izip(*[iter(fragments[:-1])] * 2))


def sentence(num_words=20, chars=''):
    """
    Returns a sentence based on random words from The Adventures of
    Sherlock Holmes that is no more than `chars` characters in length
    or `num_words` words in length.
    """
    word_list = _Book.get_text().split()
    words = ' '.join(choice(word_list) for _ in
                     xrange(num_words))
    return words if not chars else words[:chars]


def sentence_actual(min_words=3, max_words=1000):
    """
    Returns a sentence from The Adventures of Sherlock Holmes
    that contains at least `min_words` and no more than `max_words`.
    """
    _rewhite = compile(r"\s+")
    _rewhitesub = partial(_rewhite.sub, "")
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


def trash(picka_function):
    """
     :Summary: This method takes a function you pass in, and joins\
     the output with _random punctuation.
     :Date: Tue Feb 22 15:31:12 EST 2011.
     :Usage: picka.trash(picka.name) >>> 'D#o}y>l~e^'
    """
    return ''.join([str(char) + choice(str(punctuation))
                    for char in picka_function()])


# noinspection PyUnresolvedReferences
def image(filepath, length=250, width=250, a=0):
    """Generate a _random colored image, with _random text on it.
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
    im = Image.new(
        'RGBA',
        tuple((length, width)),
        tuple((rgba(format="list", a=0)))
    )
    draw = ImageDraw.Draw(im)
    text = sentence_actual(1)
    draw.text((0, 0), text, fill=tuple(rgb(format="list")))
    im.save(filepath)
    return filepath


def color():
    return choice([
        "brown", "red", "blue", "green", "white", "black", "purple"
    ])


def pokemon():
    return choice([
        "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon",
        "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie",
        "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill",
        "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate",
        "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu",
        "Sandshrew", "Sandslash", "Nidoran♀", "Nidorina", "Nidoqueen",
        "Nidoran♂", "Nidorino", "Nidoking", "Clefairy", "Clefable",
        "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat",
        "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect",
        "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth",
        "Persian", "Psyduck", "Golduck", "Mankey", "Primeape",
        "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra",
        "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout",
        "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude",
        "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke",
        "Slowbro", "Magnemite", "Magneton", "Farfetch’d", "Doduo",
        "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder",
        "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee",
        "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute",
        "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan",
        "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon",
        "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen",
        "Seaking", "Staryu", "Starmie", "Mr. Mime",
        "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros",
        "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon",
        "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto",
        "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos",
        "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo",
        "Mew", "Chikorita", "Bayleef", "Meganium",
        "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw",
        "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba",
        "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn",
        "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu",
        "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill",
        "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom",
        "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon",
        "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown",
        "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce",
        "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor",
        "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring",
        "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid",
        "Octillery", "Delibird", "Mantine", "Skarmory",
        "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2",
        "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid",
        "Magby", "Miltank", "Blissey", "Raikou", "Entei", "Suicune",
        "Larvitar", "Pupitar", "Tyranitar", "Lugia", "Ho-Oh", "Celebi",
        "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken",
        "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena",
        "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon",
        "Dustox", "Lotad", "Lombre", "Ludicolo",
        "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull",
        "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain",
        "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada",
        "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita",
        "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye",
        "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham",
        "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise",
        "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer",
        "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig",
        "Spinda", "Trapinch", "Vibrava", "Flygon",
        "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper",
        "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt",
        "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo",
        "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette",
        "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol", "Wynaut",
        "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl",
        "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon",
        "Shelgon", "Salamence", "Beldum", "Metang", "Metagross",
        "Regirock", "Regice", "Registeel", "Latias", "Latios", "Kyogre",
        "Groudon", "Rayquaza", "Jirachi", "Deoxys", "Turtwig", "Grotle",
        "Torterra", "Chimchar", "Monferno", "Infernape",
        "Piplup", "Prinplup", "Empoleon", "Starly", "Staravia",
        "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune",
        "Shinx", "Luxio", "Luxray", "Budew", "Roserade", "Cranidos",
        "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam",
        "Mothim", "Combee", "Vespiquen", "Pachirisu", "Buizel",
        "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom",
        "Drifloon", "Drifblim", "Buneary", "Lopunny", "Mismagius", "Honchkrow",
        "Glameow", "Purugly", "Chingling", "Stunky",
        "Skuntank", "Bronzor", "Bronzong", "Bonsly", "Mime Jr.",
        "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp",
        "Munchlax", "Riolu", "Lucario", "Hippopotas", "Hippowdon",
        "Skorupi", "Drapion", "Croagunk", "Toxicroak",
        "Carnivine", "Finneon", "Lumineon", "Mantyke", "Snover",
        "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior",
        "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega",
        "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z",
        "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom", "Uxie",
        "Mesprit", "Azelf", "Dialga", "Palkia", "Heatran", "Regigigas",
        "Giratina", "Cresselia", "Phione", "Manaphy", "Darkrai", "Shaymin",
        "Arceus", "Victini", "Snivy", "Servine", "Serperior",
        "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott",
        "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland",
        "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear",
        "Panpour", "Simipour", "Munna", "Musharna", "Pidove",
        "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola",
        "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill",
        "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole",
        "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle",
        "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede",
        "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin",
        "Sandile", "Krokorok", "Krookodile", "Darumaka",
        "Darmanitan", "Maractus", "Dwebble", "Crustle", "Scraggy",
        "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga",
        "Carracosta", "Archen", "Archeops", "Trubbish",
        "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino", "Gothita",
        "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus",
        "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe",
        "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier",
        "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola",
        "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink",
        "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross",
        "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew",
        "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal",
        "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao",
        "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp",
        "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz",
        "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta",
        "Volcarona", "Cobalion", "Terrakion", "Virizion", "Tornadus",
        "Thundurus", "Reshiram", "Zekrom ", "Landorus",
        "Kyurem", "Keldeo", "Meloetta", "Genesect", "Chespin",
        "Quilladin", "Chesnaught", "Fennekin", "Braixen", "Delphox",
        "Froakie", "Frogadier", "Greninja", "Bunnelby",
        "Diggersby", "Fletchling", "Fletchinder", "Talonflame",
        "Scatterbug", "Spewpa", "Vivillon", "Litleo", "Pyroar", "Flabebe",
        "Floette", "Florges", "Skiddo", "Gogoat", "Pancham", "Pangoro",
        "Furfrou", "Espurr", "Meowstic", "Honedge", "Doublade", "Aegislash",
        "Spritzee", "Aromatisse", "Swirlix", "Slurpuff", "Inkay", "Malamar",
        "Binacle", "Barbaracle", "Skrelp", "Dragalge", "Clauncher",
        "Clawitzer", "Helioptile", "Heliolisk", "Tyrunt", "Tyrantrum",
        "Amaura", "Aurorus", "Sylveon", "Hawlucha", "Dedenne",
        "Carbink", "Goomy", "Sliggoo", "Goodra", "Klefki", "Phantump",
        "Trevenant", "Pumpkaboo", "Gourgeist", "Bergmite", "Avalugg",
        "Noibat", "Noivern", "Xerneas", "Yveltal", "Zygarde", "Diancie",
        "Hoopa", "Volcanion"
    ])
