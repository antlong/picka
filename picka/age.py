from datetime import datetime
from random import randrange, randint
from calendar import monthrange, month_name
from dateutil.relativedelta import relativedelta

def date_formatter(formatting):
    return date.strftime(formatting)

def birthdate(min_year=1900, max_year=2015, formatting=False):
    """Generates a birthdate.

    :param min_year:
    :param max_year:
    :param formatting:
    :returns: datetime object
    """
    n = datetime.now()
    y = randrange(min_year, max_year + 1)
    m = randrange(1, 13)
    d = randrange(1, monthrange(y, m)[1] + 1)
    h = randint(1, 12)
    mn = randint(1, 59)
    s = randint(1, 59)
    ms = "%.6i" % randint(1, 999999)
    n.replace(y, m, d, h, mn, s, int(ms))
    if formatting:
        return n.strftime(formatting)
    return n


def birthday(min_year=1900, max_year=2015):
    rmonth = randrange(1, 13)
    birthday_month = month_name[rmonth]
    birthday_year = randrange(min_year, max_year + 1)
    birthday_day = monthrange(birthday_year, rmonth)[1]
    return birthday_month, str(birthday_day), str(birthday_year)


def age(min_year=1900, max_year=2015):
    """Returns a random age, from a range.

    :parameters:
        min_year: (integer)
            The lowest integer to use in the range
        max_year: (integer)
            The highest integer to use in the range

    :tip:
        If min and max are empty, 1 and 99 will be used.


    Birth day, month, year
    Days since birth
    Time of birth

    """
    d = {}
    date_now = datetime.now()
    _b = birthdate(min_year, max_year)
    born = _b.strftime("%B %d, %Y")
    time_of_birth = _b.strftime("%I:%m %p")
    years_ago = relativedelta(date_now, _b).years
    for i in ["born", "time_of_birth", "years_ago"]:
        d[i] = str(locals()[i])
    return d
