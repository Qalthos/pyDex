# -*- coding: UTF-8 -*-
"""This class provides a way of querying evolutionary methods of pokemon."""

import pokedex

this = None


class Evodex:

    def __init__(self):
        self.evo = {"evolution": [], "prevolution": []}
        dex = pokedex.get_instance().dex
        
        data = open("data/evo.dat")
        for line in data:
            entry = line.split()
            # pokedex unfortunately doesn't have a placeholder at 0
            self.evo["evolution"].append({
              "old": dex[int(entry[0]) - 1],
              "method": expand(entry[1]),
              "new": dex[int(entry[2]) - 1]
            })
            self.evo["prevolution"].append({
              "old": dex[int(entry[2]) - 1],
              "method": "Breed normally",
              "new": dex[int(entry[0]) - 1]
            })
        data.close()
        
        data = open("data/prevo.dat")
        for line in data:
            entry = line.split()
            parents = entry[0].split(",")
            for parent in parents:
                for prevo in self.evo["prevolution"]:
                    if prevo["old"] == parent:
                        prevo["method"] = entry[1]
        data.close()


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
    other = {"B": "Level up with maximum Beauty", "H": "Happiness",
      "R": "Level up with Remoraid in party"}

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
    elif string.startswith("L"):
        string = "Level " + string[1:]
    else:
        string = other[string]

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
