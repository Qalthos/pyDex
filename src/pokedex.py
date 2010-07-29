# -*- coding: UTF-8 -*-
"""The national pokédex."""

import pokemon

this = None
MAX_DEX = 493


class Pokedex:
    dex = []
    user_dex = []
    filename = ""

    def __init__(self):
        nat_data = open("ndex.dat")
        for line in nat_data:
            pokarray = line.split()
            if len(pokarray) == 3:
                pokarray.append("---")
            self.dex.append(pokemon.Pokemon(pokarray))
        nat_data.close()
        self.new_dex()

    def status(self, pokenum):
        temp = self.user_dex[pokenum]
        if temp == 1:
            return "missing"
        elif temp == 2:
            return "seen"
        elif temp == 4:
            return "caught"
        else:
            return "unknown"

    def valid(self, pokenum, bitstring):
        if pokenum > MAX_DEX:
            return False
        temp = int(self.user_dex[pokenum])
        try:
            if (bitstring % (temp * 2)) / temp == 1:
                return True
            else:
                return False
        except ZeroDivisionError:
            return False

    def get_filename(self):
        return self.filename

    def get_game(self):
        return self.game

    def set_filename(self, filename):
        self.filename = filename

    def new_dex(self):
        self.user_dex = [1] * (MAX_DEX + 1)


def get_instance():
    global this
    if this == None:
        this = Pokedex()
    return this
