Picka: A Python module for data generation and randomization.
-------------------------------------------------------------

:Author:
	Anthony Long

:Version:
	
	0.94
	
	- Added >1k company names.
	
	0.93
	
	- Fixed sentence generator.
    	
	0.91
	
	- Removed sentence generator.
	- Added tests.
	- Reverted back from SQLite to JSON.


What is Picka?
______________

Picka generates randomized data either from lists of known good data (or bad) stored
in a sqlite database, or by generating randomized realistic data, using string formatting (behind the scenes). Picka has 
a function for any field you would need filled in. With `selenium`, something like would populate the "field-name-here" 
box for you, 100 times with random names.

::

	for x in xrange(101):
		self.selenium.type('field-name-here', picka.male_name())

But this is just the beginning. Other ways to implement this, include using dicts:

::

	user_information = {
		"first_name": picka.male_name(),
		"last_name": picka.last_name(),
		"email_address": picka.email(extension='.org'),
		"password": picka.password_numerical(6),
	}

This would provide:

::
    
    {
        "first_name": "Jack",
        "last_name": "Logan",
        "email_address": "uragn@getit.com",
        "password": "485444"
    }


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


