# -*- coding: UTF-8 -*-
"""The main window of the pokedex.  This module handles all the GTK/Glade
specific functions

"""

import os

import gtk
import gtk.glade

import evolution
import io
import pokedex
import regional_dex


class MainWindow:

    image_dir = "images/"
    changed = False

    dexes = ("national", "Kdex", "Jdex", "Hdex", "Sdex", "Udex")
    games = ["Red", "Blue", "Yellow", "Gold", "Silver", "Crystal",
             "Ruby", "Sapphire", "Emerald", "FireRed", "LeafGreen",
             "Diamond", "Pearl", "Platinum", "HeartGold", "SoulSilver",
             "Black", "White"]

    def __init__(self):
        self.pokedex = pokedex.get_instance()
        self.evolutions = evolution.get_instance()
        self.models = {
          "national": gtk.ListStore(gtk.gdk.Pixbuf, int, int, str, str, str, str),
          "Kdex": gtk.ListStore(gtk.gdk.Pixbuf, int, int, str, str, str, str),
          "Jdex": gtk.ListStore(gtk.gdk.Pixbuf, int, int, str, str, str, str),
          "Hdex": gtk.ListStore(gtk.gdk.Pixbuf, int, int, str, str, str, str),
          "Sdex": gtk.ListStore(gtk.gdk.Pixbuf, int, int, str, str, str, str),
          "Udex": gtk.ListStore(gtk.gdk.Pixbuf, int, int, str, str, str, str),
          "evolution": gtk.ListStore(gtk.gdk.Pixbuf, str, str, gtk.gdk.Pixbuf, str),
          "prevolution": gtk.ListStore(gtk.gdk.Pixbuf, str, str, gtk.gdk.Pixbuf, str)
        }
        self.models["evolution"].set_sort_func(2, sort)

        self.filter = 0b111

        self.builder = None

        # Read settings and open last open file.
        self.config = io.read_config()
        # If we can find the file, load it.
        if "filename" in self.config:
            filename = self.config["filename"]
            if os.path.exists(filename):
                self.pokedex.filename = filename

    def main(self, parent):
        #Set the Glade file
        self.builder = gtk.Builder()
        self.builder.add_from_file("pyDex.glade")

        #Create our dictionay of actions and connect it
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
             "really_quit": self.quit}
        self.builder.connect_signals(dic)

        if not parent:
            parent = self.builder.get_object("main_window")
    
        if "filename" in self.config:
            parent.set_title(self.config["filename"])
        parent.add(self.builder.get_object("main_pane"))

        # Build the listing of pokemon (national).
        list_store = self.builder.get_object("national_pokemon")
        list_store.set_model(self.models["national"])
        build_pokemon_columns(list_store, False)

        # Build the listing of pokemon for each region.
        for region in regional_dex.IDS:
            list_store = self.builder.get_object("%s_pokemon" % region)
            list_store.set_model(self.models[region])
            build_pokemon_columns(list_store)

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
        game_store = gtk.ListStore(str)
        for game in self.games:
            game_store.append([game])
        game_name.set_model(game_store)
        cell = gtk.CellRendererText()
        game_name.pack_start(cell, True)
        game_name.add_attribute(cell, 'text', 0)

        # Set the filter for filenames to .cfg
        self.builder.get_object("config_filter").add_pattern("*.cfg")

        # If the config contains a filename, try to load it.
        if self.pokedex.filename != "":
            self.open_file(self.pokedex.filename)
        # Otherwise, just fill the models (open_file calls this already)
        else:
            self.add_pokemon()

    def add_pokemon(self):
        self.clear_models()

        for pokemon in self.pokedex.dex:
            pokenum = int(pokemon["number"])
            # This hides pokemon which do not match the current filter.
            if not self.pokedex.valid(pokenum, self.filter):
                continue
            pokarray = [gtk.gdk.pixbuf_new_from_file(
                                  self.load_image(pokenum)),
                            pokenum, pokenum, pokemon["name"],
                            pokemon["type1"], pokemon["type2"],
                            self.pokedex.status(pokenum)]
            self.models["national"].append(pokarray)
            for region_name, region in regional_dex.IDS.items():
                if pokenum in region:
                    pokarray[1] = region.index(pokenum)
                    self.models[region_name].append(pokarray)

        for evotype, evolution in self.evolutions.evo.items():
            for pokepair in evolution:
                pokeold = pokepair["old"]["number"]
                pokenew = pokepair["new"]["number"]
                if self.pokedex.valid(pokeold, 0b100) and self.pokedex.valid(pokenew, 0b011):
                    pokarray = [
                      gtk.gdk.pixbuf_new_from_file(self.load_image(pokeold)),
                      pokepair["old"]["name"],
                      pokepair["method"],
                      gtk.gdk.pixbuf_new_from_file(self.load_image(pokenew)),
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
        if button.get_label() == "Missing":
            self.filter ^= 0b001
        elif button.get_label() == "Seen":
            self.filter ^= 0b010
        elif button.get_label() == "Caught":
            self.filter ^= 0b100
        # Update the lists.
        self.add_pokemon()

    def show_dialog(self, menu_item):
        item_name = get_name(menu_item)
        if item_name == "save_menu_item" and not self.pokedex.filename == "":
            io.write_dex(self.pokedex)
            self.changed = False
            return
        button = self.builder.get_object("continue")
        chooser = self.builder.get_object("file_chooser")
        chooser.set_current_folder(io.config_dir)
        
        if item_name == "open_menu_item":
            button.set_label("Open")
            chooser.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
        else:
            button.set_label("Save")
            chooser.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
            chooser.set_current_name("%s.cfg" % self.pokedex.game)

        chooser.show()

    def hide_dialog(self, button):
        chooser = self.builder.get_object("file_chooser")
        self.config["filename"] = chooser.get_filename()
        if get_name(button) == "continue":
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
        self.builder.get_object("image").set_from_file(self.load_image(pokemon["number"], True))
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
        if get_name(button) == "info_okay":
            last_value = self.pokedex.user_dex[number]
            for radio in self.builder.get_object("radio_caught").get_group():
                if radio.get_active():
                    label = get_name(radio)
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
        self.builder.get_object("image").set_from_file(self.load_image(pokemon["number"], True))
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
        if response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_CANCEL:
            self.builder.get_object("about").hide()

    def hide_about(self, *ignored):
        self.builder.get_object("about").hide()

    def refresh_status(self, notebook, ignored, new_page_num):
        status = self.builder.get_object("statusbar")
        caught = 0
        seen = 0
        dex = []
        if new_page_num < len(self.dexes):
            if new_page_num == 0: # National
                dex = self.pokedex.user_dex
            else:
                region = regional_dex.IDS[self.dexes[new_page_num]]
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
        pokedex.get_instance().game = combobox.get_active_text()
        self.refresh_pages()

    def unown_toggle(self, checkbox):
        index = int(get_name(checkbox)[4:]) - 1
        if checkbox.get_active():
            self.pokedex.unown_code |= 2**index
        else:
            self.pokedex.unown_code &= ~(2**index)
        
        print self.pokedex.unown_code
        self.changed = True

    def save_before_quit(self, *ignored):
        if self.changed:
            self.builder.get_object("quit_dialog").show()
            return True
        else:
            io.write_config(self.config)
            gtk.main_quit()

    def quit(self, button):
        if button.get_label() == "Save":
            io.write_dex(self.pokedex)
        self.builder.get_object("quit_dialog").hide()
        if button.get_label() == "Cancel":
            return
        io.write_config(self.config)
        gtk.main_quit()

    # Convenience Methods
    def open_file(self, filename):
        self.pokedex.user_dex = io.read_dex(filename)
        if self.pokedex.game in self.games:
            self.builder.get_object("game_name").set_active(self.games.index(self.pokedex.game))
            self.builder.get_object("dex_type").set_current_page(self.pokedex.region)

        for i in range(28):
            test = (self.pokedex.unown_code & 2**i)
            self.builder.get_object("chk_%d" % (i+1)).set_active(test > 0)
        self.pokedex.filename = filename
        self.refresh_pages()
        self.add_pokemon()

    def refresh_pages(self):
        for i, region in enumerate(self.dexes):
            page = self.builder.get_object("dex_type").get_nth_page(i)
            if i > self.pokedex.gen:
                page.set_visible(False)
            else:
                page.set_visible(True)

    def clear_models(self):
        for model in self.models.values():
            model.clear()

    def load_image(self, image_number, portrait=False):
        if portrait and os.path.exists(
                "%sportraits/%s.png" % (self.image_dir, image_number)):
            return "%sportraits/%s.png" % (self.image_dir, image_number)
        elif os.path.exists(
                    "%sicons/%s.png" % (self.image_dir, image_number)):
            return "%sicons/%s.png" % (self.image_dir, image_number)
        elif os.path.exists("%sicons/0.png" % self.image_dir):
            return "%sicons/0.png" % self.image_dir
        return "%sblank.png" % self.image_dir


def get_name(buildable):
    """Returns the gtk.Buildable.get_name() for the specified widget, rather
    than the gtk.Widget.get_name() which gets called by default in newer GTK
    versions.

    """

    if gtk.gtk_version[1] < 17:
        return buildable.get_name()
    else: # Grrrr, broken get_name()
        return gtk.Buildable.get_name(buildable)


def build_pokemon_columns(list_store, regional=True):
    list_store.append_column(make_column("icon", "image", 0))
    list_store.append_column(make_column("#", "text", 1))
    if regional:
        list_store.append_column(make_column("N#", "text", 2))
    list_store.append_column(make_column("name", "text", 3))
    list_store.append_column(make_column("type 1", "text", 4))
    list_store.append_column(make_column("type 2", "text", 5))
    list_store.append_column(make_column("status", "text", 6))
    list_store.set_search_equal_func(search)


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
    if method2 == None:
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
    column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=column_id)
    if column_type == "image":
        column = gtk.TreeViewColumn(title, gtk.CellRendererPixbuf(), pixbuf=column_id)
    column.set_resizable(True)
    column.set_sort_column_id(column_id)

    return column
