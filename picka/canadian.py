#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Picka is a data generation and randomization module which aims to increase
coverage by increasing the amount of tests you _dont_ have to write
by hand.
By: Anthony Long
"""

import random


def street_type():
    return random.choice(
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
