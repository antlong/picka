from peewee import *

from ..picka_utils import query as _query

def male():
    return _query("name", "male")

def test_peewee():
    from playhouse.csv_loader import *
    db = SqliteDatabase(':memory:')
    ZipToTZ = load_csv(db, 'names.csv')
    ZipToTZ.get().timezone