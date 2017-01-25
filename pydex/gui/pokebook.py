import wx

from pydex.gui.pokepage import PokedexPage
from pydex import io
from pydex.utils import table_data_gen


class PokedexNotebook(wx.Notebook):
    def __init__(self, *args, **kwargs):
        super(PokedexNotebook, self).__init__(*args, **kwargs)
        regions = list(table_data_gen('region_names'))
        pokedexen = list(table_data_gen('pokedexes'))
        pokedex_map = list(table_data_gen('pokemon_dex_numbers'))
        for region in regions:
            pokedex = [dex for dex in pokedexen if dex['region_id'] ==
                       region['region_id']][-1]
            pokedex_list = [int(pokemon['species_id']) for pokemon in pokedex_map if pokemon['pokedex_id'] == pokedex['id']]
            page = PokedexPage(self, {'name': region['name'], 'region': region['name'], 'pokemon': pokedex_list})
            self.AddPage(page, region['name'])

    def load(self, filename=None):
        if not getattr(self, 'config', None):
            self.config = io.read_config()
            self.filter = int(self.config.get('filter', 0b111))

        if filename:
            self.config['filename'] = filename

        io.read_dex(self.config['filename'])
        self.refresh_all()

    def refresh_all(self):
        for i in range(self.GetPageCount()):
            page = self.GetPage(i)
            page.populate_list(self.filter)
