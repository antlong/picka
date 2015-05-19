from string import ascii_letters, digits
from random import choice, randint
from user import male, female, state_abbreviated
from numerics import number

def aol():
    name_choice = choice([male().name, female().name])
    state_choice = state_abbreviated().abbreviation
    number_choice = str(number(choice([1, 5])))

    return name_choice + state_choice + number_choice

def screename(service="any"):
    # Todo: Re-write
    """
    Makes screenames for the service you pick.
    The screenames conform to their rules, such as
    aol screenames are 3-16 in length with @aol.com on the end.
    Options include: nil, aol, aim, skype, google
    """
    service = "aim" if not service else service

    def _make_name(a, b):
        s = ""
        length = choice(range(a, b))
        choices = ''.join([digits, ascii_letters])
        for _ in range(length):
            s += choice(choices)
        return s

    if service in ['aim', 'aol']:
        return _make_name(3, 16)

    if service == 'skype':
        pre = choice(ascii_uppercase)
        post = _make_name(5, 31)
        return pre + post

    if service is 'google':
        return _make_name(1, 19) + '@googletalk.com'

    return "any: " + _make_name(8, 20)
