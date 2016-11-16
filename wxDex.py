#!/usr/bin/env python

import wx

from pydex.controller import PokeController


if __name__ == "__main__":
    app = wx.App()
    PokeController()
    app.MainLoop()
