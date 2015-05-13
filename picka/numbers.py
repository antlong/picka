import random
from attrdict import AttrDict

import picka_utils as _utils
from picka import number as _number

_query = _utils.query
extended_display = False

def calling_code():
    """
    Returns a calling code from a list of all known calling codes in \
    the world.
    """
    return _query("calling_code", "countries_and_calling_codes")


def calling_code_with_country():
    """Returns a country, with a calling code as a single string."""
    return _query("*", "countries_and_calling_codes")


def area_code(state=False):
    if state:
        return _query("code", "areacodes", "state")
    else:
        return _query("code", "areacodes")


@_utils.deprecated("picka.phone_number(formatting)")
def fax_number():
    """
    :Summary: Returns a fax (phone) number.
    :Usage: picka.fax_number() >>> 755-463-6544
    """

    return _phone()


def generate(state=None):
    """Generate a phone number. Conforms to NANP standards.

      :arg state: Bool
      :arg formatting: local, domestic, or international
    """
    data = {}

    def validate(*args):
        for _ in xrange(11):
            if args:
                a = str(area_code(args[0]))
            b = str(random.randint(2, 9)) + _number(2)
            if (a, b) not in ["911", "555"]:
                break
        return a, b

    a, b = validate(state)
    c = _number(4)

    if extended_display:
        data["areacode"] = a
        data["local"] = "{0}-{1}".format(b, c)
        data["domestic"] = "({0}) {1}-{2}".format(a, b, c)
        data["international"] = "+1-{0}-{1}-{2}".format(a, b, c)
        data["standard"] = "{0}-{1}-{2}".format(a, b, c)
        data["plain"] = a + b + c
        data["state"] = _query("state", "areacodes", "code", a)
    return AttrDict(data)


def phone_number(state=None):
    return generate(state)
