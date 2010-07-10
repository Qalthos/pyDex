#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Provides a method of reading and writing to or from pyDex files."""

import os

import config
import pokedex

config_dir = os.path.expanduser("~/.pyDex/")


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
    userdex = [0]
    dex_file = open(filename)

    try:
        for line in dex_file:
            line = line.strip()
            if len(line) == 0:
                break
            if len(userdex) > pokedex.MAX_DEX:
                continue
            userdex.append(int(line))
    except StopIteration:
        print "Error reading file! Only %d read." % len(userdex)

    # Premature stopping or older files may result in short arrays.
    while len(userdex) <= pokedex.MAX_DEX:
        userdex.append(1)

    dex_file.close()

    return userdex


def write_config(config):
    """Writes the current pyDex configuration to a standard location."""
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    config_file = open(config_dir + "config", "w")
    config_file.write(config.get_instance().get_last_file())
    config_file.close()


def read_config():
    """Reads saved pyDex configuration from a standard location."""
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(config_dir + "config"):
        return
    config_file = open(config_dir + "config")
    config.get_instance().set_last_file(config_file.next())
    config_file.close()
