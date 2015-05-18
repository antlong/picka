from random import sample
from string import ascii_letters, ascii_lowercase, \
    ascii_uppercase, digits, punctuation
from random import choice, randrange, randint

from attrdict import AttrDict
from sqlalchemy import text

import picka_utils
from numerics import age as _age
from numerics import number
from numerics import birthdate as _birthdate

engine = picka_utils.engine_connection()


def name(sex="Male"):
    f = [initial(period=True).upper(), set_of_initials(2)[0]]
    m = ["", initial(period=True), set_of_initials(2)[0]]
    s = [surname(), "%s-%s" % (surname(), surname())]
    if sex.startswith("M"):
        f.append(male())
        m.append(male())
    else:
        f.append(female())
        m.append(female())
    return AttrDict({
        "first": unicode(choice(f)),
        "middle": unicode(choice(m)),
        "last": unicode(choice(s))
    })


def male():
    res = engine.execute("SELECT name FROM male ORDER BY random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


def age():
    return AttrDict(_age())


def birthdate():
    return _birthdate()


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


def screename(*service):
    # Todo: Re-write
    """
    Makes screenames for the service you pick.
    The screenames conform to their rules, such as
    aol screenames are 3-16 in length with @aol.com on the end.
    Options include: nil, aol, aim, skype, google
    """
    service = "aim" if not service else service

    def _make_name(a, b):
        return ''.join(sample(
            ascii_letters, choice(
                range(a, b)))
        )

    if service in ['aim', 'aol']:
        return _make_name(3, 16)
    elif service is 'skype':
        return _make_name(6, 32)
    elif service is 'google':
        return _make_name(1, 19) + '@googletalk.com'
    else:
        return _make_name(8, 20)


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
    """Generates drivers license numbers that adhere to the state license format.

    Args:
      state (str, optional): Two letter state code.

    Returns:
      str: generated license code.

    Examples:
        print drivers_license() => "I370162546092578729"
        print drivers_license("AL") => "2405831"

    >>> assert len(drivers_license()) > 0
    >>> assert len(drivers_license("OK")) in [9, 10]

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


def business_title(abbreviated=False):
    """This will produce a random business title.

    :parameters:
        abbreviated: (boolean)
            Do you want abbreviated titles?

    This function will return business titles. \
    :tip: They are generic business titles.

    """
    abbs = ['COO', 'CEO', 'CFO', 'VP', 'EVP']
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
    return ((choice(abbs) if abbreviated else '{} {}'.format(
        choice(primary), choice(secondary))))


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
            'prefixes': ['5018', '5020', '5038', '6304', '6759', '6761', '6762',
                         '6763'],
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
            'prefixes': ['4903', '4905', '4911', '4936', '564182', '633110',
                         '6333', '6759'],
            'length': [16, 18, 19]
        },
        'visa': {
            'prefixes': ['4'],
            'length': [16]
        },
        'visa-electron': {
            'prefixes': ['4026', '417500', '4508', '4844', '4913', '4917'],
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
    return choice([
        'Sr.', 'Jr.', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'
    ])
