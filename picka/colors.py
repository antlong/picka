from random import randint

from attrdict import AttrDict

import db

_query = db.Queries()
query_multiple = _query.query_multiple
query_single = _query.query_single


def rgb():
    # todo: change from string?
    return [str(randint(0, 256)) for _ in range(3)]


def rgba():
    # todo: expand tests
    r, g, b = rgb()
    a = 100 * float(randint(1, 256)) / float(256) / 100
    return AttrDict({"r": r, "g": g, "b": b, "a": "%.2f" % round(a, 2)})


def hex_color():
    # todo: add test
    s = ""
    for x in rgb():
        s += hex(int(x))[2:4].zfill(2)
    return s


def html_name():
    # todo: add test
    print query_multiple("name,hex", "html_colors")
