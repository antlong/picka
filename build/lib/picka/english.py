"""
Picka is a data generation and randomization module which aims to increase
coverage by increasing the amount of tests you _dont_ have to write
by hand.
By: Anthony Long
"""
import string
import random
import time
import sqlite3
import functools
import os
__docformat__ = "restructuredtext en"
connect = sqlite3.connect(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db.sqlite'))
cursor = connect.cursor()

_QUERIES = {
    "us_male_first_names": "select * from american_male_names ORDER BY RANDOM();",
    "us_female_first_names": "select * from american_female_names ORDER BY RANDOM();",
    "us_cities": "select * from american_cities_with_states ORDER BY RANDOM();",
    "countries": "select * from global_countries ORDER BY RANDOM();",
    "us_postal_codes": "select * from american_postal_codes ORDER BY RANDOM();",
    "us_street_types": "select * from american_street_types ORDER BY RANDOM();",
    "us_surnames": "select * from american_surnames ORDER BY RANDOM();",
    "countries_and_calling_codes": "select * from global_countries_and_calling_codes ORDER BY RANDOM();",
}


class _memoized(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            return self.func(*args)
    
    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__
    
    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)
    

@_memoized
def _query(sql):
    cursor.execute(sql)
    return cursor.fetchall()


def age(min=1, max=100):
    """
    Returns a random age, from a range.
    
    :parameters:
        min: (integer)
            The lowest integer to use in the range
        max: (integer)
            The highest integer to use in the range
    
    :tip:
        If min and max are empty, 1 and 100 will be used.
    
    """
    return "%.i" % (random.randint(min, max + 1) if min and max else random.randint(1, 100))


def apartment_number():
    """
    Returns an apartment type, with a number.
    
    :tip: There are many different types which could be returned. If you are looking \
    for a specific format, you might be interested in using string formatting \
    instead.
    
    """
    type = random.choice(["Apt.", "Apartment", "Suite", "Ste."])
    letter = random.choice(string.ascii_letters).capitalize()
    directions = ["E", "W", "N", "S", ]
    short = "{} {}".format(type, random.randint(1, 999))
    long = "{} {}{}".format(type, random.randint(1, 999), letter)
    alt = "{} {}-{}{}".format(type, random.choice(directions), random.randint(1, 999), letter)
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
    abbreviations = [
        "COO", "CEO", "CFO", "VP", "EVP",
    ]
    primary = [
        "Lead", "Senior", "Direct", "Corporate", "Dynamic", "Future",
        "Product", "National", "Global", "Customer", "Investor", "Dynamic",
        "International", "Principal",
    ]
    secondary = [
        "Supervisor", "Associate", "Executive", "Liason", "Officer",
        "Manager", "Engineer", "Specialist", "Director", "Coordinator",
        "Assistant", "Facilitator", "Agent", "Representative", "Strategist",
    ]
    return (random.choice(abbreviations) if abbreviated else '{} {}'.format(
        random.choice(primary), random.choice(secondary)),
    )


def calling_code():
    """
    Returns a calling code from a list of all known calling codes in \
    the world.
    """
    return random.choice(_query(_QUERIES['countries_and_calling_codes']))[1]


def calling_code_with_country(formatting=''):
    """
     :Summary: Returns a country, with a calling code as a single string. If a format is passed in,
     a 2 item object of your choosing will be returned. For example, if you pass in:
     calling_code_with_country(list), we will return a list of 2 items.
    """
    country, calling_code = _query(_QUERIES['countries_and_calling_codes'])[0]
    if formatting is dict:
        return formatting({country: calling_code})
    return formatting([country, calling_code]) if formatting else "{} {}".format(country, calling_code)


def chu():
    return random.choice([
        "Bulbasaur", "Charmander", "Charizard", "Squirtle", 
        "Blastoise", "Rattata", "Spearow", "Pikachu", "Sandslash",
        "Nidorina", "Clefairy", "Vulpix", "Jigglypuff", "Mewtwo", "Mew", ])


def city():
    """This function will produce a city."""
    return city_with_state()[:-4]


def city_with_state():
    """
    This function produces a city with a state.
    ie - city_with_state() = 'New York, NY'
    """
    return random.choice(_query(_QUERIES["us_cities"]))[0]


def country():
    """This function will return a random country."""
    return random.choice(_query(_QUERIES["countries"]))[0].strip()


def creditcard(type):
    if type == 'visa':
        prefix = ['40240071']
    elif type == 'amex':
        prefix = ['34', '37']
    elif type == 'discover':
        prefix = ["6011"]
    elif type == 'mastercard':
        prefix = ['51', '52', '53', '54', '55']
    prefix = random.choice(prefix)
    while len(prefix) < 15:
        prefix = prefix + str(random.randint(0, 9))
    return ''.join(prefix) + "0"


def cvv(i):
    """
     :Summary: Returns a cvv, based on the length you provide.
    
    Usage: picka.cvv(3) or picka.cvv(4)
    """
    return '{}'.format(random.randint(111, (999 if i == 3 else 9999)))


def email(length=8, domain="@example.com"):
    """
     :Summary: Created a randomized email.
     :Usage: picka.email(length=8, domain='@antlong.com') >>> 'aijf39ss@antlong.com'
    """
    return ''.join(random.choice(string.ascii_lowercase) for i in xrange(length)) + domain


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
    return random.choice(_query(_QUERIES["us_female_first_names"]))[0]


def _foreign_characters(a, b):
    """
    This function will pick x amount of foreign chars\
    from the list below, where a is min, and b is max.
    """
    pass


def trash(function):
    """
     :Summary: This method takes a function you pass in, and joins\
     the output with random punctuation.
     :Date: Tue Feb 22 15:31:12 EST 2011.
     :Usage: picka.trash(picka.name) >>> 'D#o}y>l~e^'
    """
    return ''.join([char + random.choice(string.punctuation) for char in function()])


def male_name():
    """This function will return a male first name."""
    return random.choice(_query(_QUERIES["us_male_first_names"]))[0]


def male_full_name():
    return "{} {}".format(
        random.choice(_query(_QUERIES["us_male_first_names"]))[0],
        random.choice(_query(_QUERIES["us_surnames"]))[0],
    )


def male_full_name_w_middle_initial():
    """Returns name, middile initial and last name."""
    try:
        names = _query(_QUERIES["us_male_first_names"])
        surnames = _query(_QUERIES["us_surnames"])
    except KeyError:
        print "Key missing."
    return "%s %s. %s" % (
        random.choice(names)[0],
        random.choice(string.ascii_letters).capitalize(),
        random.choice(surnames)[0],
        )


def gender():
    """
    Returns a random gender.
    """
    return random.choice(["Male", "Female"])


def hyphenated_last_name():
    """
    This function will pick 2 random last names and hyphenate them.
    ie - hyphenated_last_name() = 'Perry-Jenkins'
    """
    return '{}-{}'.format(last_name(), last_name())


def initial():
    """
    This function will return a capitalized letter with a '.'
    ie - A.
    """
    return '{}.'.format(random.choice(string.ascii_letters).capitalize())


def language():
    """Picks a random language."""
    return random.choice(["English", "Spanish", "French", "Chinese", "Japanese"])


def last_name():
    """
    This function will return a last name from a list.
    ie - last_name() = 'Smith'.
    """
    try:
        us_surnames = _query(_QUERIES["us_surnames"])
    except KeyError:
        print "Key missing."
    return random.choice(us_surnames)[0]


def male_middle_name():
    """Picks a middle name from a list of male names."""
    try:
        us_male_first_names = _query(_QUERIES["us_male_first_names"])
    except KeyError:
        print "Key missing."
    return random.choice(us_male_first_names)[0]


def month():
    """
    Selects a month for you.
    """
    months = ["January", "February", "March", "April",
                "May", "June", "July", "August", "September",
                "October", "November", "December"]
    return random.choice(months)


def month_and_day():
    """
    Selects and month and day for you.
    There is logic to handle the days in the month correctly.
    """
    month_choice = month()
    if month_choice in ("January", "March", "May",
            "July", "August", "October", "December"):
        return '%s %s' % (month_choice, random.randrange(1, 32))
    if month_choice in ("February"):
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
    month_and_day_choice = month_and_day()
    return '%s %s' % (month_and_day_choice,
        random.randrange(start, end + 1),)


def name():
    """
    Picks a random name. Could be male, could be female.
    """
    try:
        names = _query(_QUERIES["us_male_first_names"])
        names.append(_query(_QUERIES["us_female_first_names"]))
    except KeyError:
        print "Key missing."
    return random.choice(names)[0]


def number(x, y):
    """
    This function will produce a random number with as many
    characters as you wish.
    """
    return random.randrange(x, y + 1)


def password_alphabetical(i):
    """
    This function will return a randomized password consisting of letters.
    """
    return ''.join(random.choice(string.ascii_letters)
            for x in range(i))


def password_numerical(i):
    """
    This function will return a random password consisting of numbers.
    """
    return ''.join(random.choice(string.digits)
            for x in range(i))


def password_alphanumeric(i):
    """
    This function will return an alphanumeric password.
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for x in range(i))


def phone_number():
    """
    This function will produce a phone number randomnly, with '-'s.
    """
    x = ''.join(str(random.randrange(10)) for i in xrange(10))
    y = "%s-%s-%s" % (x[0:3], x[3:6], x[6:])
    return y


def random_string(i):
    """
    This will allow you to enter an integer, and create 'i' amount
    of characters. ie: random_string(7) = DsEIzCd
    """
    return ''.join(random.choice(string.ascii_letters) for x in xrange(i))


def salutation():
    """
    This function will return a 'Mr.' or 'Mrs.'
    """
    salutations = ("Mr.", "Mrs.")
    return random.choice(salutations)


def screename(service=""):
    """
    Makes screenames for the service you pick.
    The screenames conform to their rules, such as
    aol screenames are 3-16 in length with @aol.com on the end.
    Options include: nil, aol, aim, skype, google
    """
    def _make_name(a, b):
        return ''.join(random.sample(string.ascii_letters,
            random.choice(range(a, b))))
    if service in ("", "aim", "aol"):
        name = _make_name(3, 16)
        if service == "aol":
            return name + "@aol.com"
        else:
            return name
    elif service is "skype":
        name = _make_name(6, 32)
        return name
    elif service is "google":
        name = _make_name(1, 19)
        return name + "@google.com"
    else:
        name = _make_name(8, 20)
        return name


def sentence(num_words=20, chars=''):
    word_list = open(os.path.dirname(__file__) + '/book_sherlock.txt').read().split()
    words = ' '.join(random.choice(word_list) for x in xrange(num_words))
    return words if not chars else words[:chars]


def set_of_initials(i=3):
    """Returns initials with period seperators."""
    return [''.join(random.choice(string.ascii_uppercase) + '.' for x in xrange(i))]


def social_security_number():
    """
    This function will produce a Mock Social Security Number.
    ie - social_security_number() = '112-32-3322'
    """
    return '%.3i-%.2i-%.4i' % (random.randrange(999),
        random.randrange(99), random.randrange(9999),)


def special_characters(i):
    """
    This function will pick x amount of special chars from the list below.
    ie - picka.special_characters() = '@%^$'.
    """
    return ''.join(random.choice(string.punctuation)
            for x in xrange(i))


def street_type():
    """This function will return a random street type."""
    try:
        us_street_types = _query(_QUERIES["us_street_types"])
    except KeyError:
        print "Key missing."
    return random.choice(us_street_types)[0]


def street_name():
    """
    This function will create a street name from either
    a male or female name, plus a street type.
    """
    try:
        us_street_types = _query(_QUERIES["us_street_types"])
        us_female_first_names = _query(_QUERIES["us_female_first_names"])
        us_male_first_names = _query(_QUERIES["us_male_first_names"])
    except KeyError:
        print "Key missing."
    us_male_and_female_first_names = us_female_first_names + us_male_first_names
    return "%s %s" % (
        random.choice(us_male_and_female_first_names)[0],
        random.choice(us_street_types)[0],
        )


def street_address():
    """This function will produce a complete street address."""
    return random.choice([
            '%d-%d %s' % (random.randrange(999),
                random.randrange(999), street_name()),
            '%d %s' % (random.randrange(999), street_name()),
            '%s %d, %s' % ("P.O. Box", random.randrange(999), street_name()),
            ])


def suffix():
    """This returns a suffix from a small list."""
    return random.choice(["Sr.", "Jr.", "II", "III", "IV", "V"])


def timestamp(style=False):
    """
    This is a convenience function for creating timestamps.
    Default when empty, is "12:28:59PM 07/20/10" or "%H:%M:%S%p %D".
    To change this, pass in your format as an arg.
    """
    if not style:
        return time.strftime("%H:%M:%S%p %D", time.localtime())
    else:
        return time.strftime(style, time.localtime())


def timezone_offset():
    """
    This function will select the value of a timezone offsets,
    such as GMT, GMT+4, etc.
    """
    return random.choice([["GMT+" + str(random.randint(1, 12))], ["GMT"], ["GMT" + str(random.randint(-12, -1))]])


def timezone_offset_country():
    """This function will select the country part of a timezone."""
    return random.choice(["Eniwetoa", "Hawaii", "Alaska", "Pacific", "Mountain", "Central", 
        "Eastern", "Atlantic", "Canada", "Brazilia", "Buenos Aries", "Mid-Atlantic", "Cape Verdes",
        "Greenwich Mean Time", "Dublin", "Berlin", "Rome", "Israel", "Cairo", "Moscow", "Kuwait",
        "Abu Dhabi", "Muscat", "Islamabad", "Karachi", "Almaty", "Dhaka", "Bangkok, Jakarta", 
        "Hong Kong", "Beijing", "Tokyo", "Osaka", "Sydney", "Melbourne", "Guam", "Magadan",
        "Soloman Islands", "Fiji", "Wellington", "Auckland", ])


def url(i, extension=".com"):
    """
    This function will create a website url, with a default of .com
    To use another extension, do picka.url(10, ".net")
    """
    return email(i, extension)


def state_abbreviated():
    """
    This function produces just a state abbreviation.
    ie - state_abbreviated() = 'NY'
    """
    return random.choice(_query(_QUERIES["us_cities"]))[0][-2:]


def postal_code():
    """This function will pick a zipcode randomnly from a list.
    ie - zipcode() = '11221'."""
    return random.choice(_query(_QUERIES["us_postal_codes"]))[0]
