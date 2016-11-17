import wx
from pydex import pokedex, utils


class PokedexPage(wx.ListView):
    def __init__(self, parent, dex_info):
        super(PokedexPage, self).__init__(parent, style=wx.LC_REPORT)

        self.region = dex_info['region']
        self.pokemon = dex_info['pokemon']

        columns = ['Icon', 'Regional #', 'National #', 'Name', 'Type 1', 'Type 2', 'Status']
        if self.region == 'National':
            columns.pop(1)
        for column in columns:
            self.InsertColumn(-1, column)

        self.populate_list()

    def populate_list(self, filter=0b111):
        userdex = pokedex.get_instance()
        for index, pokenum in enumerate(self.pokemon):
            if not userdex.valid(pokenum, filter):
                continue
            pokarray = [
                wx.Bitmap(utils.load_image(pokenum), wx.BITMAP_TYPE_ANY),
                index,
                pokenum,
                userdex.dex[pokenum - 1]['name'],
                userdex.dex[pokenum - 1]['type1'],
                userdex.dex[pokenum - 1]['type2'],
                userdex.status(pokenum),
            ]
            if self.region == 'National':
                pokarray.pop(1)
            self.Append(pokarray)
