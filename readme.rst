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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Make a unique Applicant name from starter for next test in a run.

    :param pattern: Initial patters for test data. Index is added by format()
    :param tester: User id for Tester running test.
    :param sut: System Under Test. Allows for testers to be testing several systems.
    :return: pattern with next index to make unique for test run

..

    sqlite table creation:
        CREATE TABLE pattern
        (
            pattern char(50) NOT NULL,
            pattern_number int NOT NULL,
            tester char(50) DEFAULT NULL
        );

    create table if not exists pattern (pattern char(40) not null, pattern_number int, tester, sut)

    pickabk.admissions.next_pattern(os.environ.get('USER'), 'Frank{0}')

pattern_curr(pattern, tester=None, sut=None, DEBUG=False)
----------------------------------------------------------
    Make current Applicant name from pattern for next test in a run.

    :param pattern: Initial patters for test data. Index is added by format()
    :param tester: User id for Tester running test.
    :return: Applicant name with next index to make unique for test run

    sqlite table creation:

    create table if not exists pattern_name (tester not null, pattern_name char(40) not null, pattern_number int)

    pickabk.admissions.next_pattern(os.environ.get('USER'), 'Frank{0}')

pattern_reset(pattern=None, tester=None, sut=None, adjust=None)
----------------------------------------------------------------
    Reset Applicants for new test run. Reset can be done by several means

    :param tester: User id for Tester running test.
    :param pattern: Initial patters for Applicant first name to reset. Reset all for Tester if None
    :param adjust: None: resets index to -1, negative value: index is reduced by abs of adjust, otherwise: set index to adjust
    :return: None

    pickabk.admissions.reset_pattern(os.environ.get('USER'), 'Frank{0}')