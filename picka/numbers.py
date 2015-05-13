from attrdict import AttrDict
from datetime import datetime
from random import randrange, randint
from calendar import monthrange
from dateutil.relativedelta import relativedelta

import picka_utils as _utils

_query = _utils.query

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
      >>> print birthday(max_year=1950)
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


def age(min_year=1900, max_year=2015, formatting=None):
    """Generates an age, and related data.

    Args:
      min_year (int): Minimum year to use in range.
      max_year (int): Maximum year to use in range.
      formatted (str): Applies strftime to the object.

    Returns:
      formatting: A string based on your strftime.
      no formatting: A dict containing multiple values.

    Examples:
      >>> age()
      {
        'year': '1916',
        'period': 'AM',
        'month_short': 'Jan',
        'month_digit': '1',
        'age': 99,
        'time': '05:01',
        'pretty_date': 'January 05, 1916',
        'datetime': datetime.datetime(1916, 1, 5, 5, 47, 47, 564468),
        'day': '05'
      }
      >>> age(formatting="%B, %d %Y")
      'June, 20 2005'

    """
    d = {}
    date_now = datetime.now()
    _b = birthdate(min_year, max_year)
    if formatting:
        return _b.strftime(formatting)
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


def calling_code():
    """
    Returns a calling code from a list of all known calling codes in \
    the world.
    """
    return _query("calling_code", "countries_and_calling_codes")


def calling_code_with_country():
    """Returns a country, with a calling code as a single string."""
    return _query("*", "countries_and_calling_codes")


def area_code(state=False):
    if state:
        return _query("code", "areacodes", "state")
    else:
        return _query("code", "areacodes")


@_utils.deprecated("picka.phone_number(formatting)")
def fax_number():
    """
    :Summary: Returns a fax (phone) number.
    :Usage: picka.fax_number() >>> 755-463-6544
    """

    return phone_number()


def generate(state=None, extended_display=True):
    """Generate a phone number. Conforms to NANP standards.

      :arg state: Bool
      :arg formatting: local, domestic, or international
    """
    data = {}

    def validate(*args):
        for _ in xrange(11):
            if args:
                a = str(area_code(args[0]))
            b = str(randint(2, 9)) + number(2)
            if (a, b) not in ["911", "555"]:
                break
        return a, b

    a, b = validate(state)
    c = number(4)

    if extended_display:
        data["areacode"] = a
        data["local"] = "{0}-{1}".format(b, c)
        data["domestic"] = "({0}) {1}-{2}".format(a, b, c)
        data["international"] = "+1-{0}-{1}-{2}".format(a, b, c)
        data["standard"] = "{0}-{1}-{2}".format(a, b, c)
        data["plain"] = a + b + c
        data["state"] = _query("state", "areacodes", "code", a)
    return AttrDict(data)


def phone_number(state=None):
    return generate(state)


def number(length=1):
    """This function will produce a random number with as many
    characters as you wish.
    """
    return ''.join(str(randrange(0, 10)) for _ in range(length))
