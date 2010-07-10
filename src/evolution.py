#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Listing of available evolutions.

"""This class provides a way of querying evolutionary methods of pokemon."""

import pokedex

this = None


class Evodex:

    def __init__(self):
        self.evo = []
        data = open("evo.dat")
        for line in data:
            entry = line.split()
            self.evo.append(Evolution(entry[0], entry[1], entry[2]))
        data.close()


class Evolution:

    def __init__(self, old, method, new):
        self.old = pokedex.get_instance().dex[int(old) - 1]
        self.method = expand(method)
        self.new = pokedex.get_instance().dex[int(new) - 1]


def expand(string):
    """This method expands the shorthand evolutionary methods from their
    compressed form to a more human-readable one.

    """

    holding = {"OS": "Oval Stone", "RC": "Razor Claw", "RF": "Razor Fang"}
    knowing = {"AP": "AncientPower", "DH": "DoubleHit", "M": "Mimic",
      "RO": "Rollout"}
    location = {"217": "Route 217", "C": "Mt. Coronet", "EF": "Eterna Forest"}
    stones = {"DA": "Dawn", "DU": "Dusk", "F": "Fire", "T": "Thunder",
      "L": "Leaf", "M": "Moon", "S": "Sun", "SH": "Shiny", "W": "Water"}
    trade = {"DD": "Dubious Disc", "DS": "Dragon Scale", "DSS": "DeepSeaScale",
      "DST": "DeepSeaTooth", "E": "Electirizer", "KR": "King's Rock",
      "M": "Magmarizer", "MC": "Metal Coat", "P": "Protector",
      "RC": "ReaperCloth", "UG": "Up-Grade"}

    suffix = ""
    # Sometimes additional information is also encoded.  This information is
    # added in parentheses as a suffix and split off here.
    pivot = string.find("(")
    if not pivot == -1:
        suffix = string[pivot:]
        string = string[:pivot]

    if string.startswith("h"):      # Level while holding...
        string = "Level up holding " + holding[string[1:]]
    elif string.startswith("k"):    # Level while knowing...
        string = "Level up knowing " + knowing[string[1:]]
    elif string.startswith("l"):    # Level at location...
        string = "Level up in " + location[string[1:]]
    elif string.startswith("s"):    # Use evolutionary stone
        string = stones[string[1:]] + " Stone"
    elif string.startswith("t"):    # Trade (while holding...)
        if not len(string) == 1:
            string = " holding " + trade[string[1:]]
        else:
            string = ""
        string = "Trade" + string
    elif string == "B":
        string = "Level up with maximum Beauty"
    elif string == "H":
        string = "Happiness"
    elif string == "R":
        string = "Level up with Remoraid in party"
    elif string.startswith("L"):
        string = "Level " + string[1:]

    # Now we can deal with a suffix if one exists.
    if suffix == "(D)":
        suffix = " during the day"
    elif suffix == "(E)":
        suffix = " with a free spot"
    elif suffix == "(N)":
        suffix = " at night"
    elif suffix == "(♀)":
        suffix = " (female)"
    elif suffix == "(♂)":
        suffix = " (male)"
    elif suffix.startswith("(A") and suffix.endswith("D)"):
        suffix = " (Attack " + suffix[2] + " Defense)"

    return string + suffix


def get_instance():
    global this
    if this == None:
        this = Evodex()
    return this
