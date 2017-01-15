# -*- coding: UTF-8 -*-
import wx

from pydex.gui.pokebook import PokedexNotebook


class MainWindow(wx.Frame):
    def __init__(self):
        super(MainWindow, self).__init__(None, title='pyDex.py', size=(700, 600))

        self.init_ui()
        self.Show()

    def init_ui(self):
        # Toolbar
        self.toolbar = self.CreateToolBar(wx.TB_NOICONS)

        self.new = wx.Button(self.toolbar, wx.ID_NEW, 'New...')
        self.toolbar.AddControl(self.new)

        self.open = wx.Button(self.toolbar, wx.ID_OPEN, 'Open')
        self.toolbar.AddControl(self.open)

        self.save = wx.Button(self.toolbar, wx.ID_SAVE, 'Save')
        self.toolbar.AddControl(self.save)

        self.toolbar.AddStretchableSpace()
        self.toolbar.AddCheckTool(0, 'Missing', wx.NullBitmap)
        self.toolbar.AddCheckTool(1, 'Seen', wx.NullBitmap)
        self.toolbar.AddCheckTool(2, 'Caught', wx.NullBitmap)
        self.toolbar.Realize()

        # Contents
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.notebook = PokedexNotebook(panel, style=wx.NB_LEFT)
        vbox.Add(self.notebook, wx.EXPAND | wx.ALL)

        panel.SetSizer(vbox)
