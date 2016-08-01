#!/usr/bin/env python
import wx


from pydex import wx_gui


if __name__ == "__main__":
    app = wx.App()
    wx_gui.MainWindow(None, title='pyDex.py')
    app.MainLoop()
