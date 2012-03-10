#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""PyDex is an interactive pokédex reader written in Python and Glade"""

from gi.repository import Gtk

import os
import sys

from pydex import main_window

if __name__ == "__main__":
    # Fix for relative paths
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

    mw = main_window.MainWindow()

    mw.main(None)
    Gtk.main()
