# -*- coding: UTF-8 -*-
"""The national pokédex."""

import re

this = None
MAX_DEXEN = [0, 151, 251, 386, 496, 649]
GAME_DATA = {"Red": {"gen": 1, "region": 1},
             "Blue": {"gen": 1, "region": 1},
             "Yellow": {"gen": 1, "region": 1},
             "Gold": {"gen": 2, "region": 2},
             "Silver": {"gen": 2, "region": 2},
             "Crystal": {"gen": 2, "region": 2},
             "Ruby": {"gen": 3, "region": 3},
             "Sapphire": {"gen": 3, "region": 3},
             "Emerald": {"gen": 3, "region": 3},
             "FireRed": {"gen": 3, "region": 1},
             "LeafGreen": {"gen": 3, "region": 1},
             "Diamond": {"gen": 4, "region": 4},
             "Pearl": {"gen": 4, "region": 4},
             "Platinum": {"gen": 4, "region": 4.1},
             "HeartGold": {"gen": 4, "region": 2},
             "SoulSilver": {"gen": 4, "region": 2},
             "Black": {"gen": 5, "region": 5},
             "White": {"gen": 5, "region": 5},
             "Black 2": {"gen": 5, "region": 5.1},
             "White 2": {"gen": 5, "region": 5.1},
            }


class Pokedex:
    max_dex = MAX_DEXEN[-1]
    gen = 0
    region = 0
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
                # This pokemon does not have a second type.
                pokarray.append("---")
            self.dex.append({"number": int(pokarray[0]),
                             "name": re.sub('_', ' ', pokarray[1]),
                             "type1": pokarray[2],
                             "type2": pokarray[3]
                            })
        nat_data.close()
        self.new_dex()

    def status(self, pokenum):
        try:
            temp = self.user_dex[pokenum]
        except IndexError:
            print("%d is out of user_dex" % pokenum)
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
        # Make sure pokemon outside the current generation don't show up.
        if pokenum > self.max_dex:
            return False
        # But also make sure all the current pokemon do.
        elif pokenum >= len(self.user_dex):
            print("%d not initialized" % pokenum)
            return True
        temp = int(self.user_dex[pokenum])
        try:
            if not bitstring & temp:
                return False
        except ZeroDivisionError:
            return False

        if bitstring & 0b1000:
            from pydex import evolution
            if pokenum in evolution.get_instance().evolved:
                return False

        return True

    def new_dex(self):
        self.user_dex = [1] * (self.max_dex + 1)
        self.gen = 0
        self.region = 0
        self.unown_code = 0
        self.game = "Default"
        self.filename = ""

    def change_game(self, game):
        """Change the set game of the pokedex."""
        self.gen = GAME_DATA[game]['gen']
        self.region = GAME_DATA[game]['region']
        self.game = game

    def __repr__(self):
        """Dump the most useful vasriables from a loaded pokedex."""
        output = "Pokedex size:    %d\n" % self.max_dex
        output += "Game generation: %d\n" % self.gen
        output += "Game region:     %d\n" % self.region
        output += "Unown code:      %d\n" % self.unown_code
        output += "Game name:       %s\n" % self.game
        output += "Config filename: %s\n" % self.filename

        return output


def get_instance():
    global this
    if this == None:
        this = Pokedex()
    return this
