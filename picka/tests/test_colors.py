__author__ = 'antlong'
from assertlib import assertEqual

from picka import hex_color, rgb, rgba, html_name


def test_hex_color():
    h = hex_color()
    assert "r" in h.keys()
    assert "g" in h.keys()
    assert "b" in h.keys()
    assert "hex" in h.keys()
    for x in h.values():
        if len(x) <= 3:
            assert 0 <= int(x) <= 256

def test_rbg():
    c = rgb()
    assert "r" in c.keys()
    assert "g" in c.keys()
    assert "b" in c.keys()
    for x in c.values():
        if len(x) <= 3:
            assert 0 <= int(x) <= 256


def test_rgba():
    c = rgba()
    assert "r" in c.keys()
    assert "g" in c.keys()
    assert "b" in c.keys()
    assert "a" in c.keys()
    for x in c.values():
        if len(x) <= 3:
            assert 0 <= int(x) <= 256
    assert len(c.a) >= 3


def test_html_name():
    n = html_name()
    assert "hex" in n.keys()
    assert "name" in n.keys()
    assertEqual(len(n.hex), 6)