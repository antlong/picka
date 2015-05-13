import random
import string

import picka_utils as _utils


_query = _utils.query


def street_address():
    """This function will produce a complete street address."""

    return random.choice(
        [
            '%d-%d %s' % (
                random.randrange(999),
                random.randrange(999),
                street_name()
            ),
            '%d %s' % (
                random.randrange(999),
                street_name()
            ),
            '%s %d, %s' % (
                'P.O. Box',
                random.randrange(999),
                street_name()
            )
        ]
    )


def street_name():
    """
    This function will create a street name from either
    a male or female name, plus a street type.
    """
    return "{} {}".format(_query("name", "streetnames"), str(street_type()))


def street_type():
    """This function will return a random street type."""
    return _query("name", "us_street_types")


def apartment_number():
    """
    Returns an apartment type, with a number.

    :tip: There are many different types which could be returned.
    If you are looking for a specific format, you might be interested\
    in using string formatting instead.

    """
    _type = random.choice(['Apt.', 'Apartment', 'Suite', 'Ste.'])
    letter = random.choice(string.ascii_letters).capitalize()
    directions = ['E', 'W', 'N', 'S']
    short = '{} {}'.format(_type, random.randint(1, 999))
    _long = '{} {}{}'.format(_type, random.randint(1, 999), letter)
    alt = '{} {}-{}{}'.format(_type, random.choice(directions),
                              random.randint(1, 999), letter)
    return random.choice([short, _long, alt])


def city():
    """This function will produce a city."""
    return _query("city", "us_cities")


def city_with_state():
    """
    This function produces a city with a state.
    ie - city_with_state() = 'New York, NY'
    """
    return ', '.join(_query("city, state", "us_cities"))


def state_abbreviated():
    """
    This function produces just a state abbreviation.
    eg - state_abbreviated() = 'NY'
    """
    return _query("abbreviation", "states")


@_utils.deprecated("picka.zipcode(state)")
def postal_code():
    return zipcode()


def zipcode(state=False):
    """This function will pick a zipcode randomnly from a list.
    eg - zipcode() = '11221'.
    """
    range_gen = []
    if state:
        _range = _query(custom='SELECT min, max FROM zipcodes WHERE st = "{}";'.format(state), quantity=True)
        for r in _range:
            range_gen += range(r[0], r[1])
        return '%05d' % random.choice(range_gen)
    else:
        range_gen += _query(
            custom='SELECT min, max FROM zipcodes ORDER BY RANDOM() LIMIT 1;',
            quantity=True
        )[0]
    print range_gen
    return '%05d' % random.randint(range_gen[0], range_gen[1])


def country():
    # Todo: Use max row.
    """This function will return a random country."""
    return _query("name", "countries")
