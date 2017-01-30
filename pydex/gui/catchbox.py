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
        infobox.Add(wx.StaticText(self, label=self.generate_evolution_text(pokemon.number)))
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
        pokemon_species = list(utils.table_data_gen('pokemon_species'))

        prevo_id = pokemon_species[pokenum - 1]['evolves_from_species_id']
        if not prevo_id:
            return ''

        evorray = [
            row for row in utils.table_data_gen('pokemon_evolution')
            if row['evolved_species_id'] == str(pokenum)
        ][0]
        trigger_prose = list(utils.table_data_gen('evolution_trigger_prose'))[int(evorray['evolution_trigger_id']) - 1]

        gender_cond = 'a {} '.format(evorray['gender_id']) if evorray['gender_id'] else ''
        trigger = 'Evolves from {}{} after a {}'.format(gender_cond, prevo_id, trigger_prose['name'])
        conditions = []
        if evorray['minimum_level']:
            conditions.append('starting at level {}'.format(evorray['minimum_level']))
        if evorray['minimum_happiness']:
            conditions.append('with happiness >= {}'.format(evorray['minimum_happiness']))
        if evorray['held_item_id']:
            conditions.append('while holding {}'.format(evorray['held_item_id']))
        if evorray['known_move_id']:
            conditions.append('knowing {}'.format(evorray['known_move_id']))
        if evorray['location_id']:
            conditions.append('in {}'.format(evorray['location_id']))
        if evorray['trade_species_id']:
            conditions.append('trading for {}'.format(evorray['trade_species_id']))
        if evorray['trigger_item_id']:
            conditions.append('using {}'.format(evorray['trigger_item_id']))
        if evorray['party_species_id']:
            conditions.append('with {} in party '.format(evorray['party_species_id']))
        if evorray['turn_upside_down'] == '1':
            conditions.append('while holding the console upside down')
        if evorray['time_of_day']:
            conditions.append('during the {}'.format(evorray['time_of_day']))
        if evorray['needs_overworld_rain'] == '1':
            conditions.append('in the rain')
        if evorray['minimum_affection']:
            conditions.append('with affection >= {}'.format(evorray['minimum_affection']))
        if evorray['known_move_type_id']:
            conditions.append('while knowing a {}-type move'.format(evorray['known_move_type_id']))
        if evorray['minimum_beauty']:
            conditions.append('with beauty >= {}'.format(evorray['minimum_beauty']))

        return ' '.join([trigger] + conditions) + evorray['relative_physical_stats'] + evorray['party_type_id']
