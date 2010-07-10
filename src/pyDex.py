#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""PyDex is an interactive pokédex reader written in Python and Glade"""

import gtk

import os
import sys

import main_window
import config
import io

if __name__ == "__main__":
    # Fix for relative paths
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

    mw = main_window.MainWindow()

    # Read settings and open last open file.
    io.read_config()
    filename = config.get_instance().get_last_file()
    # If we can find the file, load it.
    if os.path.exists(filename):
        mw.user_settings = io.read_dex(filename)

    mw.main()
    gtk.main()
