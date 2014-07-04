#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sqlite3
import os
import unittest
import picka
import db

connect = \
    sqlite3.connect(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'db.sqlite'))
cursor = connect.cursor()

class TestPatterFunctions(unittest.TestCase):

    def setUp(self):
        delete_cmd = 'DELETE FROM pattern;'
        cursor.execute(delete_cmd)
        connect.commit()

    def test_new_pattern_next(self):
        pattern = 'test{0:0}'
        test_data = db.pattern_next(pattern, "me")
        assert test_data == pattern.format(0)
        assert db.pattern_next(pattern, "me") == pattern.format(1)
        assert db.pattern_next(pattern, "me") == pattern.format(2)
        assert db.pattern_curr(pattern, "me") == pattern.format(2)
        assert db.pattern_curr(pattern, "me") == pattern.format(2)
        assert db.pattern_curr(pattern, "me") == pattern.format(2)
        assert db.pattern_curr(pattern, "me") == pattern.format(2)
        assert db.pattern_next(pattern, "me") == pattern.format(3)
        assert db.pattern_curr(pattern, "me") == pattern.format(3)

class TestListFunctions(unittest.TestCase):

    def setUp(self):
        delete_cmd = 'DELETE FROM data_lists;'
        cursor.execute(delete_cmd)
        connect.commit()

    def test_int_list(self):
        name = 'int'
        int_list = range(10)

        db.load_in_group(name, int_list)
        dump = db.dump_in_group(name)
        assert (int_list == dump[1])

        for each in int_list:
            #print each
            assert (each == db.next_in_group(name))
            assert (each == db.current_in_group(name))

        rand_set = random.randint(0, len(int_list))
        db.reset_in_group(name, rand_set)
        assert (int_list[rand_set] == db.current_in_group(name))

        rand_adj = random.randint(0, len(int_list))
        db.adjust_in_group(name, rand_adj)
        set = min(max(rand_set+rand_adj, 0), len(int_list)-1)
        assert (int_list[set] == db.current_in_group(name))
        rand_adj = -random.randint(0, len(int_list))

        db.adjust_in_group(name, rand_adj)
        set = min(max(set+rand_adj, 0), len(int_list)-1)
        assert (int_list[set] == db.current_in_group(name))

        rand_adj = random.randint(0, len(int_list)-1)
        db.reset_in_group(name, rand_adj)
        assert (int_list[rand_adj] == db.current_in_group(name))
        assert (int_list[rand_adj+1] == db.next_in_group(name))



if __name__ == '__main__':
    unittest.main()

assert picka.phone_number()
assert picka.last_name()
assert picka.random_string(8)
assert picka.sentence()
assert picka.sentence_actual()
assert picka.timezone_offset()
assert picka.language()
assert picka.timezone_offset_country()
assert picka.screename()
assert picka.number(10)
assert picka.month()
assert picka.month_and_day_and_year()
assert picka.special_characters(8)
assert picka.postal_code()
assert picka.apartment_number()
assert picka.gender()
assert picka.salutation()
assert picka.creditcard('visa')
assert picka.male_middle_name()
assert picka.city()
assert picka.male_full_name_w_middle_initial()
assert picka.state_abbreviated()
assert picka.street_name()
assert picka.initial()
assert picka.calling_code_with_country()
assert picka.surnames()
assert picka.business_title()
assert picka.male_middle()
assert picka.trash(picka.male_first)
assert picka.female_first()
assert picka.calling_code()
assert picka.male_first()
assert picka.timestamp()
assert picka.hyphenated_last_name()
assert picka.fax_number()
assert picka.male_full_name()
assert picka.password_alphanumeric(8)
assert picka.birthday()
assert picka.social_security_number()
assert picka.set_of_initials()
assert picka.female_middle()
assert picka.month_and_day()
assert picka.password_alphabetical(8)
assert picka.name()
assert picka.cvv(3)
assert picka.country()
assert picka.age()
assert picka.city_with_state()
assert picka.email()
assert picka.female_name()
assert picka.street_type()
assert picka.suffix()
assert picka.url(10)
assert picka.password_numerical(10)
assert picka.street_address()
assert picka.language()
assert len(picka.barcode("EAN-8")) == 8
assert len(picka.barcode("EAN-13")) == 13
#assert picka.locale()
assert picka.mime_type()
