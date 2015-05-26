from types import StringType, UnicodeType
from re import match

import pytest
from assertlib import assertEqual, assertTrue, assertIsInstance

from picka import *

current_year = datetime.now().year


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


def test_age_datetime():
    a = age()
    assert isinstance(a.datetime, datetime)


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


def test_birthdate_custom_strftime():
    a = birthdate(custom_strftime="%m/%d/%Y")
    a_split = str(a).split("/")
    assert len(a_split) == 3
    assert int(a_split[0]) <= 12
    assert int(a_split[1]) <= 31
    assert int(a_split[2]) <= 2015


def test_birthdate_custom_strftime_dto():
    a = birthdate(custom_strftime="DTO")
    assert type(a) == type(datetime.now())


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


def test_age():
    # min_year default
    # max_year default
    # year range: 1900 through 2015
    assert 1900 <= int(age().year) <= current_year

    # min_year modified
    # max_year default
    # year range: 2000 through 2015
    assert 2000 <= int(age(min_year=2000).year) <= current_year

    # min_year default
    # max_year 2000
    # year range: 1900 through 2000
    assert 1900 <= int(age(max_year=2000).year) <= 2000

    # min_year 1950
    # max_year 1950
    # year range: 1950
    assert 1950 == int(age(min_year=1950, max_year=1950).year)

    # The minimum year should be greater than the maximum.
    with pytest.raises(InvalidRange):
        age(min_year=2000, max_year=1900)

    assert age().datetime
    assert 1 <= int(age().day) <= 31
    assert 1 <= int(age().month_digit) <= 12
    assert age().month_short
    assert age().period in ["AM", "PM"]
    assert age().pretty_date
    assert age().time
    assert 1900 <= int(age().year) <= 2015
    assert 1 <= int(age().years_old) <= 115


def test_apartment_number():
    pass


def test_birthdate():
    pass


def test_business_title():
    assert len(business_title().split()) == 2


def test_business_title_abbreviation():
    assert business_title_abbreviation() in ['COO', 'CEO', 'CFO', 'VP', 'EVP']


def test_career():
    pass


def test_city():
    pass


def test_city_with_state():
    pass


def test_company_name():
    pass


def test_country():
    pass


def test_creditcard():
    pass


def test_cvv():
    pass


def test_drivers_license():
    pass


def test_email():
    pass


def test_female():
    pass


def test_gender():
    pass


def test_hyphenated_last_name():
    pass


def test_initial():
    pass


def test_language():
    pass


def test_mac_address():
    pass


def test_male():
    pass


def test_name():
    pass


def test_password():
    pass


def test_salutation():
    pass


def test_set_of_initials():
    pass


def test_social_security_number():
    pass


def test_state_abbreviated():
    pass


def test_street_address():
    pass


def test_street_name():
    pass


def test_street_type():
    pass


def test_suffix():
    pass


def test_surname():
    assert len(surname().name) > 1


def test_url():
    assert '.com' in url(5).email
    assert len(url(5).email) == 9


def test_zipcode():
    assert len(zipcode()) == 5


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


def test_timezone_offset_no_utc():
    t = timezone_offset(utc=False)
    assert len(t.keys()) == 1
    assertTrue(match("[+-]\d{2}:\d{2}", t.dst))


def test_phone_number():
    assert len(picka.phone_number().items()) > 1


def test_last_name():
    _name = picka.surname().name
    assert len(_name) >= 1
    assert type(_name) is UnicodeType, "%s is not a unicode object." % _name


def test_timezone_offset():
    assert picka.timezone_offset()


def test_timezone_offset_country():
    assert len(picka.timezone_offset_country()) > 0


def test_screename():
    assert picka.screename()


def test_barcode_ean_8():
    assert len(picka.barcode("EAN-8")) == 8


def test_barcode_ean_13():
    assert len(picka.barcode("EAN-13")) == 13


# assert picka.locale()

def test_mime_type():
    assert picka.mime_type()
