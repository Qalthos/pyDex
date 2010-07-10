#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Provides a method of reading and writing to or from pyDex files."""

import os

import pokedex

config_dir = os.path.expanduser("~/.pyDex2/")


def write_dex(userdex):
    """Writes the current pokedex to a file."""
    print "Writing to %s" % userdex.get_filename()
    dex_file = open(userdex.get_filename(), "w")
    dex_file.write("%s\n" % userdex.get_game())
    # user_dex index 0 is junk to keep index to dexnum translation straight
    # Skip it.
    for pokemon in userdex.user_dex[1:]:
        dex_file.write("%s\n" % pokemon)
    dex_file.write("\n%s\n" % userdex.unown_code)
    dex_file.close()


def read_dex(filename):
    """Loads the pokedex stored in filename into pyDex."""
    print "Reading from", filename
    userdex = [0]
    dex_file = open(filename)

    try:
        # Read the game version
        game = dex_file.next()
        for line in dex_file:
            line = line.strip()
            if len(line) == 0:
                break
            if len(userdex) > pokedex.MAX_DEX:
                continue
            userdex.append(int(line))
        # Read the Unown code
        unown = dex_file.next()
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
    for key, value in config.items():
        config_file.write("%s %s" % (key, value))
    config_file.close()


def read_config():
    """Reads saved pyDex configuration from a standard location."""
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(config_dir + "config"):
        return
    config_file = open(config_dir + "config")
    config = {}
    for line in config_file:
        config["filename"] = line.strip()
        break
    config_file.close()

    return config
