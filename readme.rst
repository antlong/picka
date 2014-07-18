Picka: A Python module for data generation and randomization.
-------------------------------------------------------------

:Author:
	Anthony Long

:Version:
	0.96
	
	- rbg, image, hex_color, and more.
    

What is Picka?
______________

Picka generates randomized data for testing. 

Data is generated both from a database of known good data (which is included), or by generating realistic data (valid), using string formatting (behind the scenes). 

Picka has a function for any field you would need filled in. With `selenium`, something like would populate the "field-name-here" 
box for you, 100 times with random names.

::

	for x in xrange(101):
		self.selenium.type('field-name-here', picka.male_name())

But this is just the beginning. Other ways to implement this, include using dicts:

::

	user_information = {
		"first_name": picka.male_name(),
		"last_name": picka.last_name(),
		"email_address": picka.email(10, extension='example.org'),
		"password": picka.password_numerical(6),
	}

This would provide:

::
    
    {
        "first_name": "Jack",
        "last_name": "Logan",
        "email_address": "uragnscsah@example.org",
        "password": "485444"
    }

Don't forget, since all of the data is considered "clean" or valid - you can also use it to fill selects and other form fields with pre-defined values. For example, if you were to generate a state; picka.state() the result would be "Alabama". You can use this result to directly select a state in an address drop-down box.


Examples:
---------

Selenium
________

::

	def search_for_garbage():
		selenium.open('http://yahoo.com')
		selenium.type('id=search_box', picka.random_string(10))
		selenium.submit()
	
	def test_search_for_garbage_results():
		search_for_garbage()
		selenium.wait_for_page_to_load('30000')
		assert selenium.get_xpath_count('id=results') == 0
	
Webdriver
_________

::

    driver = webdriver.Firefox()
    driver.get("http://somesite.com")
    x = {
        "name": [
            "#name",
            picka.name()
        ]
    }
    driver.find_element_by_css_selector(
        x["name"][0]).send_keys(x["name"][1]
    )
    
Funcargs / pytest
_________________

::

	def pytest_generate_tests(metafunc):
		if "test_string" in metafunc.funcargnames:
			for i in range(10):
				metafunc.addcall(funcargs=dict(numiter=picka.random_string(20)))
	
	def test_func(test_string):	
		assert test_string.isalpha()
		assert len(test_string) == 20


MySQL / SQLite
______________

::

    first, last, age = picka.first_name(), picka.last_name(), picka.age()
    cursor.execute(
	   "insert into user_data (first_name, last_name, age) VALUES (?, ?, ?)",
	   (first, last, age)
    )
    

HTTP
____

::

	def post(host, data):
	    http = httplib.HTTP(host)
	    return http.send(data)
	
	def test_post_result():
	    post("www.spam.egg/bacon.htm", picka.random_string(10))


A More Useful Picka
___________________
Picka can be more useful by allowing developers and testers to add their own data. picka.db
provide functions to create an pattern that returns a unique entry each time. Consider user
names. Each user name must be unique. Changing a test is a problem. picka.db allow for a
pattern of user name to include a number to make each one unique. Different tests use
patterns to prevent collisions.

Another set of functions allow developers and testers to create their own lists for testing.
Tests can step through the list or randomly select a value.

Picka.db for Patterns
_____________________

