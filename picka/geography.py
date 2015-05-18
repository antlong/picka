from attrdict import AttrDict
from sqlalchemy import text
from math import sqrt, pi, cos, sin
import random
from LatLon import LatLon


import picka_utils

engine = picka_utils.engine_connection()


def timezone_offset(dst=True, utc=True):
    """Generates a random timezone offset.

    Arguments:
      dst (bool): Enable dst selection.
      utc (bool): Enable utc offset.

    Returns:
      dst: Returns a dst offset.
      utc: Returns a utc offset.

    Examples:
      >>> timezone_offset()
      {'utc': u'+06:30', 'dst': u'-03:00'}
      >>> timezone_offset(dst=False)
      {'utc': u'+10:00'}
      >>> timezone_offset(utc=False)
      {'dst': u'-03:00'}
      >>> timezone_offset(utc=False, dst=False)
      {}
      >>> timezone_offset(utc=False).dst
      '-4:30'
    """
    data = {}

    if dst:
        res = engine.execute("select distinct(dst) from timezones where rowid = (abs(random()) % \
          (select max(rowid)+1 from timezones))")
        data["dst"] = res.fetchall()[0][0]

    if utc:
        res = engine.execute("select distinct(utc) from timezones where rowid = (abs(random()) % \
          (select max(rowid)+1 from timezones))")
        data["utc"] = res.fetchall()[0][0]

    return AttrDict(data)


def timezone_offset_country():
    """Generates a random country from the timezone country list.

    Returns:
      country (str): Name of the generated country.

    Examples:
      >>> timezone_offset_country()
      AttrDict({'country': u'Maldives'})
      >>> timezone_offset_country().country
      AttrDict({'country': u'Maldives'})
    """
    res = engine.execute("select distinct(country) from timezones \
                         where rowid = (abs(random()) % \
        (select max(rowid)+1 from timezones))")
    return AttrDict({"country": res.fetchall()[0][0]})


def lat_long(state="NY", radius=150000):
    """Generates a random latitude, and longitude.

    The lat and long will be within the radius, of the state of your choice.

    Note: The radius seems to need to be over 150,000 to produce a difference
    from the original lat and long.

    Arguments:
      state (str): The 2 letter abbreviation for the state of your choosing.
      radius (int): The radius which will be used to generate a lat and long
      inside of.

    Returns:
      abbrev (string): The 2 letter abbreviation of the chosen state.
      lat (string): A generated latitude of varying length.
      long (string): A generated longetude of varying length.

    Examples:
      >>> d_gen.lat_long("NY", 150000)
      AttrDict({
        u'lat': '41.9656885445',
        u'abbrev': u'NY',
        u'long': '-75.9459285158'
      })
      >>> lat_long("NY", 175000).lat
      '43.0438318157'
    """
    cmd = 'SELECT abbrev,lat,long FROM us_s_ll WHERE abbrev = :_st LIMIT 1;'
    res = engine.execute(text(cmd), _st=state)
    data = AttrDict([dict(d) for d in res.fetchall()][0])

    radius_in_degrees = radius / 111300

    x0 = float(data["long"])
    y0 = float(data["lat"])

    u = round(random.uniform(0.1, 1.0), 6)
    v = round(random.uniform(0.1, 1.0), 6)

    w = radius_in_degrees * sqrt(u)
    t = 2 * pi * v
    x = w * cos(t)
    y1 = w * sin(t)
    x1 = x / cos(y0)

    obj = LatLon(y0 + y1, x0 + x1).to_string()
    data["lat"] = obj[0]
    data["long"] = obj[1]

    return data
