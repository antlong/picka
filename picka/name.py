import random
import string

import picka_utils as _utils
import english as _english


_query = _utils.query


def salutation():
    """This function will return a 'Mr.' or 'Mrs.'"""
    return random.choice(['Mr.', 'Mrs.', 'Miss', 'Dr.', 'Prof.', 'Rev.'])


def male():
    """Returns a randomly chosen male first name."""
    return _query("name", "male")


def female():
    """Returns a randomly chosen female first name."""
    return _query("name", "female")


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
    return "{0}{1}".format(_utils.random_string(), "." if period else "")


def set_of_initials(i=3):
    """Returns initials with period seperators."""

    return [''.join(initial(True) for _ in xrange(i))]


def surname():
    """Returns a randomly chosen surname."""
    return _query("name", "surname")


def hyphenated_last_name():
    """
    This function will pick 2 random last names and hyphenate them.
    ie - hyphenated_last_name() = 'Perry-Jenkins'
    """

    return '{}-{}'.format(surname(), surname())


def suffix():
    """This returns a suffix from a small list."""
    return random.choice([
        'Sr.', 'Jr.', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'
    ])


@_utils.deprecated("picka.surname()")
def last_name():
    return surname()


@_utils.deprecated("picka.surname()")
def last():
    return last_name()


@_utils.deprecated("picka.name(format='{male}{middle}{last}'")
def male_full_name():
    return _english.name("{male} {male} {surname}")


@_utils.deprecated("picka.name(format='{male}{initial}{last}', gender='M'")
def male_full_name_w_middle_initial():
    return _english.name("{male} {initial}")


@_utils.deprecated("picka.name('{female}')")
def female_first():
    return female()


@_utils.deprecated("picka.name('{female}')")
def female_middle():
    return female()


@_utils.deprecated("picka.name('{female}')")
def female_name():
    """
     :Summary: Returns a random female name.
     :Usage: picka.female_name() >>> 'Christy'
    """
    return female()


@_utils.deprecated("picka.name('{male}')")
def male_middle_name():
    return male()


@_utils.deprecated("picka.name('{male}')")
def male_middle():
    return male()


@_utils.deprecated("picka.name('{male}')")
def male_first():
    return male()