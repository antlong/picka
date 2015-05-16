from sqlalchemy import create_engine, text
from sqlalchemy.orm import class_mapper

engine = create_engine('sqlite:///picka/data/db.sqlite', echo=True)


def asdict(obj):
    return dict((col.name, getattr(obj, col.name))
                for col in class_mapper(obj.__class__).mapped_table.c)


def calling_code(country=False):
    if country:
        cmd = 'select * from calling_codes where country like :_country limit 1;'
        res = engine.execute(text(cmd), _country=country)
        return [dict(d) for d in res.fetchall()]

    else:
        res = engine.execute(
            "select calling_code, country from calling_codes \
            where rowid = (abs(random()) % (select max(rowid)+1 from calling_codes))"
        )
        return [dict(d) for d in res.fetchall()]
