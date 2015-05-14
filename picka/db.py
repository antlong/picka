import sqlite3
from os.path import abspath, join, dirname
import random

row_counts = {}

class Queries(object):
    def __init__(self):
        dbpath = join(abspath(dirname(__file__)), 'data/db.sqlite')
        self.connect = sqlite3.connect(dbpath, isolation_level=None)
        self.connect.text_factory = lambda x: unicode(x, "utf-8", "ignore")
        self.tups = self.connect.cursor()
        self.dict = self.connect.cursor()
        self.dict.row_factory = sqlite3.Row
        self.row_counts = {}

    def dict_from_row(self, row):
        d = {}
        for idx, col in enumerate(self.dict.description):
            d[col[0]] = row[idx]
        return d

    def get_rows(self, table):
        if table not in self.row_counts:
            self.tups.execute('SELECT MAX(_ROWID_) FROM {} LIMIT 1;'.format(table))
            self.row_counts[table] = self.tups.fetchone()[0]
            return self.row_counts

    def custom_query(self, query=None, output=None):
        if output:
            self.dict.execute(query)
            return self.dict.fetchall()
        else:
            self.tups.execute(query)
            return self.tups.fetchall()

    def query_single(self, name=None, column=None, where=None, value=None):
        self.get_rows(column)
        if where and value:
            self.tups.execute('SELECT {} FROM {} WHERE {} = {}'.format(
                name, column, where, value)
            )
        else:
            self.tups.execute('SELECT {} FROM {} WHERE id = {}'.format(
                name, column, random.randint(1, self.row_counts[column]))
            )
        return self.tups.fetchone()[0]

    def query_multiple(self, name=None, table=None, where=None, value=None, output=None):
        """Grabs data from the database."""
        # Get row counts
        self.get_rows(table)
        ch = random.randint(1, self.row_counts[table])
        if where and value:
            self.dict.execute('SELECT {} FROM {} WHERE {} = {}'.format(
                name, table, where, value)
            )

        else:
            self.dict.execute('SELECT {} FROM {} WHERE id = {};'.format(name, table, ch))

        return self.dict_from_row(self.dict.fetchall()[0])

