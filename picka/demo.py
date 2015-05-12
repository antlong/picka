from random import randrange, randint
from datetime import datetime
from calendar import monthrange


class age(object):
    """Generates age related data.

    Note:
      You must enable the types of data you wish to generate by settings the
      corresponding attribute to True.

    Attributes:
      min (int): minimum year to use in the range.
      max (int): maximum year to use in the range.
      time (bool): True to return a time which can be used as birth time.
      datetime (bool): True to return a randomized datetime object.
      pretty_date (bool): True to return a pretty version of the birth date.
      period (bool): True to return AM or PM.
      years_old (bool): True to return years since generated birth year.
      month_short (bool): True to return a generated year in numeric form.
      month_digit (bool): True to return a generated month in numeric form.
      day (bool): True to return a generated day in numeric form.
      year (bool): True to return a generated year in numeric form.


    Examples:

      >>> picka.age.datetime = True
      >>> picka.age())
      datetime.datetime(1903, 12, 23, 10, 46, 55, 140438)
      >>> picka.age.day = True
      >>> print picka.age()
      {
        'day': '02',
        'datetime': datetime.datetime(1928, 6, 20, 12, 26, 17, 27057)
      }

    """
    _min = 1950
    _max = 1990
    _time = False
    _datetime = False
    _pretty_date = False
    _period = False
    _years_old = False
    _month_short = False
    _month_digit = False
    _day = False
    _year = False

    class __metaclass__(type):
        @property
        def time(cls):
            return cls._time

        @time.setter
        def time(cls, value):
            cls._time = value

        @property
        def min(cls):
            return cls._min

        @min.setter
        def min(cls, value):
            cls._min = value

        @property
        def max(cls):
            return cls._max

        @max.setter
        def max(cls, value):
            cls._max = value

        @property
        def datetime(cls):
            return cls._datetime

        @datetime.setter
        def datetime(cls, value):
            cls._datetime = value

        @property
        def pretty_date(cls):
            return cls._pretty_date

        @pretty_date.setter
        def pretty_date(cls, value):
            cls._pretty_date = value

        @property
        def period(cls):
            return cls._period

        @period.setter
        def period(cls, value):
            cls._period = value

        @property
        def years_old(cls):
            return cls._years_old

        @years_old.setter
        def years_old(cls, value):
            cls._years_old = value

        @property
        def month_short(cls):
            return cls._month_short

        @month_short.setter
        def month_short(cls, value):
            cls._month_short = value

        @property
        def month_digit(cls):
            return cls._month_digit

        @month_digit.setter
        def month_digit(cls, value):
            cls._month_digit = value

        @property
        def day(cls):
            return cls._day

        @day.setter
        def day(cls, value):
            cls._day = value

        @property
        def year(cls):
            return cls._year

        @year.setter
        def year(cls, value):
            cls._year = value


    def __init__(self):
        pass


    def __new__(self):
        self.data = {}
        _b = self._birthdate()
        date_now = datetime.now()

        if age.time:
            self.data["time"] = _b.strftime("%I:%m")

        if age.datetime:
            self.data["datetime"] = _b

        if age.pretty_date:
            self.data["pretty_date"] = _b.strftime("%B %d, %Y")

        if age.period:
            self.data["period"] = _b.strftime("%p")

        if age.years_old:
            self.data["years_old"] = relativedelta(date_now, _b).years

        if age.month_short:
            self.data["month_short"] = _b.strftime("%b")

        if age.month_digit:
            self.data["month_digit"] = _b.strftime("%m")

        if age.day:
            self.data["day"] = _b.strftime("%d")

        if age.year:
            self.data["year"] = _b.strftime("%Y")

        return self.data


    @classmethod
    def _birthdate(self):
        """Generates a randomized datetime object.

        Note:
          This not exposted to the public.

        Attributes:
          min (int): minimum year to use in the range.
          max (int): maximum year to use in the range.

        Example:
          >>> age.min = 1990
          >>> age.max = 2000
          >>> age.year = True
          >>> print age()
          '1994'

        """
        n = datetime.now()
        y = randrange(age.min, age.max + 1)
        m = randrange(1, 13)
        d = randrange(1, monthrange(y, m)[1] + 1)
        h = randint(1, 12)
        mn = randint(1, 59)
        s = randint(1, 59)
        ms = "%.6i" % randint(1, 999999)
        n = n.replace(y, m, d, h, mn, s, int(ms))
        return n


if __name__ == '__main__':
    age.datetime = True
    print age()
    age.time = True
    print age()