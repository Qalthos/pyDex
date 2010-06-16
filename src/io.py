#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# I/O functions for PyDex

import config
import os
import settings

settings_dir = os.path.expanduser("~/.pyDex/")
    
def write_config(userdex):
    print "Writing to", userdex.get_filename()
    file = open(userdex.get_filename(), "w")
    for pokemon in userdex.user_dex:
        file.write(str(pokemon) + "\n")
    file.close()
        
def read_config(filename):
    print "Reading from", filename
    userdex = settings.Settings()
    userdex.set_filename(filename)
    file = open(filename)
    for num, line in enumerate(file):
        userdex.user_dex[num] = int(line.strip())
    file.close()
        
    return userdex
    
def write_settings():
    if not os.path.exists(settings_dir):
        os.makedirs(settings_dir)
    file = open(settings_dir + "config", "w")
    file.write(config.get_instance().get_last_file())
    file.close()
    
def read_settings():
    if not os.path.exists(settings_dir):
        os.makedirs(settings_dir)
    if not os.path.exists(settings_dir + "config"):
        return
    file = open(settings_dir + "config")
    config.get_instance().set_last_file(file.next())
    file.close()
