from datetime import datetime
from random import randrange, randint
from calendar import monthrange
from dateutil.relativedelta import relativedelta


def birthdate(min_year=1900, max_year=2015, formatted=False):
    """Generates a birthdate.

    Args:
      min_year (int): Minimum year to use in range.
      max_year (int): Maximum year to use in range.
      formatted (str): Applies strftime to object.

    Returns:
      formatted: A string based on your strftime.
      no formatting: a datetimeobject.

    Examples:

      >>> print picka.birthdate()
      datetime.datetime(1903, 12, 23, 10, 46, 55, 140438)
      >>> print picka.birthday(max_year=1950)
      datetime.datetime(1928, 6, 20, 12, 26, 17, 27057)
      >>> print picka.birthdate(formatted="%m/%d/%Y")
      '07/07/2002'
      >>> x = picka.birthdate()
      >>> print x.month, x.day, x.year
      11 1 1981
      >>> picka.birthdate(formatted="%B")
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


def age(min_year=1900, max_year=2015, formatting=False):
    """Generates an age, and related data.

    Args:
      min_year (int): Minimum year to use in range.
      max_year (int): Maximum year to use in range.
      formatted (str): Applies strftime to the object.

    Returns:
      formatting: A string based on your strftime.
      no formatting: A dict containing multiple values.

    Examples:
      >>> picka.age()
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
      >>> picka.age(formatting="%B, %d %Y")
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
