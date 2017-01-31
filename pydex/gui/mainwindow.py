# -*- coding: UTF-8 -*-
import os

import wx

from pydex import io, pokedex
from pydex.gui.pokebook import PokedexNotebook


# Custom IDs for reference
ID_MISS = wx.NewId()
ID_SEEN = wx.NewId()
ID_HAVE = wx.NewId()


class MainWindow(wx.Frame):
    def __init__(self):
        super(MainWindow, self).__init__(None, title='pyDex.py', size=(700, 600))

        self.init_ui()
        self.Show()

    def init_ui(self):
        # Toolbar
        self.toolbar = self.CreateToolBar(wx.TB_NOICONS)

        self.new = wx.Button(self.toolbar, wx.ID_NEW, 'New...')
        self.new.Bind(wx.EVT_BUTTON, self.new_file)
        self.toolbar.AddControl(self.new)

        self.open = wx.Button(self.toolbar, wx.ID_OPEN, 'Open')
        self.open.Bind(wx.EVT_BUTTON, self.open_file)
        self.toolbar.AddControl(self.open)

        self.save = wx.Button(self.toolbar, wx.ID_SAVE, 'Save')
        self.save.Bind(wx.EVT_BUTTON, self.save_file)
        self.toolbar.AddControl(self.save)

        self.toolbar.AddStretchableSpace()
        self.toolbar.AddCheckTool(ID_MISS, 'Missing', wx.NullBitmap)
        self.toolbar.AddCheckTool(ID_SEEN, 'Seen', wx.NullBitmap)
        self.toolbar.AddCheckTool(ID_HAVE, 'Caught', wx.NullBitmap)
        self.toolbar.Realize()
        self.toolbar.Bind(wx.EVT_TOOL, self.filter_pages)

        # Contents
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.notebook = PokedexNotebook(panel, style=wx.NB_LEFT)
        vbox.Add(self.notebook, wx.EXPAND | wx.ALL)

        panel.SetSizer(vbox)

    def new_file(self, event):
        dex = pokedex.get_instance()
        dex.new_dex()
        self.notebook.refresh_all()

    def open_file(self, event):
        wildcard = 'Config files|*.cfg'
        location = os.path.expanduser('~/.pyDex')
        dialog = wx.FileDialog(self, defaultDir=location, wildcard=wildcard, style=wx.FD_OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            self.notebook.load(path)

    def save_file(self, event):
        io.write_dex()

    def save_as_file(self, event):
        wildcard = 'Config files|*.cfg'
        location = os.path.expanduser('~/.pyDex')
        dialog = wx.FileDialog(self, defaultDir=location, wildcard=wildcard, style=wx.FD_SAVE)

        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            userdex = pokedex.get_instance()
            userdex.filename = path
            io.write_dex()

    def filter_pages(self, event):
        for i, id_ in enumerate((ID_MISS, ID_SEEN, ID_HAVE)):
            if event.Id == id_:
                break

        self.notebook.filter ^= 2**i
        self.notebook.refresh_all()
