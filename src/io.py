#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Provides a method of reading and writing to or from pyDex files."""

import os

settings_dir = os.path.expanduser("~/.pyDex/")
import config
import pokedex


def write_dex(userdex):
    """Writes the current pokedex to a file."""
    print "Writing to %s" % userdex.get_filename()
    dex_file = open(userdex.get_filename(), "w")
    for pokemon in userdex.user_dex:
        dex_file.write("%s\n" % pokemon)
    dex_file.close()


def read_dex(filename):
    """Loads the pokedex stored in filename into pyDex."""
    print "Reading from", filename
    userdex = settings.Settings()
    userdex.set_filename(filename)
    dex_file = open(filename)
        for num, line in enumerate(dex_file):
        userdex.user_dex[num] = int(line.strip())
    dex_file.close()

    return userdex


def write_settings():
    """Writes the current pyDex configuration to a standard location."""
    if not os.path.exists(settings_dir):
        os.makedirs(settings_dir)
    config_file = open(settings_dir + "config", "w")
    config_file.write(config.get_instance().get_last_file())
    config_file.close()


def read_settings():
    """Reads saved pyDex configuration from a standard location."""
    if not os.path.exists(settings_dir):
        os.makedirs(settings_dir)
    if not os.path.exists(settings_dir + "config"):
        return
    config_file = open(settings_dir + "config")
    config.get_instance().set_last_file(config_file.next())
    config_file.close()
