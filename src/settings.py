#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# User settings file.

import pokedex

class Settings:
    user_dex = []
    game = ""
    filename = ""
    
    def __init__(self):
        self.user_dex = [1] * (pokedex.MAX_DEX + 1)
    
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
        temp = int(self.user_dex[pokenum])
        if (int(bitstring) % (temp * 2)) / temp == 1:
            return True
        else:
            return False

    def get_filename(self):
        return self.filename
    def set_filename(self, filename):
        self.filename = filename
