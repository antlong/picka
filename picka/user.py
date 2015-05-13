import random
import string

from attrdict import AttrDict

import utils as _utils
import age as _age

def age():
    return AttrDict(_age.age())

def birthdate():
    return _age.birthdate()

def email(length=8, domain='@example.com'):
    """
    :Summary: Created a randomized email.
    :Usage: picka.email(length=8, domain='@foo.com')
    """

    return ''.join(random.choice(string.ascii_lowercase) for _ in
                   xrange(length)) + domain


def screename(*service):
    """
    Makes screenames for the service you pick.
    The screenames conform to their rules, such as
    aol screenames are 3-16 in length with @aol.com on the end.
    Options include: nil, aol, aim, skype, google
    """
    service = "aim" if not service else service

    def _make_name(a, b):
        return ''.join(random.sample(
            string.ascii_letters, random.choice(
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


@_utils.deprecated("picka.password(format='numbers')")
def password_alphanumeric(i=8):
    return password(length=i, format="numbers")


@_utils.deprecated("picka.password(format='letters', length=8")
def password_alphabetical(i=8, case="mixed"):
    return password(case=case, length=i)


@_utils.deprecated("picka.password(format='numeric', length=8")
def password_numerical(i):
    return password(length=i)


def password(case='mixed', length=6, format='letters', special_chars=False):
    choices = ''
    if format in ['letters', 'alphanumeric']:
        cases = {
            'upper': string.ascii_uppercase,
            'mixed': string.ascii_letters,
            'lower': string.ascii_lowercase
        }
        choices += cases[case]
    if format in ['numbers', 'alphanumeric']:
        choices += string.digits
    if special_chars:
        choices += string.punctuation
    output = ''
    for _ in xrange(length):
        output += random.choice(choices)
    return output


def url(i, extension='.com'):
    """
    This function will create a website url, with a default of .com
    To use another extension, do picka.url(10, ".net")
    """

    return email(i, extension)


def mac_address():
    mac = [
        0x00, 0x16, 0x3e,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def gender():
    """
    Returns a random gender.
    """

    return random.choice(['Male', 'Female'])


def language():
    """Picks a random language."""

    _query("name", "languages")


def social_security_number(state="NY"):
    """Produces a US Social Security Number.

    Example:
      social_security_number() => '112-32-3322'

    >>> assert len(social_security_number()) == 11

    """
    x = random.choice(_utils._ssn_prefixes(state))
    return '{0}-{1}-{2}'.format(
        random.randrange(x[0], x[1] + 1),
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
        i = random.choice([random.randint(1, 7), 12])
        return password(
            case="upper",
            length=i,
            format="alphanumeric",
            special_chars=False
        )
    n = random.choice(lengths[state])
    s = ""
    s += random_string(length=n[0])
    s += number(length=n[1])

    if len(n) > 2:
        if state == "ID":
            s += random_string()
        if state == "IA":
            s += random_string(length=n[2])
            s += number(n[3])
        if state == "KS":
            s += random_string(n[2])
            s += number(n[3])
            s += random_string(n[4])
        if state == "MO":
            s += "R" if n[2] == "R" else random_string(n[2])
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
        'Supervisor',
        'Associate',
        'Executive',
        'Liason',
        'Officer',
        'Manager',
        'Engineer',
        'Specialist',
        'Director',
        'Coordinator',
        'Assistant',
        'Facilitator',
        'Agent',
        'Representative',
        'Strategist',
    ]
    return ((random.choice(abbs) if abbreviated else '{} {}'.format(
        random.choice(primary), random.choice(secondary))))


def career():
    """This function will produce a career."""
    cursor.execute('SELECT name FROM careers ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


def company_name():
    """This function will return a company name"""

    cursor.execute('SELECT name FROM companies \
        ORDER BY RANDOM() LIMIT 1;')
    return cursor.fetchone()[0]


def creditcard(prefix='visa'):
    if prefix == 'visa':
        prefix = ['40240071']
    elif prefix == 'amex':
        prefix = ['34', '37']
    elif prefix == 'discover':
        prefix = ['6011']
    elif prefix == 'mastercard':
        prefix = ['51', '52', '53', '54', '55']
    while len(prefix) < 15:
        prefix += str(random.randint(0, 9))
    return ''.join(prefix) + '0'


def cvv(i):
    """Returns a cvv, based on the length you provide.
    :Usage: picka.cvv(3) or picka.cvv(4)
    """

    return '{}'.format(random.randint(111, (999 if i == 3 else 9999)))
