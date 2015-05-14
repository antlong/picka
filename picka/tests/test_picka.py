#!/usr/bin/env python
# -*- coding: utf-8 -*-
from types import *

import picka


def test_phone_number():
    assert len(picka.phone_number().items()) > 1


def test_last_name():
    name = picka.last_name()
    assert len(name) >= 1
    assert type(name) is UnicodeType, "%s is not a unicode object." % name


def test_random_string():
    s = picka.random_string(8)
    assert len(s) == 8
    assert type(s) is StringType, "%r is not a string."


def test_initial():
    x = picka.initial()
    y = picka.initial(period=True)
    assert "." not in x
    assert len(x) == 1
    assert type(x) is StringType
    assert type(picka.initial(x)) is StringType
    assert y[-1] == "."


def test_sentence():
    assert type(picka.sentence()) is StringType


def test_sentence_actual():
    x = picka.sentence_actual(min_words=3, max_words=3)
    assert len(x.split()) == 3


def test_timezone_offset():
    assert picka.timezone_offset()


def test_rgba():
    assert len(picka.rgba()) == 4


def test_language():
    assert len(picka.language()) > 0


def test_timezone_offset_country():
    assert len(picka.timezone_offset_country()) > 0


def test_screename():
    assert picka.screename()


def test_number():
    assert picka.number(10)


def test_month():
    assert picka.month()


def test_special_characters():
    assert picka.special_characters(8)


def test_postal_code():
    assert picka.postal_code()


def test_apartment_number():
    assert picka.apartment_number()


def test_gender():
    assert picka.gender()


def test_salutation():
    assert picka.salutation()


def test_creditcard():
    assert picka.creditcard(prefix='visa')


def test_male_middle_name():
    assert picka.male_middle_name()


def test_city():
    assert picka.city()


def test_male_full_name_w_middle_initial():
    assert picka.male_full_name_w_middle_initial()


def test_state_abbreviated():
    assert picka.state_abbreviated()


def test_street_name():
    assert picka.street_name()


def test_calling_code_with_country():
    assert picka.calling_code_with_country()


def test_surname():
    assert picka.surname()


def test_business_title():
    assert picka.business_title()


def test_male_middle():
    assert picka.male_middle()


def test_trash():
    assert picka.trash(picka.male_first)


def test_female_first():
    assert picka.female_first()


def test_calling_code():
    assert picka.calling_code()


def test_male_first():
    assert picka.male_first()


def test_timestamp():
    assert picka.timestamp()


def test_hyphenated_last_name():
    assert picka.hyphenated_last_name()


def test_fax_number():
    assert picka.fax_number()


def test_male_full_name():
    assert picka.male_full_name()


def test_password_alphanumeric():
    assert picka.password_alphanumeric(8)


# assert picka.birthday()

def test_social_security_number():
    assert picka.social_security_number()


def test_set_of_initials():
    assert picka.set_of_initials()


def test_female_middle():
    assert picka.female_middle()


def test_month_and_day():
    assert picka.month_and_day()


def test_password_alphabetical():
    assert picka.password_alphabetical(8)


def test_name():
    assert picka.name()


def test_cvv():
    assert picka.cvv(3)


def test_country():
    assert picka.country()


def test_age():
    assert picka.age()


def test_city_with_state():
    assert picka.city_with_state()


def test_email():
    assert picka.email()


def test_female_name():
    assert picka.female_name()


def test_street_type():
    assert picka.street_type()


def test_suffix():
    assert picka.suffix()


def test_url():
    assert picka.url(10)


def test_password_numerical():
    assert picka.password_numerical(10)


def test_street_address():
    assert picka.street_address()


def test_barcode_ean_8():
    assert len(picka.barcode("EAN-8")) == 8


def test_barcode_ean_13():
    assert len(picka.barcode("EAN-13")) == 13


# assert picka.locale()

def test_mime_type():
    assert picka.mime_type()


def test_zipcode_result_length():
    data = picka.zipcode()
    assert len(data.result) == 5


def test_zipcode_is_string():
    data = picka.zipcode()
    assert isinstance(data.result, StringType)


def test_zipcode_selections_in_computed_range():
    data = picka.zipcode()
    for x in data.original_range:
        for y in x:
            assert y in data.computed_range
