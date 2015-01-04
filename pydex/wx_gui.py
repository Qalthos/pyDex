import wx


from pydex import io, pokedex, regional_dex, utils


class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.init_ui()
        self.notebook.load()
        self.Show()

    def init_ui(self):
        # Menu Setup
        menubar = wx.MenuBar()
        filem = wx.Menu()
        menubar.Append(filem, '&File')
        self.SetMenuBar(menubar)

        # Contents
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.notebook = PokedexNotebook(panel, style=wx.NB_LEFT)
        vbox.Add(self.notebook, wx.EXPAND | wx.ALL)

        panel.SetSizer(vbox)

        # Status Bar
        statusbar = wx.StatusBar(self)
        self.SetStatusBar(statusbar)


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


class PokedexPage(wx.ListView):
    def __init__(self, *args, **kwargs):
        data = kwargs.pop('data')
        for key in data:
            setattr(self, key, data[key])

        super(PokedexPage, self).__init__(
            #style=wx.LC_ICON,
            *args, **kwargs
        )

        columns = ['Icon', 'Regional #',  'National #', 'Name', 'Type 1', 'Type 2', 'Status']
        if self.region == 'National':
            columns.pop(1)
        for index, column in enumerate(columns):
            self.InsertColumn(index, column)

    def populate_list(self, filter):
        userdex = pokedex.get_instance()
        for index, pokenum in enumerate(self.pokemon):
            if not userdex.valid(pokenum, filter):
                continue
            pokarray = [
                wx.Bitmap(utils.load_image(pokenum), wx.BITMAP_TYPE_ANY),
                index,
                pokenum,
                userdex.dex[pokenum-1]['name'].decode('utf8'),
                userdex.dex[pokenum-1]['type1'],
                userdex.dex[pokenum-1]['type2'],
                userdex.status(pokenum),
            ]
            if self.region == 'National':
                pokarray.pop(1)
            self.Append(pokarray)
