# -*- coding: UTF-8 -*-
"""The national pokédex."""

this = None
MAX_DEX = 649


class Pokedex:
    dex = []
    user_dex = []
    unown_code = 0
    game = "Default"
    filename = ""

    def __init__(self):
        nat_data = open("data/ndex.dat")
        for line in nat_data:
            pokarray = line.split()
            if len(pokarray) == 3:
                pokarray.append("---")
            self.dex.append({"number": int(pokarray[0]), "name": pokarray[1],
              "type1": pokarray[2], "type2": pokarray[3]})
        nat_data.close()
        self.new_dex()

    def status(self, pokenum):
        try:
            temp = self.user_dex[pokenum]
        except IndexError:
            print "%d is out of user_dex" % pokenum
            return "unknown"
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
            if bitstring & temp > 0:
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
