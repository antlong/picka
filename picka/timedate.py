"""Functions which generate data in the time and date categories.

Attributes:
  engine (Engine): The connection to the database.

Notes:
  Corresponding tests are found in picka/tests/test_timedate.py
"""
from random import randrange, choice
from calendar import month_name
from time import strftime, localtime

from attrdict import AttrDict

import picka_utils

engine = picka_utils.engine_connection()


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
