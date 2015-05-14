from random import randint

from attrdict import AttrDict

import db

_query = db.Queries()
query_multiple = _query.query_multiple
query_single = _query.query_single


def rgb():
    return [str(randint(0, 256)) for _ in range(3)]


def rgba():
    r, g, b = rgb()
    a = 100 * float(randint(1, 256)) / float(256) / 100
    return AttrDict({"r": r, "g": g, "b": b, "a": "%.2f" % round(a, 2)})


def hex_color():
    s = ""
    for x in rgb():
        s += hex(x)[2:4].zfill(2)
    return s


def html_name():
    print query_multiple("name,hex", "html_colors")
