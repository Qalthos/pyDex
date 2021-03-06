# -*- coding: UTF-8 -*-
"""The main window of the pokedex.  This module handles all the GTK/Glade
specific functions

"""

import os

from gi.repository import Gtk, GdkPixbuf

from pydex import evolution, io, pokedex, regional_dex, utils


GAMES = [
    "Red", "Blue", "Yellow", "Gold", "Silver", "Crystal",
    "Ruby", "Sapphire", "Emerald", "FireRed", "LeafGreen",
    "Diamond", "Pearl", "Platinum", "HeartGold", "SoulSilver",
    "Black", "White", "Black 2", "White 2",
    "X", "Y", "Omega Ruby", "Alpha Sapphire", "Sun", "Moon",
]


class MainWindow:

    changed = False

    def __init__(self):
        self.builder = None
        self.pokedex = pokedex.get_instance()
        self.evolutions = evolution.get_instance()
        self.models = {
            "national": Gtk.ListStore(GdkPixbuf.Pixbuf, int, int, str, str, str, str),
            "Kdex": Gtk.ListStore(GdkPixbuf.Pixbuf, int, int, str, str, str, str),
            "Jdex": Gtk.ListStore(GdkPixbuf.Pixbuf, int, int, str, str, str, str),
            "Hdex": Gtk.ListStore(GdkPixbuf.Pixbuf, int, int, str, str, str, str),
            "Sdex": Gtk.ListStore(GdkPixbuf.Pixbuf, int, int, str, str, str, str),
            "Udex": Gtk.ListStore(GdkPixbuf.Pixbuf, int, int, str, str, str, str),
            "CeKdex": Gtk.ListStore(GdkPixbuf.Pixbuf, int, int, str, str, str, str),
            "CoKdex": Gtk.ListStore(GdkPixbuf.Pixbuf, int, int, str, str, str, str),
            "MoKdex": Gtk.ListStore(GdkPixbuf.Pixbuf, int, int, str, str, str, str),
            "Adex": Gtk.ListStore(GdkPixbuf.Pixbuf, int, int, str, str, str, str),
            "evolution": Gtk.ListStore(GdkPixbuf.Pixbuf, str, str, GdkPixbuf.Pixbuf, str),
            "prevolution": Gtk.ListStore(GdkPixbuf.Pixbuf, str, str, GdkPixbuf.Pixbuf, str)
        }
        self.models["evolution"].set_sort_func(2, sort)

        # Read settings and open last open file.
        self.config = io.read_config()
        # If we can find the file, load it.
        if "filename" in self.config:
            filename = self.config["filename"]
            if os.path.exists(filename):
                self.pokedex.filename = filename

        self.filter = int(self.config.get("filter", 0b111))
        self.filtermodels = dict()
        for region in regional_dex.IDS:
            rname = region['name']
            self.filtermodels[rname] = self.models[rname].filter_new()
            self.filtermodels[rname].set_visible_func(self.valid_wrapper)
            self.models[rname].set_sort_column_id(1, Gtk.SortType.ASCENDING)

    def main(self, parent):
        #Set the Glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file("pyDex.glade")

        for power, toggle in enumerate(['missing', 'seen', 'caught']):
            self.builder.get_object(toggle).set_active(self.filter & (2 ** power))

        if not parent:
            parent = self.builder.get_object("main_window")

        if "filename" in self.config:
            parent.set_title(self.config["filename"])
        parent.add(self.builder.get_object("main_pane"))

        # Build the listing of pokemon for each region (incl. national).
        for region in regional_dex.IDS:
            list_store = self.builder.get_object("%s_pokemon" % region['name'])
            list_store.set_model(self.filtermodels[region['name']])
            build_pokemon_columns(list_store, not (region['name'] == 'national'))

        list_store = self.builder.get_object("evolvable_pokemon")
        list_store.set_model(self.models["evolution"])
        list_store.append_column(make_column("icon", "image", 0))
        list_store.append_column(make_column("name", "text", 1))
        list_store.append_column(make_column("method", "text", 2))
        list_store.append_column(make_column("icon", "image", 3))
        list_store.append_column(make_column("name", "text", 4))

        list_store = self.builder.get_object("breedable_pokemon")
        list_store.set_model(self.models["prevolution"])
        list_store.append_column(make_column("icon", "image", 0))
        list_store.append_column(make_column("name", "text", 1))
        list_store.append_column(make_column("method", "text", 2))
        list_store.append_column(make_column("icon", "image", 3))
        list_store.append_column(make_column("name", "text", 4))

        # Populate the game dropdown
        game_name = self.builder.get_object("game_name")
        for game in GAMES:
            game_name.append_text(game)
        cell = Gtk.CellRendererText()
        game_name.pack_start(cell, True)
        game_name.set_entry_text_column(0)
        game_name.set_active(0)

        # Create our dictionary of actions and connect it
        # Do this late to keep setup from activating them
        dic = {"on_toggle": self.toggle,
               "new_file": self.new_file,
               "gtk_dialog_show": self.show_dialog,
               "show_about": self.show_about,
               "hide_about": self.hide_about,
               "gtk_info_show": self.show_info,
               "on_dialog_clicked": self.hide_dialog,
               "on_info_clicked": self.hide_info,
               "on_evo_clicked": self.hide_evo,
               "on_tab_flip": self.refresh_status,
               "on_game_change": self.game_change,
               "on_chk_toggled": self.unown_toggle,
               "quit": self.save_before_quit,
               "really_quit": self.quit
        }
        self.builder.connect_signals(dic)

        # Set the filter for filenames to .cfg
        self.builder.get_object("config_filter").add_pattern("*.cfg")

        # If the config contains a filename, try to load it.
        if self.pokedex.filename != "":
            self.open_file(self.pokedex.filename)
        # Otherwise, just fill the models (open_file calls this already)
        else:
            self.add_pokemon()

    def add_pokemon(self):
        """Clear out the stored pokemon and reload the list."""
        for model in self.models.values():
            model.clear()

        for pokemon in self.pokedex.dex:
            pokenum = int(pokemon["number"])
            pokarray = [GdkPixbuf.Pixbuf.new_from_file(
                                  utils.load_image(pokenum)),
                            pokenum, pokenum, pokemon["name"],
                            pokemon["type1"], pokemon["type2"],
                            self.pokedex.status(pokenum)]
            self.models["national"].append(pokarray)

            for i, region_dict in enumerate(regional_dex.IDS):
                if i == 0:
                    continue
                region = region_dict['pokemon']
                if self.pokedex.region in region_dict.get('versions', {}):
                    length = region_dict['versions'][self.pokedex.region]
                    region = region[:length]
                if pokenum in region:
                    pokarray[1] = region.index(pokenum)
                    self.models[region_dict['name']].append(pokarray)

        for evotype, evolist in self.evolutions.evo.items():
            for pokepair in evolist:
                pokeold = pokepair["old"]["number"]
                pokenew = pokepair["new"]["number"]
                if self.pokedex.valid(pokeold, 0b100) and self.pokedex.valid(pokenew, 0b011):
                    pokarray = [
                      GdkPixbuf.Pixbuf.new_from_file(utils.load_image(pokeold)),
                      pokepair["old"]["name"],
                      pokepair["method"],
                      GdkPixbuf.Pixbuf.new_from_file(utils.load_image(pokenew)),
                      pokepair["new"]["name"]
                    ]
                    self.models[evotype].append(pokarray)

        notebook = self.builder.get_object("dex_type")
        self.refresh_status(notebook, None, notebook.get_current_page())

    # Reaction Methods
    def new_file(self, *ignored):
        self.pokedex.new_dex()
        self.builder.get_object("main_window").set_title("New file")
        self.builder.get_object("game_name").set_active(0)
        self.add_pokemon()

    def toggle(self, button):
        """Changes the filter depending on which button was pressed."""
        filters = ['Missing', 'Seen', 'Caught', 'Show Evolved Pokemon',
                   'Show Unobtainable Pokemon',]
        if button.get_label() in filters:
            self.filter ^= 2 ** filters.index(button.get_label())
            self.config["filter"] = self.filter
            # Update the filters.
            for model in self.filtermodels.values():
                model.refilter()

    def show_dialog(self, menu_item):
        item_name = Gtk.Buildable.get_name(menu_item)
        if item_name == "save_menu_item" and not self.pokedex.filename == "":
            io.write_dex(self.pokedex)
            self.changed = False
            return
        button = self.builder.get_object("continue")
        chooser = self.builder.get_object("file_chooser")
        chooser.set_current_folder(io.config_dir)

        if item_name == "open_menu_item":
            button.set_label("Open")
            chooser.set_action(Gtk.FileChooserAction.OPEN)
        else:
            button.set_label("Save")
            chooser.set_action(Gtk.FileChooserAction.SAVE)
            chooser.set_current_name("%s.cfg" % self.pokedex.game)

        chooser.show()

    def hide_dialog(self, button):
        chooser = self.builder.get_object("file_chooser")
        self.config["filename"] = chooser.get_filename()
        if Gtk.Buildable.get_name(button) == "continue":
            if button.get_label() == "Save":
                self.pokedex.filename = chooser.get_filename()
                io.write_dex(self.pokedex)
            elif button.get_label() == "Open":
                self.open_file(chooser.get_filename())
            self.changed = False
            self.builder.get_object("main_window").set_title(chooser.get_filename())
        chooser.hide()

    def show_info(self, tv, *ignored):
        pokenum = tv.get_model().get_value(tv.get_selection().get_selected()[1], 2)
        pokemon = self.pokedex.dex[pokenum - 1]

        self.builder.get_object("number").set_label(str(pokemon["number"]))
        self.builder.get_object("image").set_from_file(utils.load_image(pokemon["number"], True))
        self.builder.get_object("info_type1").set_label(pokemon["type1"])
        if not pokemon["type2"] == "---":
            self.builder.get_object("info_type2").set_label(pokemon["type2"])
        else:
            self.builder.get_object("info_type2").set_label("")

        status = self.pokedex.user_dex[pokemon["number"]]
        # Prefill the status radio group
        self.builder.get_object("radio_missing").set_active(status & 1)
        self.builder.get_object("radio_seen").set_active(status & 2)
        self.builder.get_object("radio_caught").set_active(status & 4)

        self.builder.get_object("info_box").show()

    def hide_info(self, button):
        number = int(self.builder.get_object("number").get_label())
        if Gtk.Buildable.get_name(button) == "info_okay":
            last_value = self.pokedex.user_dex[number]
            for radio in self.builder.get_object("radio_caught").get_group():
                if radio.get_active():
                    label = Gtk.Buildable.get_name(radio)
                    if label == "radio_caught":
                        self.pokedex.user_dex[number] = 4
                    elif label == "radio_seen":
                        self.pokedex.user_dex[number] = 2
                    elif label == "radio_missing":
                        self.pokedex.user_dex[number] = 1
            if not last_value == self.pokedex.user_dex[number]:
                self.add_pokemon()
                self.changed = True
        self.builder.get_object("info_box").hide()

    def show_evo(self, tv, *ignored):
        pokenum = tv.get_model().get_value(tv.get_selection().get_selected()[1], 2)
        pokemon = self.pokedex.dex[pokenum - 1]

        self.builder.get_object("number").set_label(str(pokemon["number"]))
        self.builder.get_object("image").set_from_file(utils.load_image(pokemon["number"], True))
        self.builder.get_object("info_type1").set_label(pokemon["type1"])
        if not pokemon["type2"] == "---":
            self.builder.get_object("info_type2").set_label(pokemon["type2"])
        else:
            self.builder.get_object("info_type2").set_label("")

        self.builder.get_object("evolution_dialog").show()

    def hide_evo(self, button):
        self.builder.get_object("evolution_dialog").hide()

    def show_about(self, *ignored):
        response = self.builder.get_object("about").run()
        if response == Gtk.ResponseType.DELETE_EVENT or response == Gtk.ResponseType.CANCEL:
            self.builder.get_object("about").hide()

    def hide_about(self, *ignored):
        self.builder.get_object("about").hide()

    def refresh_status(self, notebook, ignored, new_page_num):
        status = self.builder.get_object("statusbar")
        caught = 0
        seen = 0
        dex = []
        if new_page_num < len(regional_dex.IDS):
            if new_page_num == 0: # National
                dex = self.pokedex.user_dex
            else:
                region = regional_dex.IDS[new_page_num]['pokemon']
                for entry in self.pokedex.dex:
                    if entry["number"] in region:
                        if entry["number"] >= len(self.pokedex.user_dex):
                            continue
                        dex.append(self.pokedex.user_dex[entry["number"]])

            for pokestat in dex:
                if pokestat == 4:
                    caught += 1
                elif pokestat == 2:
                    seen += 1

            seen += caught
            pct_seen = seen * 100.0 / len(dex)
            pct_caught = caught * 100.0 / len(dex)
            status.push(0, "Seen: %d (%d%%)  Caught: %d (%d%%)" %
                            (seen, pct_seen, caught, pct_caught))
        else:
            status.push(0, "%d pokemon waiting to evolve" %
                                    len(self.models["evolution"]))

    def game_change(self, combobox):
        old_game = self.pokedex.game

        self.pokedex.change_game(combobox.get_active_text())
        self.refresh_pages()

        # Don't save if the game hasn't changed
        if old_game != self.pokedex.game:
            self.changed = True

    def unown_toggle(self, checkbox):
        index = int(Gtk.Buildable.get_name(checkbox)[4:]) - 1
        old_code = self.pokedex.unown_code

        if checkbox.get_active():
            self.pokedex.unown_code |= 2**index
        else:
            self.pokedex.unown_code &= ~(2**index)

        # Don't save if the code hasn't changed.
        if old_code != self.pokedex.unown_code:
            self.changed = True

    def save_before_quit(self, *ignored):
        if self.changed:
            self.builder.get_object("quit_dialog").show()
            return True
        else:
            io.write_config(self.config)
            Gtk.main_quit()

    def quit(self, button):
        if button.get_label() == "Save":
            io.write_dex(self.pokedex)
        self.builder.get_object("quit_dialog").hide()
        if button.get_label() == "Cancel":
            return
        io.write_config(self.config)
        Gtk.main_quit()

    # Convenience Methods
    def open_file(self, filename):
        io.read_dex(filename)
        if self.pokedex.game in GAMES:
            self.builder.get_object("game_name") \
                .set_active(GAMES.index(self.pokedex.game))
            self.builder.get_object("dex_type") \
                .set_current_page(self.pokedex.region)

        for i in range(28):
            test = (self.pokedex.unown_code & 2**i)
            self.builder.get_object("chk_%d" % (i+1)).set_active(test > 0)
        self.pokedex.filename = filename
        self.refresh_pages()
        self.add_pokemon()

    def refresh_pages(self):
        """Determine visible pages based on current game."""
        effective_gen = self.pokedex.gen
        if effective_gen >= 6:
            # account for the three Kalos pokedexen
            effective_gen += 2
        for i in range(len(regional_dex.IDS)):
            page = self.builder.get_object("dex_type").get_nth_page(i)
            page.set_visible(i <= effective_gen)

        # Hide functions not present in Gen I
        for tab in ['national', 'unown', 'baby']:
            self.builder.get_object("%s_tab" % tab).set_visible(self.pokedex.gen != 1)

    def valid_wrapper(self, model, model_iter, data):
        """A wrapper around pokedex's valid() function for use with
        TreeModelFilter."""
        # This is different in the national vs the regional dexes, but it's
        # always 5 from the end.
        pokenum = model.get_value(model_iter, model.get_n_columns() - 5)
        return self.pokedex.valid(pokenum, self.filter)


