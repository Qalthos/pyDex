import wx

from pydex import pokedex, utils
from pydex.pokemon import Pokemon
from pydex.gui.catchbox import CatchBox


class PokedexPage(wx.ListView):
    pokedex = pokedex.get_instance()
    pokemon_il = wx.ImageList(96, 96)
    pokicon_list = []
    for pokenum in range(pokedex.max_dex + 1):
        pokicon_list.append(pokemon_il.Add(wx.Bitmap(utils.load_image(pokenum), wx.BITMAP_TYPE_ANY)))

    def __init__(self, parent, dex_info):
        super(PokedexPage, self).__init__(parent, style=wx.LC_REPORT)
        self.parent = parent

        self.region = dex_info['region']
        self.pokemon = dex_info['pokemon']

        self.SetImageList(self.pokemon_il, wx.IMAGE_LIST_SMALL)

        columns = ['Name', 'Regional #', 'National #', 'Type 1', 'Type 2', 'Status']
        if self.region == 'National':
            columns.pop(1)
        for column in columns:
            self.InsertColumn(-1, column)

        self.populate_list()
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)

        self.bind_events()

    def populate_list(self):
        self.DeleteAllItems()
        userdex = pokedex.get_instance()
        for index, pokenum in enumerate(self.pokemon):
            if not userdex.valid(pokenum, self.parent.filter):
                continue
            row_index = self.InsertItem(index, userdex.dex[pokenum - 1]['name'], self.pokicon_list[pokenum])
            self.SetItemData(row_index, pokenum)
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

    def bind_events(self):
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.catch_box)

    # Event handlers
    def catch_box(self, event):
        pokemon = Pokemon(name=event.Label, number=event.Data)
        box = CatchBox(self, pokemon)

        userdex = pokedex.get_instance()
        if box.ShowModal() == wx.ID_OK:
            for i, radio in enumerate((box.missing, box.seen, box.caught)):
                if radio.GetValue():
                    userdex.mark_pokemon(event.Data, 2**i)

            self.populate_list()
