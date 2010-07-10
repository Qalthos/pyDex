#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# The national pokédex.

import pokemon

this = None
MAX_DEX = 493


class Pokedex:

    def __init__(self):
        self.dex = []
        nat_data = open("ndex.dat")
        for line in nat_data:
            pokarray = line.split()
            if len(pokarray) == 3:
                pokarray.append("---")
            self.dex.append(pokemon.Pokemon(pokarray))
        nat_data.close()


def get_instance():
    global this
    if this == None:
        this = Pokedex()
    return this
