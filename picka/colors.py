"""Functions that generate data in the color category.

Attributes:
  engine (Engine): The connection to the database.

Notes:
  Corresponding tests are found in picka/tests/test_colors.py
"""
from random import randint

from attrdict import AttrDict

import picka_utils

engine = picka_utils.engine_connection()
asdict = picka_utils.asdict


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
    """Generates an RGBA color.

    Returns:
      AttrDict: A dictionary with the generated colors.

    Examples:
      >>> rgba()
      AttrDict({'r': '133', 'g': '12', 'b': '211', 'a': '0.90'})
    """
    _rgb = rgb()
    _rgb["a"] = str(100 * float(randint(1, 256)) / float(256) / 100)[:4]
    return _rgb


def hex_color():
    """Generates a hex color.

    Returns:
      AttrDict (str): A dictionary with the generated colors.

    Examples:
      >>> hex_color()
      AttrDict({'r': '82', 'b': '37', 'hex': '525725', 'g': '87'})
      >>> hex_color().hex
      '525725'
    """
    s = ""

    color_choice = rgb()
    r = color_choice.r
    g = color_choice.g
    b = color_choice.b

    for x in [r, g, b]:
        s += hex(int(x))[2:4].zfill(2)

    return AttrDict({"hex": s.upper(), "r": r, "g": g, "b": b})


def html_name():
    """Generates a random html color name.

    Returns:
      name (str): The name of the picked color.
      hex (str): The corresponding hex code of the color.

    Examples:
      >>> html_name()
      AttrDict({u'hex': u'80008', u'name': u'purple'})
      >>> html_name().hex
      '808080'
    """
    res = engine.execute(
        "SELECT name, hex FROM html_colors ORDER BY RANDOM() LIMIT 1;"
    )

    return AttrDict([dict(d) for d in res.fetchall()][0])
