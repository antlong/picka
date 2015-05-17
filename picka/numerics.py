from datetime import datetime
from random import randrange, randint
from calendar import monthrange

from sqlalchemy import text
from dateutil.relativedelta import relativedelta
from attrdict import AttrDict

import picka_utils

engine = picka_utils.engine_connection()
asdict = picka_utils.asdict


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
    d = {}
    date_now = datetime.now()
    _b = birthdate(min_year, max_year, formatted="DTO")

    d["datetime"] = _b
    d["pretty_date"] = _b.strftime("%B %d, %Y")
    d["time"] = _b.strftime("%I:%m")
    d["period"] = _b.strftime("%p")
    d["years_old"] = str(relativedelta(date_now, _b).years)
    d["month_short"] = _b.strftime("%b")
    d["month_digit"] = _b.strftime("%m")
    d["day"] = _b.strftime("%d")
    d["year"] = _b.strftime("%Y")

    return AttrDict(d)


def areacode(state=False):
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


def birthdate(min_year=1900, max_year=2015, formatted=None):
    """Generates a birthdate.

    Args:
      min_year (int): Minimum year to use in range.
      max_year (int): Maximum year to use in range.
      formatted (str): Applies strftime to object.

    Returns:
      formatted (str):
      A string based on your strftime arguments.

      unformatted (AttrDict):
      A datetime object which includes: datetime, month, day, and year

    Examples:
      >>> birthdate()
      datetime.datetime(1903, 12, 23, 10, 46, 55, 140438)
      >>> birthdate(max_year=1950)
      datetime.datetime(1928, 6, 20, 12, 26, 17, 27057)
      >>> birthdate(formatted="%m/%d/%Y")
      '07/07/2002'
      >>> x = birthdate()
      >>> x.month, x.day, x.year
      (11, 1, 1981)
      >>> birthdate(formatted="%B")
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

    if formatted:
        if formatted is not "DTO":
            return generated_datetime.strftime(formatted)
        else:
            return generated_datetime

    data["datetime"] = generated_datetime
    data["year"] = generated_datetime.strftime("%Y")
    data["month"] = generated_datetime.strftime("%m")
    data["day"] = generated_datetime.strftime("%d")

    return AttrDict(data)


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
        cmd = 'SELECT country, calling_code FROM calling_codes WHERE country ' \
              'LIKE :_country LIMIT 1;'
        res = engine.execute(text(cmd), _country=country)
    else:
        res = engine.execute(
            "SELECT country, calling_code FROM calling_codes ORDER BY random() "
            "LIMIT 1;"
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
        a = str(areacode(state).areacode) if state else str(areacode().areacode)
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
