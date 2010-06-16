#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# PyDex: An interactive pokédex reader.

import gtk

import os
import sys

import main_window
import config
import io

if __name__ == "__main__":
    # Fix for relative paths
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

    # Change file based on version of pyGTK
    if gtk.gtk_version[1] < 17:
        mw = main_window.MainWindow()
    else: # Grrrr, broken get_name()
        mw = main_window.MainWindowHack()

    # Read settings and open last open file.
    io.read_settings()
    filename = config.get_instance().get_last_file()
    if os.path.exists(filename):
        mw.user_settings = io.read_config(filename)

    mw.main()
    gtk.main()
