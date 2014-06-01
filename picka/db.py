#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
db adds database support for data generation and randomization to picka.
Testers can create their templates that are indexed to generate test data for
testing new User and other tests where unique entry is necessary.
db supports storing lists of values that can be accessed sequentially or randomly.

Testers can continue testing with less thought on what will be a value for this run.
Those decision can be made when tests are developed and will not interrupt a test session.

By: Bernard Kuehlhorn
"""

from itertools import izip
from functools import partial
import string
import random
import time
import datetime
import sqlite3
import os
import re
import calendar
import linecache

__docformat__ = 'restructuredtext en'

connect = \
    sqlite3.connect(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'db.sqlite'))
cursor = connect.cursor()

def random_fib(number=4, start=0):
    """
    :param number: Number of entries for width of random selection
    :param start: Starting point on Fibonacci sequence for weighting
    :return: Random number with Fibonacci weighting. Each successive value is twice probable as prior.

    """
    fib_sequence = [1, 2, 3, 5, 8, 13, 21, 1000]
    fib_list = []
    end = min(start+number, len(fib_sequence)-1)
    for i in fib_sequence[start:end]:
        fib_list.extend([i]*i)
    return fib_sequence.index(random.choice(fib_list))-start

def isodate(start=1900, end=2010):
    """
    Selects a monday, day and year for you.
    Logic built in to handle day in month.
    To change month do (a, b). b has +1 so the
    last year in your range can be selected. Default is 1900, 2010.
    """
    start_date = calendar.datetime.date(start, 1, 1)
    end_date = calendar.datetime.date(end, 12, 31)
    random_date = random.randint(datetime.datetime.toordinal(start_date), datetime.datetime.toordinal(end_date))
    return datetime.datetime.isoformat(datetime.datetime.fromordinal(random_date)).split('T')[0]

def pattern_next(pattern, tester=None, sut=None, DEBUG=False):
    """ Make a unique Applicant name from starter for next test in a run.

    :param pattern: Initial patters for test data. Index is added by format()
    :param tester: User id for Tester running test.
    :param sut: System Under Test. Allows for testers to be testing several systems.
    :return: pattern with next index to make unique for test run

    sqlite table creation:
        CREATE TABLE pattern
        (
            pattern char(50) NOT NULL,
            pattern_number int NOT NULL,
            tester char(50) DEFAULT NULL,
            sut char(50) DEFAULT NULL 
        );

    create table if not exists pattern (pattern char(40) not null, pattern_number int, tester, sut)

    pickabk.admissions.next_pattern(os.environ.get('USER'), 'Frank{0}')
    """
    sel = "SELECT pattern_number FROM pattern where (pattern=? and tester = ? and sut = ?)"
    # print sel
    try:
        cursor.execute(sel, (pattern, tester, sut))
        index =  cursor.fetchone()   # update that index is used
        if index is None:
            index = 0
            sel = "insert into pattern (pattern, pattern_number, tester, sut) values (?, ?, ?, ?);"
        else:
            index = index[0]
            if not DEBUG:
                index += 1
                sel = "update pattern_name set pattern_number = ? where (pattern=? and tester = ? and sut = ?);"
    except IOError, e:
        print "Error {0}: {1}".format(e.args[0], e.args[1])
        index = 0
    # print 'insert/update: ', sel
    cursor.execute(sel, (index, pattern, tester, sut))
    connect.commit()
    # cursor.execute('commit ;')
    # print ('new start: ', spickabk.number()tarter.format(index))
    return (pattern.format(index))

def pattern_curr(pattern, tester=None, sut=None, DEBUG=False):
    """ Make current Applicant name from pattern for next test in a run.

    :param pattern: Initial patters for test data. Index is added by format()
    :param tester: User id for Tester running test.
    :return: Applicant name with next index to make unique for test run

    sqlite table creation:

    create table if not exists pattern_name (tester not null, pattern_name char(40) not null, pattern_number int)

    pickabk.admissions.next_pattern(os.environ.get('USER'), 'Frank{0}')
    """
    sel = "SELECT pattern_number FROM pattern_name where (tester = ? and pattern_name=?)"
    # print sel
    try:
        cursor.execute(sel, (tester, pattern))
        index =  cursor.fetchone()   # update that index is used
        if index is None:
            index = 0
            sel = "insert into pattern_name (pattern_number, tester, pattern_name) values (?, ?, ?);"
        else:
            index = index[0]
    except IOError, e:
        print "Error {0}: {1}".format(e.args[0], e.args[1])
        index = 0
    return (pattern.format(index))

def pattern_reset(pattern=None, tester=None, sut=None, adjust=None):
    """ Reset Applicants for new test run. Reset can be done by several means

    :param tester: User id for Tester running test.
    :param pattern: Initial patters for Applicant first name to reset. Reset all for Tester if None
    :param adjust: None: resets index to -1, negative value: index is reduced by abs of adjust, otherwise: set index to adjust
    :return: None

    pickabk.admissions.reset_pattern(os.environ.get('USER'), 'Frank{0}')
    """
    cursor_update = connect.cursor()
    rows_updated = []
    if pattern is None:
        sel = 'select pattern_number, tester, pattern_name from pattern_name where tester = ? and sut = ?'
        rows = cursor.execute(sel, (tester,))
    else:
        sel = 'select pattern_number, tester, pattern_name from pattern_name where tester = ? and pattern_name = ? and sut = ?'
        rows = cursor.execute(sel, (tester, pattern))
    # print 'sel: ', sel

    sel = "update pattern_name set pattern_number = ? where (tester = ? and pattern_name=? and sut = ?);"
    for row in cursor:
        # print 'reset: ', row
        if adjust is None:
            new_pattern_number = 0
        else:
            adjust = int(adjust)
            if adjust < 0:
                new_pattern_number = max( -1, (row[0] + adjust))
            else:
                new_pattern_number = adjust
        cursor_update.execute(sel, (new_pattern_number, row[1], row[2], sut))
        rows_updated.append(row[2])
    connect.commit()
    return rows_updated

def next_in_group(rowkey):
    """ Select next entry in rowkey from select_entry table

    :param rowkey: key to access row
    :return:

    sqlite table creation:

    create table if not exists select_row (rowkey PRIMARY KEY unique , next_select, entries)

    """
    sel = "SELECT next_select, entries FROM select_row where rowkey = ?"
    try:
        cursor.execute(sel, (rowkey,))
        row =  cursor.fetchone()   # update that index is used
        if row is None:
            return None
        else:
            index = row[0]
            entries = row[1]
            return_value = json.loads(entries)[index]
            index = min(index + 1, len(entries)-1)
            sel = "update select_row set next_select = ? where (rowkey = ?);"
    except IOError, e:
        print "Error {0}: {1}".format(e.args[0], e.args[1])
        return None
    # print 'insert/update: ', sel
    # print 'update:', rowkey, index, return_value
    # print 'sel:', sel
    cursor.execute(sel, (index, rowkey))
    connect.commit()
    # cursor.execute('commit ;')
    # print ('new start: ', spickabk.number()tarter.format(index))
    return return_value

def current_in_group(rowkey):
    """ Select current entry in rowkey from select_entry table

    :param rowkey: key to access row
    :return:

    sqlite table creation:

    create table if not exists select_row (rowkey PRIMARY KEY unique , next_select, entries)

    """
    sel = "SELECT next_select, entries FROM select_row where rowkey = ?"
    try:
        cursor.execute(sel, (rowkey,))
        row =  cursor.fetchone()   # update that index is used
        if row is None:
            return None
        else:
            index = row[0]
            entries = row[1]
            x = json.loads(entries)
            return_value = json.loads(entries)[index]
    except IOError, e:
        print "Error {0}: {1}".format(e.args[0], e.args[1])
        return None
    return return_value

def reset_in_group(rowkey, index=None):
    """ Reset the next entry to start of list in rowkey

    :param rowkey: key to access row
    :param index: Set index to specific value. None decrease index by 1, min zero. No check on range and can be broken
    :return:
    """
    cursor_update = connect.cursor()
    sel = "SELECT next_select, entries FROM select_row where rowkey = ?"
    try:
        cursor.execute(sel, (rowkey,))
        row =  cursor.fetchone()   # update that index is used
        if row is None:
            return None
        else:
            if index is None:
                index = min(0, len(row[1])-1)
            else:
                index = int(index)
                if index < 0:
                    index = max(row[0] + index, 0)
            sel = "update select_row set next_select = ? where (rowkey = ?);"
    except IOError, e:
        print "Error {0}: {1}".format(e.args[0], e.args[1])
        return None
    cursor_update.execute(sel, (index, rowkey))
    connect.commit()
    return

def load_in_group(rowkey, entries):
    """ Initialize rowkey with entries.

    Table:

    :param rowkey: key to access row
    :param entries: new list for rowkey. reset row to give first entry
    :return:


    """
    sel = "insert or replace into select_row (rowkey, next_select, entries) values(?, 0, ?);"
    e = json.dumps(entries)
    cursor.execute(sel, (rowkey, json.dumps(entries)))
    # print "sel:", sel
    connect.commit()
    return

def get_in_group(rowkey, select=None):
    """ Initialize rowkey with entries.

    Table:

    :param rowkey: key to access row
    :param select: List of elements to return from entry in table. None or empty returns entire list
    :return: get index and entries from rowkey, if select is used: [0, selected]


    """
    sel = "select next_select, entries from select_row where rowkey = ?;"
    rows = cursor.execute(sel, (rowkey,)).fetchone()
    if select is None:
        return [rows[0], json.loads(rows[1])]

    retList = []
    data = json.loads(rows[1])
    if isinstance(data, list):
        if len(select)==0: return [rows[0], json.loads(rows[1])]
        for each in select:
            retList.append(data[each if each>-len(data) and each<len(data) else -len(data)+1 if each<0 else len(data)-1])
    if isinstance(data, dict):
        if len(select)==0: return [rows[0], json.loads(rows[1])]
        for each in select:
            retList.append(data.get(each, None))
    return [0, retList]
