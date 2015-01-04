# -*- coding: UTF-8 -*-
"""This class provides a way of querying evolutionary methods of pokemon."""

from pydex import pokedex

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

        self.evolved = [x['new']['number'] for x in self.evo['evolution']]

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

    holding = {
        "OS": "Oval Stone", "RaC": "Razor Claw", "RF": "Razor Fang",
        "DD": "Dubious Disc", "DS": "Dragon Scale", "DSS": "DeepSeaScale",
        "DST": "DeepSeaTooth", "E": "Electirizer", "KR": "King's Rock",
        "M": "Magmarizer", "MC": "Metal Coat", "P": "Protector",
        "ReC": "Reaper Cloth", "UG": "Up-Grade", 'WD': 'Whipped Dream',
    }
    knowing = {"AP": "AncientPower", "DH": "Double Hit", "M": "Mimic",
      "RO": "Rollout"}
    location = {
        "217": "Route 217", "C": "Mt. Coronet", "EF": "Eterna Forest",
        'Ra': 'rain',
    }
    stones = {"Da": "Dawn", "Du": "Dusk", "Fi": "Fire", "Th": "Thunder",
      "Le": "Leaf", "Mo": "Moon", "Su": "Sun", "Sh": "Shiny", "Wa": "Water"}
    trade = {"Sh": "Shelmet", "Ka": "Karrablast"}
    with_ = {
        "B": "maximum Beauty", 'D': 'Dark type in party',
        "R": "Remoraid in party", 'U': '3DS held upside down',
    }
    other = {"H": "Happiness"}

    suffix = ""
    # Sometimes additional information is also encoded.  This information is
    # added in parentheses as a suffix and split off here.
    pivot = string.find("(")
    if not pivot == -1:
        suffix = string[pivot:]
        string = string[:pivot]

    end =  string[1:]
    if string[0] == "L":
        if end in holding:      # Level up holding [item]
            end = "up holding %s" % holding[end]
        elif end in knowing:    # Level up knowing [move]
            end = "up knowing %s" % knowing[end]
        elif end in location:    # Level up at [location]
            end = "up in %s" % location[end]
        elif end in with_:    # Level up with [condition]
            end = "up with %s" % with_[end]
        string = "Level %s" % (end)
    elif string[0] == "s":    # Use evolutionary stone
        string = "%s Stone" % stones[end]
    elif string[0] == "t":
        if end in holding:    # Trade holding [item]
            end = " holding %s" % holding[end]
        elif end in trade:    # Trade for [pokemon]
            end = " for %s" % trade[end]
        string = "Trade%s" % end
    else:
        string = other[string]

    # Now we can deal with a suffix if one exists.
    if suffix == "(D)":
        suffix = " (day)"
    elif suffix == "(E)":
        suffix = " with a free spot"
    elif suffix == "(N)":
        suffix = " (night)"
    elif suffix == "(F)":
        suffix = " (female)"
    elif suffix == "(M)":
        suffix = " (male)"
    elif suffix.startswith("(A") and suffix.endswith("D)"):
        suffix = " (Attack " + suffix[2] + " Defense)"

    return string + suffix


def get_instance():
    global this
    if this == None:
        this = Evodex()
    return this
