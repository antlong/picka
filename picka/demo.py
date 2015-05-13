from random import randrange, randint
from datetime import datetime
from dateutil import relativedelta
from calendar import monthrange


class AgeGenerator(object):
    def __init__(self):
        self.min = 1950
        self.max = 1990
        self.time = False
        self.datetime = False
        self.pretty_date = False
        self.period = False
        self.years_old = False
        self.month_short = False
        self.month_digit = False
        self.day = False
        self.year = False

    def generate(self):
        data = {}
        birthdate = self.generate_birthdate()
        date_now = datetime.now()

        if self.time:
            data["time"] = birthdate.strftime("%I:%m")

        if self.datetime:
            data["datetime"] = birthdate

        if self.pretty_date:
            data["pretty_date"] = birthdate.strftime("%B %d, %Y")

        if self.period:
            data["period"] = birthdate.strftime("%p")

        if self.years_old:
            data["years_old"] = relativedelta(date_now, birthdate).years

        if self.month_short:
            data["month_short"] = birthdate.strftime("%b")

        if self.month_digit:
            data["month_digit"] = birthdate.strftime("%m")

        if self.day:
            data["day"] = birthdate.strftime("%d")

        if self.year:
            data["year"] = birthdate.strftime("%Y")

        return data

    def generate_birthdate(self):
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
        y = randrange(age.min, age.max + 1)
        m = randrange(1, 13)
        d = randrange(1, monthrange(y, m)[1] + 1)
        h = randint(1, 12)
        mn = randint(1, 59)
        s = randint(1, 59)
        ms = "%.6i" % randint(1, 999999)
        return datetime(y, m, d, h, mn, s, int(ms))

def age():
    a = AgeGenerator()
    return a.generate()

if __name__ == '__main__':
    age.datetime = True
    print age()
    age.time = True
    print age()