import wx


class PokedexPage(wx.ListView):
    def __init__(self, *args, **kwargs):
        data = kwargs.pop('data')
        for key in data:
            setattr(self, key, data[key])

        super(PokedexPage, self).__init__(
            # style=wx.LC_ICON,
            *args, **kwargs
        )

        columns = ['Icon', 'Regional #', 'National #', 'Name', 'Type 1', 'Type 2', 'Status']
        if self.region == 'National':
            columns.pop(1)
        for column in columns:
            self.InsertColumn(-1, column)

    def populate_list(self, filter):
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
