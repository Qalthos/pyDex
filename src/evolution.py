#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Listing of available evolutions.

import pokedex

this = None


class Evodex:

    def __init__(self):
        self.evo = []
        file = open("evo.dat")
        for line in file:
            entry = line.split()
            self.evo.append(Evolution(entry[0], entry[1], entry[2]))
        file.close()


class Evolution:

    def __init__(self, old, method, new):
        self.old = pokedex.get_instance().dex[int(old) - 1]
        self.method = format(method)
        self.new = pokedex.get_instance().dex[int(new) - 1]


def format(string):
    suffix = ""
    pivot = string.find("(")
    if not pivot == -1:
        suffix = string[pivot:]
        string = string[:pivot]

    if string.startswith("h"):      # Level while holding...
        if string[1:] == "OS":
            string = "Oval Stone"
        elif string[1:] == "RC":
            string = "Razor Claw"
        elif string[1:] == "RF":
            string = "Razor Fang"
        string = "Level up holding " + string
    elif string.startswith("k"):    # Level while knowing...
        if string[1:] == "AP":
            string = "AncientPower"
        elif string[1:] == "DH":
            string = "DoubleHit"
        elif string[1:] == "M":
            string = "Mimic"
        elif string[1:] == "RO":
            string = "Rollout"
        string = "Level up knowing " + string
    elif string.startswith("l"):    # Level at location...
        if string[1:] == "217":
            string = "Route 217"
        elif string[1:] == "C":
            string = "Mt. Coronet"
        elif string[1:] == "EF":
            string = "Eterna Forest"
        string = "Level up in " + string
    elif string.startswith("s"):    # Use evolutionary stone
        if string[1:] == "DA":
            string = "Dawn"
        elif string[1:] == "DU":
            string = "Dusk"
        elif string[1:] == "F":
            string = "Fire"
        elif string[1:] == "T":
            string = "Thunder"
        elif string[1:] == "L":
            string = "Leaf"
        elif string[1:] == "M":
            string = "Moon"
        elif string[1:] == "S":
            string = "Sun"
        elif string[1:] == "SH":
            string = "Shiny"
        elif string[1:] == "W":
            string = "Water"
        string = string + " Stone"
    elif string.startswith("t"):    # Trade (while holding...)
        if not len(string) == 1:
            if string[1:] == "DD":
                string = "Dubious Disc"
            elif string[1:] == "DS":
                string = "Dragon Scale"
            elif string[1:] == "DSS":
                string = "DeepSeaScale"
            elif string[1:] == "DST":
                string = "DeepSeaTooth"
            elif string[1:] == "E":
                string = "Electirizer"
            elif string[1:] == "KR":
                string = "King's Rock"
            elif string[1:] == "M":
                string = "Magmarizer"
            elif string[1:] == "MC":
                string = "Metal Coat"
            elif string[1:] == "P":
                string = "Protector"
            elif string[1:] == "RC":
                string = "ReaperCloth"
            elif string[1:] == "UG":
                string = "Up-Grade"
            string = " holding " + string
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
