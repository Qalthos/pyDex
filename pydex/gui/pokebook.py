import wx

from pydex.gui.pokepage import PokedexPage
from pydex import io
from pydex.utils import table_data_gen


class PokedexNotebook(wx.Notebook):
    def __init__(self, *args, **kwargs):
        super(PokedexNotebook, self).__init__(*args, **kwargs)
        self.config = None
        self.filter = 0b111

        pokedex_ids = [row['id'] for row in table_data_gen('pokedexes') if row['is_main_series'] == '1']
        pokedex_names = [
            (row['pokedex_id'], row['name']) for row in table_data_gen('pokedex_prose')
            if row['pokedex_id'] in pokedex_ids
        ]
        pokedex_map = list(table_data_gen('pokemon_dex_numbers'))

        for dex_id, dex_name in sorted(pokedex_names):
            regional_dex = sorted([
                (int(row['pokedex_number']), int(row['species_id'])) for row
                in pokedex_map if row['pokedex_id'] == dex_id
            ])
            page = PokedexPage(self, {'region': dex_name, 'pokemon': regional_dex})
            self.AddPage(page, dex_name)

    def load(self, filename=None):
        if not self.config:
            self.config = io.read_config()
            self.filter = int(self.config.get('filter', 0b111))

        if filename:
            self.config['filename'] = filename

        io.read_dex(self.config['filename'])
        self.refresh_all()

    def refresh_all(self):
        for i in range(self.GetPageCount()):
            page = self.GetPage(i)
            page.populate_list()
