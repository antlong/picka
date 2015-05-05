#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Picka is a data generation and randomization module which aims to increase
coverage by increasing the amount of tests you _dont_ have to write
by hand.
By: Anthony Long
"""

import random as _random
import sqlite3 as _sqlite3
import os as _os
import linecache as _linecache

_connect = \
    _sqlite3.connect(_os.path.join(_os.path.abspath(
        _os.path.dirname(__file__)), 'db.sqlite'))
_connect.text_factory = str
_cursor = _connect.cursor()


def street_type():
    """Returns a Canadian street type."""
    return _random.choice(
        [
            "Abbey", "Acres", "Allée", "Alley", "Autoroute", "Avenue",
            "Bay", "Beach", "Bend", "Boulevard", "By-pass", "Byway",
            "Campus", "Cape", "Carré", "Carrefour", "Centre", "Cercle",
            "Chase", "Chemin", "Circle", "Circuit", "Close", "Common",
            "Concession", "Corners", "Côte", "Cour", "Cours", "Court",
            "Cove", "Crescent", "Croissant", "Crossing", "Cul-de-sac"
            "Dale", "Dell", "Diversion", "Downs", "Drive", "Échangeur",
            "End", "Esplanade", "Estates", "Expressway", "Extension",
            "Farm", "Field", "Forest", "Freeway", "Front", "Gardens",
            "Gate", "Glade", "Glen", "Green", "Grounds", "Grove",
            "Harbour", "Heath", "Heights", "Highlands", "Highway",
            "Hill", "Hollow", "Île", "Impasse", "Inlet", "Island",
            "Key", "Knoll", "Landing", "Lane", "Limits", "Line",
            "Link", "Lookout", "Loop", "Mall", "Manor", "Maze",
            "Meadow", "Mews", "Montée", "Moor", "Mount", "Mountain",
            "Orchard", "Parade", "Parc", "Park", "Parkway",
            "Passage", "Path", "Pathway", "Pines", "Place",
            "Plateau", "Plaza", "Point", "Pointe", "Port",
            "Private", "Promenade", "Quai", "Quay", "Ramp",
            "Rang", "Range", "Ridge", "Rise", "Road",
            "Rond-point" "Route", "Row", "Rue", "Ruelle",
            "Run", "Sentier", "Square", "Street", "Subdivision",
            "Terrace", "Terrasse", "Thicket", "Towers",
            "Townline", "Trail", "Turnabout", "Vale", "Via",
            "View", "Village", "Villas", "Vista", "Voie", "Walk",
            "Way", "Wharf", "Wood", "Wynd"
        ]
    )


def province():
    """Returns a list, full name and postal abbreviation"""
    return _random.choice(
        [
            ["Ontario", "ON"],
            ["Quebec", "QC"],
            ["Nova Scotia", "NS"],
            ["New Brunswick", "NB"],
            ["Manitoba", "MB"],
            ["British Columbia", "BC"],
            ["Prince Edward Island", "PE"],
            ["Saskatchewan", "SK"],
            ["Alberta", "AB"],
            ["Newfoundland and Labrador", "NL"]
        ]
    )


def postal():
    """Returns a valid postal code"""
    return _linecache.getline(
        _os.path.join(_os.path.abspath(_os.path.dirname(__file__)), 'ca_postal_codes.csv'),
        _random.randrange(0, 917358)
    ).strip("\n")


def city():
    """Returns a valid Canadian city"""
    _cursor.execute('SELECT DISTINCT(name) FROM ca_cities where name is not null order by random() limit 1;')
    return _cursor.fetchone()[0].decode("utf-8")


def lat_long():
    """Returns a valid lat long."""
    return _linecache.getline(
        _os.path.join(_os.path.abspath(_os.path.dirname(__file__)), 'ca_lat_long.csv'),
        _random.randrange(0, 917358)
    ).strip("\n")
