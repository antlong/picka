"""Tests for numerics.py"""
from types import StringType
import datetime
from re import match

from attrdict import AttrDict

from picka import age, areacode, birthdate, calling_code, number, phone_number


def test_age_datetime():
    a = age()
    assert isinstance(a.datetime, datetime.datetime)


def test_age_day():
    a = age()
    assert 1 <= int(a.day) <= 31
    assert isinstance(a.day, StringType)


def test_age_month_digit():
    a = age()
    assert int(a.month_digit) <= 12
    assert isinstance(a.month_digit, StringType)


def test_age_month_short():
    a = age()
    assert len(a.month_short) > 2
    assert isinstance(a.month_short, StringType)


def test_age_period():
    a = age()
    assert a.period in ["AM", "PM"]
    assert isinstance(a.period, StringType)


def test_age_pretty_date():
    a = age()
    tup = a.pretty_date.replace(",", "").split()
    assert len(tup) == 3
    assert 1900 <= int(tup[2]) <= 2015
    assert isinstance(a.pretty_date, StringType)


def test_age_min_year():
    a = age(min_year=2010)
    assert 2010 <= int(a.year) <= 2015
    assert isinstance(a.year, StringType)


def test_age_max_year():
    a = age(min_year=3000, max_year=3000)
    assert a.year == "3000"
    assert isinstance(a.year, StringType)


def test_age_time():
    a = age()
    tup = a.time.split(":")
    assert int(tup[0]) <= 12
    assert int(tup[1]) <= 60
    assert isinstance(a.time, StringType)


def test_age_years_old():
    a = age()
    age_range = 2015 - 1900
    assert int(a.years_old) <= age_range
    assert isinstance(a.years_old, StringType)


def test_area_code_default():
    a = areacode()
    assert 201 <= int(a.areacode) <= 989
    assert len(a.state) == 2


def test_phone_number_areacode():
    a = areacode()
    assert len(a.areacode) == 3
    assert isinstance(a.areacode, unicode)
    assert 201 <= int(a.areacode) <= 989
    assert bool(match(r"\d{3}", a.areacode))


def test_phone_number_areacode_with_state():
    a = areacode("AB")
    assert a.areacode in ["780", "403"]
    assert isinstance(a.areacode, unicode)


def test_birthdate_min_year():
    a = birthdate(min_year=2015)
    assert a.year == "2015"
    isinstance(a.year, StringType)


def test_birthdate_max_year():
    a = birthdate(min_year=3000, max_year=3000)
    assert a.year == "3000"
    isinstance(a.year, StringType)


def test_birthdate_month():
    a = birthdate()
    assert 1 <= int(a.month) <= 12
    isinstance(a, StringType)


def test_birthdate_day():
    a = birthdate()
    assert 1 <= int(a.day) <= 31
    isinstance(a, StringType)


def test_birthdate_year():
    a = birthdate()
    assert 1900 <= int(a.year) <= 2015


def test_birthdate_formatted():
    a = birthdate(formatted="%m/%d/%Y")
    a_split = str(a).split("/")
    assert len(a_split) == 3
    assert int(a_split[0]) <= 12
    assert int(a_split[1]) <= 31
    assert int(a_split[2]) <= 2015


def test_birthdate_formatted_dto():
    a = birthdate(formatted="DTO")
    assert type(a) == type(datetime.datetime.now())


def test_birthdate_is_attrdict():
    a = birthdate()
    assert isinstance(a, AttrDict)


def test_calling_code():
    a = calling_code()
    assert a.calling_code
    assert a.country
    assert 1 <= int(a.calling_code) <= 998
    assert len(a.keys()) == 2


def test_calling_code_with_country():
    a = calling_code("Denmark")
    assert a.country
    assert a.calling_code == '45'
    assert len(a.keys()) == 2


def test_number():
    assert len(str(number())) == 1
    for i in range(11):
        n = number(i)
        assert len(str(n)) == i


def test_phone_number_domestic():
    a = phone_number()
    assert bool(match(r"\(\d{3}\) \b\d{3}[-]?\d{4}\b", a.domestic))


def test_phone_number_international():
    a = phone_number()
    assert bool(match(r"\+1\-\d{3}-\d{3}[-]?\d{4}\b", a.international))


def test_phone_number_local():
    a = phone_number()
    assert bool(match(r"\d{3}-\d{4}", a.local))


def test_phone_number_plain():
    a = phone_number()
    assert bool(match(r"\d{10}", a.plain))


def test_phone_number_standard():
    a = phone_number()
    assert bool(match(r"\d{3}-\d{3}-\d{4}", a.standard))


def test_phone_number_with_state():
    a = phone_number("NY")
    assert bool(match(r"\b\w{2}\b", a.state))