def build_pokemon_columns(list_store, regional=True):
    list_store.append_column(make_column("icon", "image", 0))
    list_store.append_column(make_column("#", "text", 1))
    if regional:
        list_store.append_column(make_column("N#", "text", 2))
    list_store.append_column(make_column("name", "text", 3))
    list_store.append_column(make_column("type 1", "text", 4))
    list_store.append_column(make_column("type 2", "text", 5))
    list_store.append_column(make_column("status", "text", 6))
    list_store.set_search_equal_func(search, None)


def search(model, column, key, iterator, data=None):
    """Checks each row to see if it matches the search pattern."""
    row_data = model.get(iterator, 1, 2, 3, 4, 5)
    for datum in row_data:
        if not str(datum).lower().find(key.lower()) == -1:
            return False
    return True


def sort(model, iter1, iter2, data=None):
    """Orders evolutions.  Trades first, then special trades, then levels, then
    special levels, then the rest alphabetically.

    """

    method1 = model.get(iter1, 2)[0]
    method2 = model.get(iter2, 2)[0]
    if method2 is None:
        # I think this runs when we're past the edge
        return -1
    elif method1[:2] == "Tr" and method2[:2] == "Tr":
        return normal_sort(method1, method2)
    elif method1[:2] == "Tr":
        return -1
    elif method2[:2] == "Tr":
        return 1
    elif method1[:3] == "Lev" and method2[:3] == "Lev":
        return normal_sort(method1, method2)
    elif method1[:3] == "Lev":
        return -1
    elif method2[:3] == "Lev":
        return 1
    return normal_sort(method1, method2)


def normal_sort(method1, method2):
    """Normal, everyday, alphanumeric sort."""

    if method1 < method2:
        return -1
    elif method2 < method1:
        return 1
    else:
        return 0


def make_column(title, column_type, column_id):
    column = Gtk.TreeViewColumn(title, Gtk.CellRendererText(), text=column_id)
    if column_type == "image":
        column = Gtk.TreeViewColumn(title, Gtk.CellRendererPixbuf(), pixbuf=column_id)
    column.set_resizable(True)
    column.set_sort_column_id(column_id)

    return column
