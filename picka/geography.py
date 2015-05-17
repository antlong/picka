from attrdict import AttrDict
from sqlalchemy import text
from math import sqrt, pi, cos, sin
import random
from decimal import Decimal
from LatLon import LatLon, Latitude, Longitude


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


def lat_long(state="NY", radius=1000000):
    """Generates a random latitude, and longitude.

    The lat and long will be within the radius of a state of your choice.

    Arguments:
      state (str): The 2 letter abbreviation for the state of your choosing.
      radius (int): The radius which will be used to generate a lat and long
      inside of.

    Examples:
      >>> lat_long("NY", 1000000)
      AttrDict({u'lat': 42.15, u'state': u'NY', u'long': -74.94})
      >>> lat_long("NY", 10000).lat
      u'lat': 42.15
    """
    cmd = 'SELECT state,lat,long FROM us_s_ll WHERE state = :_st LIMIT 1;'
    res = engine.execute(text(cmd), _st=state)
    data = AttrDict([dict(d) for d in res.fetchall()][0])

    radius_in_degrees = radius / 111300

    x0 = float(data["long"])
    y0 = float(data["lat"])

    u = round(random.uniform(0.1, 1.0), 4)
    v = round(random.uniform(0.1, 1.0), 4)

    w = radius_in_degrees * sqrt(u)
    t = 2 * pi * v
    x = w * cos(t)
    y1 = w * sin(t)
    x1 = x / cos(y0)

    obj = LatLon(y0 + y1, x0 + x1).to_string()
    data["lat"] = obj[0]
    data["long"] = obj[1]

    return data
