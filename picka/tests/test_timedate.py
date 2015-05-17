"""Tests for the time and date categories."""
from re import match
from types import StringType

from assertlib import assertTrue, assertIsInstance

from picka import month, month_day, \
    month_day_year, timestamp, timezone_offset


def test_month():
    m = month()
    assert len(m) > 0
    assert isinstance(m, StringType)


def test_month_day():
    m = month_day()
    assert len(m.month) > 0
    assert 1 <= len(m.day) <= 31
    assertIsInstance(m.month, StringType)
    assertIsInstance(m.day, StringType)


def test_month_day_year():
    m = month_day_year()
    assert len(m.month) > 0
    assert 1 <= len(m.day) <= 31
    assert 1900 <= int(m.year) <= 2010
    assertIsInstance(m.month, StringType)
    assertIsInstance(m.day, StringType)
    assertIsInstance(m.day, StringType)


def test_timestamp():
    t = timestamp().split(" ")
    assertTrue(match("\d{2}:\d{2}:\d{2}[A:P][M]", t[0]))
    assertTrue(match("\d{2}/\d{2}/\d{2}", t[1]))


def test_timezone_offset_default():
    t = timezone_offset()
    assertTrue(match("[+-]\d{2}:\d{2}", t.dst))
    assertTrue(match("[+-]\d{2}:\d{2}", t.utc))


def test_timezone_offset_no_dst():
    t = timezone_offset(dst=False)
    assert len(t.keys()) == 1
    assertTrue(match("[+-]\d{2}:\d{2}", t.utc))


def test_timezone_offset_no_utc():
    t = timezone_offset(utc=False)
    assert len(t.keys()) == 1
    assertTrue(match("[+-]\d{2}:\d{2}", t.dst))
