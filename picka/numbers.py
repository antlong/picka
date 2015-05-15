from datetime import datetime
from random import randrange, randint
from calendar import monthrange

from attrdict import AttrDict
from dateutil.relativedelta import relativedelta

import db as _db

_query = _db.Queries()
query_single = _query.query_single
query_multiple = _query.query_multiple
query_custom = _query.query_custom


def birthdate(min_year=1900, max_year=2015, formatted=None):
    """Generates a birthdate.

    Args:
      min_year (int): Minimum year to use in range.
      max_year (int): Maximum year to use in range.
      formatted (str): Applies strftime to object.

    Returns:
      formatted: A string based on your strftime.
      no formatting: a datetimeobject.

    Examples:

      >>> print birthdate()
      datetime.datetime(1903, 12, 23, 10, 46, 55, 140438)
      >>> print birthdate(max_year=1950)
      datetime.datetime(1928, 6, 20, 12, 26, 17, 27057)
      >>> print birthdate(formatted="%m/%d/%Y")
      '07/07/2002'
      >>> x = birthdate()
      >>> print x.month, x.day, x.year
      11 1 1981
      >>> birthdate(formatted="%B")
      'Februrary'

    """
    n = datetime.now()
    y = randrange(min_year, max_year + 1)
    m = randrange(1, 13)
    d = randrange(1, monthrange(y, m)[1] + 1)
    h = randint(1, 12)
    mn = randint(1, 59)
    s = randint(1, 59)
    ms = "%.6i" % randint(1, 999999)
    n = n.replace(y, m, d, h, mn, s, int(ms))
    if formatted:
        return n.strftime(formatted)
    return n


def age(min_year=1900, max_year=2015):
    """
    Generates an age, and related data.

    Args:
      min_year (int): Minimum year to use in range.
      max_year (int): Maximum year to use in range.

    Returns:
      A dict containing multiple age related values.

    Examples:
      >>> age()
      {
        'year': '1916',
        'period': 'AM',
        'month_short': 'Jan',
        'month_digit': '1',
        'years_old': 99,
        'time': '05:01',
        'pretty_date': 'January 05, 1916',
        'datetime': datetime.datetime(1916, 1, 5, 5, 47, 47, 564468),
        'day': '05'
      }
      >>> age().datetime.strftime("%B, %d %Y")
      'June, 20 2005'
      >>> age().day
      '09'

    """
    d = {}
    date_now = datetime.now()
    _b = birthdate(min_year, max_year)
    d["datetime"] = _b
    d["pretty_date"] = _b.strftime("%B %d, %Y")
    d["time"] = _b.strftime("%I:%m")
    d["period"] = _b.strftime("%p")
    d["years_old"] = relativedelta(date_now, _b).years
    d["month_short"] = _b.strftime("%b")
    d["month_digit"] = _b.strftime("%m")
    d["day"] = _b.strftime("%d")
    d["year"] = _b.strftime("%Y")
    return d


def calling_code(country=None):
    """Returns a calling code from a list of global calling codes.

    Returns:
      calling code: (str) Variable length calling code.

    Example:
      >>> calling_code()
      '377'
    """
    if country:
        return query_custom('SELECT country, calling_code FROM calling_codes WHERE country LIKE ?', (country,))
        # return query_custom("select * from calling_codes where country LIKE {};".format(country), output=True)
    else:
        return query_single("calling_code", "calling_codes")


def calling_code_with_country():
    """Returns a country, with a calling code as a single string."""
    return query_multiple(
        "country, calling_code",
        "calling_codes",
        output=True
    )


def area_code(state=False):
    """Returns a random zipcode from a list of US zipcodes.

    Argument:
      state: (str) 2 letter state abbreviation.

    Returns:
      areacode: (str) 3 digit area code.

    Examples:
      >>> area_code()
      '810'
      >>> area_code('NY')
      '718'
    """
    if state:
        return query_single("code", "areacodes", "state")
    else:
        return query_single("code", "areacodes")


def phone_number(state=None):
    """Generates a phone number in multiple formats.
    Conforms to NANP standards.

    Argument:
      state: String - 2 letter state abbreviation.

    Returns:
      state: string
      international: string
      areacode: string
      plain: string
      local: string
      domestic: string
      standard: string

    Examples:
      >>> phone_number()
      AttrDict({
        'state': u'CA',
        'international': '+1-562-422-9802',
        'areacode': '562',
        'plain': '5624229802',
        'local': '422-9802',
        'domestic': '(562) 422-9802',
        'standard': '562-422-9802'
      })
      >>> phone_number().state
      "NY"
      >>> phone_number().international
      '+1-574-720-9722'
    """
    data = {}
    valid_number = False
    invalid_prefixes = ["911", "555", "311", "411"]

    # If the number that we generate appears in the invalid_prefixes
    # list, then we will regenerate until the chosen number is not.
    while not valid_number:
        a = str(area_code(state)) if state else str(area_code())
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
    data["state"] = query_single("state", "areacodes", "code", a)

    return AttrDict(data)


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
