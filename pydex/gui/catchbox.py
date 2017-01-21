import wx

from pydex import utils


class CatchBox(wx.Dialog):
    def __init__(self, parent, pokemon):
        super(CatchBox, self).__init__(parent, name=pokemon.name, size=(550, 200))

        self.init_ui(pokemon)

    def init_ui(self, pokemon):
        topbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(topbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        topbox.Add(hbox, flag=wx.EXPAND|wx.ALL)

        image = wx.Bitmap(utils.load_image(pokemon.number), wx.BITMAP_TYPE_ANY)
        staticbmp = wx.StaticBitmap(self, label=image)
        hbox.Add(staticbmp, flag=wx.EXPAND|wx.ALL)

        infobox = wx.BoxSizer(wx.VERTICAL)
        infobox.Add(wx.StaticText(self, label=pokemon.name))
        #FIXME: hardcoded version_id
        pokesummary = [row for row in utils.table_data_gen('pokemon_species_flavor_text') if row['version_id'] == '26']
        infobox.Add(wx.StaticText(self, label=pokesummary[pokemon.number]['flavor_text']))
        hbox.Add(infobox, flag=wx.EXPAND|wx.ALL)

        buttonbox = wx.BoxSizer(wx.VERTICAL)
        self.missing = wx.RadioButton(self, label='missing', style=wx.RB_GROUP)
        self.seen = wx.RadioButton(self, label='seen')
        self.caught = wx.RadioButton(self, label='caught')
        buttonbox.Add(self.missing)
        buttonbox.Add(self.seen)
        buttonbox.Add(self.caught)
        hbox.Add(buttonbox, flag=wx.EXPAND|wx.LEFT)

        buttons = self.CreateButtonSizer(flags=wx.OK|wx.CANCEL)
        topbox.Add(buttons)

    def generate_evolution_text(self, pokenum):
        evolist = [row for row in utils.table_data_gen('pokemon_evolution')]
        trigger_list = list(utils.table_data_gen('evolution_trigger_prose'))
        evorray = evolist[pokenum - 1]
        trigger_prose = trigger_list[int(evorray['evolution_trigger_id']) - 1]

        print(trigger_prose['name'] +
              ' after ' + evorray['minimum_level'] +
              ' with happiness >= ' + evorray['minimum_happiness'] +
              ' while holding ' + evorray['held_item_id'] +
              evorray['relative_physical_stats'] +
              evorray['turn_upside_down'] +
              ' trading with ' + evorray['trade_species_id'] +
              evorray['gender_id'] +
              evorray['time_of_day'] +
              ' with ' + evorray['party_species_id'] + ' in party ' +
              evorray['party_type_id'] +
              evorray['needs_overworld_rain'] +
              ' knowing ' + evorray['known_move_id'] +
              ' using ' + evorray['trigger_item_id'] +
              ' with affection >= ' + evorray['minimum_affection'] +
              evorray['known_move_type_id'] +
              ' in ' + evorray['location_id'] +
              ' with beauty >= ' + evorray['minimum_beauty']
        )
