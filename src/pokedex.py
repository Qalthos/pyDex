#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# The national pokédex.

import pokemon

this = None
MAX_DEX = 502

class Pokedex:
    def __init__(self):
        self.dex = []
        file = open("ndex.dat")
        for line in file:
            pokarray = line.split()
            if len(pokarray) == 3:
                pokarray.append("---")
            self.dex.append(pokemon.Pokemon(pokarray))
        file.close()
        
        
def get_instance():
    global this
    if this == None: this = Pokedex()
    return this
