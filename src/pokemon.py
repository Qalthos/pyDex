#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# A basic pokemon class.

class Pokemon:
    
    def __init__(self, name, national_number=None, type1=None, type2=None):
        if national_number == None:
            self.number = int(name[0])
            self.name = name[1]
            self.type1 = name[2]
            self.type2 = name[3]
        else:
            self.name = name
            self.number = int(national_number)
            self.type1 = type1
            self.type2 = type2
        
    def get_number(self):
        return self.number
    def get_name(self):
        return self.name
    def get_type1(self):
        return self.type1
    def get_type2(self):
        return self.type2

    def __str__(self):
        return self.name
