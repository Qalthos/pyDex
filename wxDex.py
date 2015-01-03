#!/usr/bin/env python
import wx

from pydex import pokedex, regional_dex, utils


class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

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

        notebook = PokedexNotebook(panel, style=wx.NB_LEFT)
        vbox.Add(notebook, wx.EXPAND | wx.ALL)

        panel.SetSizer(vbox)

        # Status Bar
        statusbar = wx.StatusBar(self)
        self.SetStatusBar(statusbar)


class PokedexNotebook(wx.Notebook):
    def __init__(self, *args, **kwargs):
        super(PokedexNotebook, self).__init__(*args, **kwargs)
        for dex_info in regional_dex.IDS:
            page = PokedexPage(self, data=dex_info)
            self.AddPage(page, dex_info['region'])


class PokedexPage(wx.ListView):
    def __init__(self, *args, **kwargs):
        data = kwargs.pop('data')
        for key in data:
            setattr(self, key, data[key])

        super(PokedexPage, self).__init__(
            style=wx.LC_ICON, *args, **kwargs
        )

        columns = ['Icon', 'Regional #',  'National #', 'Name', 'Type 1', 'Type 2', 'Status']
        if self.region == 'National':
            columns.pop(1)
        #for index, column in enumerate(columns):
        #    self.InsertColumn(index, column)

        self.populate_list()

    def populate_list(self):
        dex = pokedex.get_instance().dex
        for index, pokenum in enumerate(self.pokemon):
            if pokenum == 0:
                continue
            pokarray = [
                wx.Bitmap(utils.load_image(pokenum), wx.BITMAP_TYPE_ANY),
                index,
                pokenum,
                dex[pokenum-1]['name'].decode('utf8'),
                dex[pokenum-1]['type1'],
                dex[pokenum-1]['type2'],
                'unknown',
            ]
            if self.region == 'National':
                pokarray.pop(1)
            self.Append(pokarray)


if __name__ == "__main__":
    app = wx.App()
    MainWindow(None, title='pyDex.py')
    app.MainLoop()
