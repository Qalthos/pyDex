#!/usr/bin/env python
import wx


from pydex.gui.mainwindow import MainWindow


if __name__ == "__main__":
    app = wx.App()
    MainWindow()
    app.MainLoop()
