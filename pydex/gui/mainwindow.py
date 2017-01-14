# -*- coding: UTF-8 -*-
import wx

from pydex.gui.pokebook import PokedexNotebook


class MainWindow(wx.Frame):
    def __init__(self):
        super(MainWindow, self).__init__(None, title='pyDex.py', size=(700, 600))

        self.init_ui()
        self.Show()

    def init_ui(self):
        # Menu Setup
        menubar = wx.MenuBar()
        filem = wx.Menu()
        menubar.Append(filem, '&File')
        self.SetMenuBar(menubar)

        # Contents
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.notebook = PokedexNotebook(panel, style=wx.NB_LEFT)
        vbox.Add(self.notebook, wx.EXPAND | wx.ALL)

        panel.SetSizer(vbox)

        # Status Bar
        statusbar = wx.StatusBar(self)
        self.SetStatusBar(statusbar)
