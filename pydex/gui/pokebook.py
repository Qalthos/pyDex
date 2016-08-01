import wx

from pydex import regional_dex
from pydex.gui.pokepage import PokedexPage

class PokedexNotebook(wx.Notebook):
    def __init__(self, *args, **kwargs):
        super(PokedexNotebook, self).__init__(*args, **kwargs)
        for dex_info in regional_dex.IDS:
            page = PokedexPage(self, data=dex_info)
            self.AddPage(page, dex_info['region'])

    def load(self, filename=None):
        if not getattr(self, 'config', None):
            self.config = io.read_config()
            self.filter = int(self.config.get('filter', 0b111))
        if not filename:
            filename = self.config['filename']
        io.read_dex(filename)
        self.refresh_all()

    def refresh_all(self):
        for i in range(self.GetPageCount()):
            page = self.GetPage(i)
            page.populate_list(self.filter)
