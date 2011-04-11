Picka: Data Generation, and Randomization.
==========================================
:Title: Picka
:Author: Anthony Long
:Modified: 2/5/2010

What is Picka?
--------------

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

	cursor.execute("insert into user_data (first_name, last_name, age) VALUES (?, ?, ?)", (pick.male_first_name, picka.last_name, picka.age))


HTTP
____

::

	def post(host, path, data, type=None):
	    http = httplib.HTTP(host)
	    http.putrequest("PUT", path)
	    http.putheader("User-Agent", USER_AGENT)
	    http.putheader("Host", host)
	    if type:
	        http.putheader("Content-Type", type)
	    http.putheader("Content-Length", str(len(data)))
	    http.endheaders()
	    http.send(data)
	
	def test_post_result():
	    post("www.spam.egg", "/bacon.htm", picka.random_string(10), "text/plain")
		errcode, errmsg, headers = http.getreply()
	    if errcode != 200:
	        raise Error(errcode, errmsg, headers)
	    file = http.getfile()
	    return file.read()

