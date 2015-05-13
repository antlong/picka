import apsw
from os.path import abspath, join, dirname
import random

row_counts = None
cursor = None

def get_row_counts():
    global row_counts
    if not row_counts:
        row_counts = {}
    return row_counts


def get_cursor():
    global cursor
    if not cursor:
        connect = apsw.Connection(join(abspath(
            dirname(__file__)), 'data/db.sqlite')
        )
    return connect.cursor()


def query(name=None, column=None, where=None, value=None, quantity=None, custom=None):
    """
    Grabs data from the database.
    """
    try:
        if not cursor and row_counts:
            pass
    except Exception:
        cursor = get_cursor()
        row_counts = get_row_counts()
    if custom:
        cursor.execute(custom)
        return cursor.fetchall()
    if column not in row_counts:
        cursor.execute('SELECT MAX(_ROWID_) FROM {} LIMIT 1;'.format(column))
        row_counts[column] = cursor.fetchone()[0]
    if where and value:
        cursor.execute('SELECT {} FROM {} WHERE {} = {}'.format(
            name, column, where, value )
        )
    else:
        cursor.execute('SELECT {} FROM {} WHERE id = {}'.format(
            name, column, random.randint(1, row_counts[column]))
        )
    if not quantity:
        data = cursor.fetchone()
    else:
        data = cursor.fetchall()
    return data if len(name.split()) > 1 else data[0]
