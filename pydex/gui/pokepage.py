import wx
from pydex import pokedex, utils


class PokedexPage(wx.ListView):
    pokedex = pokedex.get_instance()
    pokemon_il = wx.ImageList(40, 40)
    pokicon_list = []
    for pokenum in range(pokedex.max_dex + 1):
        pokicon_list.append(pokemon_il.Add(wx.Bitmap(utils.load_image(pokenum), wx.BITMAP_TYPE_ANY)))

    def __init__(self, parent, dex_info):
        super(PokedexPage, self).__init__(parent, style=wx.LC_REPORT)

        self.region = dex_info['region']
        self.pokemon = dex_info['pokemon']

        self.SetImageList(self.pokemon_il, wx.IMAGE_LIST_SMALL)

        columns = ['Name', 'Regional #', 'National #', 'Type 1', 'Type 2', 'Status']
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
            row_index = self.InsertItem(index, userdex.dex[pokenum - 1]['name'], self.pokicon_list[index])
            pokarray = [
                str(index),
                str(pokenum),
                userdex.dex[pokenum - 1]['type1'],
                userdex.dex[pokenum - 1]['type2'],
                userdex.status(pokenum),
            ]
            if self.region == 'National':
                pokarray.pop(0)

            for i, data in enumerate(pokarray):
                self.SetItem(row_index, i+1, data)
