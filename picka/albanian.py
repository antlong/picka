# -*- coding: UTF-8 -*-
"""
Picka is a data generation and randomization module which aims to increase
coverage by increasing the amount of tests you _dont_ have to write
by hand.
By: Anthony Long
"""
import os
import random
import string
import jsonlib as json
__docformat__ = "restructuredtext en"
albanian_names = json.loads(open(os.path.join(os.path.dirname(__file__), 'picka.json')).read())['albanian']


def age(min=1, max=99):
    return random.randint(min, max + 1)


def apartment_number():
    return ' '.join([random.choice(["apartament", "pas", "dhomë"]), str(random.randint(1, 100))])


def business_title():
    pass


def calling_code():
    pass


def calling_code_with_country():
    pass


def city():
    pass


def city_with_state():
    pass


def country():
    pass


def creditcard():
    pass


def cvv():
    pass


def email():
    pass


def fax_number():
    pass


def _female():
    return random.choice(albanian_names['female'])


def female_name():
    return _female()


def trash():
    pass


def male_full_name():
    return ' '.join([_male(), _male()])


def _male():
    return random.choice(albanian_names['male'])


def new_male_name():
    return _male()


def male_full_name_w_middle_initial():
    return ' '.join([_male(), random.choice(string.uppercase) + '.', _male()])


def gender():
    pass


def hyphenated_last_name():
    pass


def initial():
    pass


def language():
    pass


def _last_name():
    return random.choice(albanian_names['surname'])


def last_name():
    return _last_name()


def male_middle_name():
    return _male()


def male_name():
    return _male()


def month():
    pass


def month_and_day():
    pass


def month_and_day_and_year():
    pass


def name():
    pass


def number():
    pass


def password_alphabetical():
    pass


def password_numerical():
    pass


def password_alphanumeric():
    pass


def phone_number():
    pass


def random_string():
    pass


def salutation():
    pass


def screename():
    pass


def sentence():
    pass


def set_of_initials():
    pass


def social_security_number():
    pass


def special_characters():
    pass


def street_type():
    pass


def street_name():
    pass


def street_address():
    pass


def suffix():
    pass


def timestamp():
    pass


def timezone_offset():
    pass


def timezone_offset_country():
    pass


def url():
    pass


def state_abbreviated():
    pass


def postal_code():
    pass