pattern_next(pattern, tester=None, sut=None, DEBUG=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Make a unique Applicant name from starter for next test in a run.

    :param pattern: Initial patters for test data. Index is added by format()
    :param tester: User id for Tester running test.
    :param sut: System Under Test. Allows for testers to be testing several systems.
    :return: pattern with next index to make unique for test run

    sqlite table creation:
::

        CREATE TABLE if not exists pattern
        (
            pattern char(50) NOT NULL,
            pattern_number int NOT NULL,
            tester char(50) DEFAULT NULL
        );

pattern_curr(pattern, tester=None, sut=None, DEBUG=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Make current Applicant name from pattern for next test in a run.

    :param pattern: Initial patters for test data. Index is added by format()
    :param tester: User id for Tester running test.
    :return: pattern with next index to make unique for test run


pattern_reset(pattern=None, tester=None, sut=None, adjust=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Reset Applicants for new test run. Reset can be done by several means

    :param tester: User id for Tester running test.
    :param pattern: Initial patters for Applicant first name to reset. Reset all for Tester if None
    :param adjust: None: resets index to -1, negative value: index is reduced by abs of adjust, otherwise: set index to adjust
    :return: Pattern that was updated

Webdriver
_________

Use Pattern to create a unique name for each test run. Between runs, last name can be used
in different tests.

::

    driver = webdriver.Firefox()
    driver.get("http://somesite.com")
    x = {
        "name": [
            "#name",
            test_data = picka.db.pattern_next('testName{0:0}', "me")
        ]
    }
    driver.find_element_by_css_selector(
        x["name"][0]).send_keys(x["name"][1]
    )

Funcargs / pytest
_________________

::

	def pytest_generate_tests(metafunc):
		if "test_string" in metafunc.funcargnames:
			for i in range(10):
				metafunc.addcall(funcargs=dict(numiter=picka.db.pattern_next('testName{0:0}', "me")))

	def test_func(test_string):
		assert test_string.isalpha()
		assert len(test_string) == 20

Picka.db for Lists
__________________


next_in_group(rowkey)
^^^^^^^^^^^^^^^^^^^^^
    Select next entry in rowkey from select_entry table

    Table: data_lists

    :param rowkey: key to access row
    :return: Next index into list or None if not valid index

    sqlite table creation:
::

    CREATE TABLE if not exists data_lists
    (
        rowkey TEXT PRIMARY KEY,
        next_select TEXT,
        entries TEXT
    );

current_in_group(rowkey)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Select current entry in rowkey from select_entry table

    Table: data_lists

    :param rowkey: key to access row
    :return: Current index into list or None if not valid index

adjust_in_group(rowkey, change=-1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Reset the next entry to start of list in rowkey

    Table: data_lists

    :param rowkey: key to access row
    :param change: Change index by change number. Default is -1. Limit of index after change is +-(len(list)-1)
    :return: None

reset_in_group(rowkey, index=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Reset the next entry to start of list in rowkey

    Table: data_lists

    :param rowkey: key to access row
    :param index: Set index to specific value. None decrease index by 1, min zero. No check on range and can be broken
    :return:

load_in_group(rowkey, entries)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Initialize rowkey with entries.

    Table: data_lists

    :param rowkey: key to access row
    :param entries: new list for rowkey. reset row to give first entry
    :return:


dump_in_group(rowkey)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Dump rowkey with index, entries.

    Table: data_lists

    :param rowkey: key to access row
    :return: (index, list of entries)

get_in_group(rowkey, select=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Initialize rowkey with entries.

    Table: data_lists

    :param rowkey: key to access row
    :param select: List of elements to return from entry in table. None or empty returns entire list
    :return: get index and entries from rowkey, if select is used: [0, selected]

Initialize list with Python
___________________________
Add to initialization test run. Not part of initialization of test cases. Use when starting
set of tests for a release.

::

    name = 'int_list'
    int_list = range(100)
    load_in_group(name, int_list)

Webdriver
_________
Get next in group for selenium test.

::

    driver = webdriver.Firefox()
    driver.get("http://somesite.com")
    x = {
        "name": [
            "#name",
            test_data = db.next_in_group('int_list')
        ]
    }
    driver.find_element_by_css_selector(
        x["name"][0]).send_keys(x["name"][1]
    )

Funcargs / pytest
_________________

::

	def pytest_generate_tests(metafunc):
		if "test_string" in metafunc.funcargnames:
			for i in range(10):
				metafunc.addcall(funcargs=dict(numiter=db.next_in_group('int_list')))

	def test_func(test_string):
		assert test_string.isalpha()
		assert len(test_string) == 20

