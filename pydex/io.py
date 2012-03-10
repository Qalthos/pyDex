# -*- coding: UTF-8 -*-
"""Provides a method of reading and writing to or from pyDex files."""

import os

from pydex import pokedex

config_dir = os.path.expanduser("~/.pyDex/")


def write_dex(userdex):
    """Writes the current pokedex to a file."""
    print("Writing to %s" % userdex.filename)
    dex_file = open(userdex.filename, "w")
    dex_file.write("%s\n" % userdex.game)
    # user_dex index 0 is junk to keep index to dexnum translation straight
    # Skip it.
    for pokemon in userdex.user_dex[1:]:
        dex_file.write("%s\n" % pokemon)
    dex_file.write("\n%s\n" % userdex.unown_code)
    dex_file.close()


def read_dex(filename):
    """Loads the pokedex stored in filename into pyDex."""
    print("Reading from", filename)
    userdex = [0]
    dex_file = open(filename)
    dex = pokedex.get_instance()

    try:
        # Read the game version
        game = dex_file.next().strip()
        if game in pokedex.GAME_DATA:
            dex.max_dex = pokedex.MAX_DEXEN[pokedex.GAME_DATA[game]["gen"]]
            dex.game = game
            dex.gen = pokedex.GAME_DATA[game]["gen"]
            dex.region = pokedex.GAME_DATA[game]["region"]
        for line in dex_file:
            line = line.strip()
            if len(line) == 0:
                break
            if len(userdex) > dex.max_dex:
                continue
            userdex.append(int(line))
        # Read the Unown code
        dex.unown_code = int(dex_file.next())
    except StopIteration:
        print("Error reading file! Only %d read." % len(userdex))

    # Premature stopping or older files may result in short arrays.
    while len(userdex) <= dex.max_dex:
        userdex.append(1)

    dex_file.close()

    return userdex


def write_config(config):
    """Writes the current pyDex configuration to a standard location."""
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    config_file = open(config_dir + "config", "w")
    for key, value in config.items():
    	if key == "filename":
	        config_file.write("%s" % value)
    config_file.close()


def read_config():
    """Reads saved pyDex configuration from a standard location."""
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    config = {}
    if not os.path.exists(config_dir + "config"):
        return config
    config_file = open(config_dir + "config")
    for line in config_file:
        line = line.split()
        try:
            config[line[0]] = line[1]
        except IndexError:
            config["filename"] = line[0]
        break
    config_file.close()

    return config
