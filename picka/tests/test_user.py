"""Tests for the user.py module"""
import datetime

import pytest

from picka.picka_exceptions import InvalidRange
from picka.user import age, apartment_number, birthdate, business_title, \
    career, city, city_with_state, company_name, country, creditcard, cvv, \
    drivers_license, email, female, gender, hyphenated_last_name, initial, \
    language, mac_address, male, name, password, salutation, \
    set_of_initials, social_security_number, state_abbreviated, street_address,\
    street_name, street_type, suffix, surname, url, zipcode
current_year = datetime.datetime.now().year


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
    pass


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
    pass


def test_url():
    pass


def test_zipcode():
    pass
