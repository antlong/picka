from random import randint
from attrdict import AttrDict

from picka.picka import engine as _engine

engine = _engine

def rgb():
    """Generates an RGB color.

    Returns:
      AttrDict: A dictionary with the generated colors.

    Examples:
      >>> rgb
      AttrDict({'r': '133', 'g': '12', 'b': '211'})
    """
    # todo: change from string?
    r, g, b = [str(randint(0, 256)) for _ in range(3)]
    return AttrDict({"r": r, "g": g, "b": b})

def rgba():
    # todo: expand tests
    _rgb = rgb()
    _rgb["a"] = str(100 * float(randint(1, 256)) / float(256) / 100)[:4]
    return _rgb


def hex_color():
    # todo: add test
    s = ""
    for x in rgb():
        s += hex(int(x))[2:4].zfill(2)
    return AttrDict({"color": s})


def html_name():
    # todo: add test
    res = engine.execute(
        "select name, hex from html_colors where rowid = (abs(random()) % (select max(rowid)+1 from html_colors))"
    )
    return [dict(d) for d in res.fetchall()]

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)