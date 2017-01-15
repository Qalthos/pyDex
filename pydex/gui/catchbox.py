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
        buttonbox.Add(wx.RadioButton(self, label='missing', style=wx.RB_GROUP))
        buttonbox.Add(wx.RadioButton(self, label='seen'))
        buttonbox.Add(wx.RadioButton(self, label='caught'))
        hbox.Add(buttonbox, flag=wx.EXPAND|wx.ALL)

        buttons = self.CreateButtonSizer(flags=wx.OK|wx.CANCEL)
        topbox.Add(buttons)
