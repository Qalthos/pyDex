#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""The main window of the pokedex.  This module handles all the GTK/Glade
specific functions

"""

import os

import gtk
import gtk.glade

import config
import evolution
import io
import pokedex
import regional_dex


class MainWindow:

    image_dir = "../images/"
    changed = False

    def __init__(self):
        self.pokedex = pokedex.get_instance()
        self.evolutions = evolution.get_instance()
        self.national_model = gtk.ListStore(gtk.gdk.Pixbuf, int, int, str,
                                                            str, str, str)
        self.kanto_model = gtk.ListStore(gtk.gdk.Pixbuf, int, int, str,
                                                         str, str, str)
        self.johto_model = gtk.ListStore(gtk.gdk.Pixbuf, int, int, str,
                                                         str, str, str)
        self.hoenn_model = gtk.ListStore(gtk.gdk.Pixbuf, int, int, str,
                                                         str, str, str)
        self.sinnoh_model = gtk.ListStore(gtk.gdk.Pixbuf, int, int, str,
                                                          str, str, str)
        self.isshu_model = gtk.ListStore(gtk.gdk.Pixbuf, int, int, str,
                                                         str, str, str)
        self.evolution_model = gtk.ListStore(gtk.gdk.Pixbuf, str, str,
                                             gtk.gdk.Pixbuf, str)
        self.evolution_model.set_sort_func(2, sort)

        self.filter = 0b111

        self.builder = None

    def main(self):
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
                    "quit": self.save_before_quit,
             "really_quit": self.quit}
        self.builder.connect_signals(dic)

        filename = config.get_instance().get_last_file()
        if not filename == "":
            self.builder.get_object("main_window").set_title(filename)

        # Build the listing of pokemon (national).
        list_store = self.builder.get_object("national_pokemon")
        list_store.set_model(self.national_model)
        build_pokemon_columns(list_store, False)

        # Build the listing of pokemon (Kanto).
        list_store = self.builder.get_object("kanto_pokemon")
        list_store.set_model(self.kanto_model)
        build_pokemon_columns(list_store)

        # Build the listing of pokemon (Johto).
        list_store = self.builder.get_object("johto_pokemon")
        list_store.set_model(self.johto_model)
        build_pokemon_columns(list_store)

        # Build the listing of pokemon (Hoenn).
        list_store = self.builder.get_object("hoenn_pokemon")
        list_store.set_model(self.hoenn_model)
        build_pokemon_columns(list_store)

        # Build the listing of pokemon (Sinnoh).
        list_store = self.builder.get_object("sinnoh_pokemon")
        list_store.set_model(self.sinnoh_model)
        build_pokemon_columns(list_store)

        # Build the listing of pokemon (Isshu).
        #list_store = self.builder.get_object("isshu_pokemon")
        #list_store.set_model(self.isshu_model)
        #build_pokemon_columns(list_store)

        list_store = self.builder.get_object("evolvable_pokemon")
        list_store.set_model(self.evolution_model)
        list_store.append_column(make_column("icon", "image", 0))
        list_store.append_column(make_column("name", "text", 1))
        list_store.append_column(make_column("method", "text", 2))
        list_store.append_column(make_column("icon", "image", 3))
        list_store.append_column(make_column("name", "text", 4))

        # Populate the game dropdown
        game_name = self.builder.get_object("game_name")
        game_store = gtk.ListStore(str)
        game_store.append(["Diamond"])
        game_store.append(["Pearl"])
        game_store.append(["Platinum"])
        game_store.append(["HeartGold"])
        game_store.append(["SoulSilver"])
        game_store.append(["Black"])
        game_store.append(["White"])
        game_name.set_model(game_store)
        cell = gtk.CellRendererText()
        game_name.pack_start(cell, True)
        game_name.add_attribute(cell, 'text', 0)

        self.builder.get_object("config_filter").add_pattern("*.cfg")

        self.add_pokemon()

    def add_pokemon(self):
        self.clear_models()

        for pokemon in self.pokedex.dex:
            pokenum = pokemon.get_number()
            if not self.pokedex.valid(pokenum, self.filter):
                continue
            pokarray = [gtk.gdk.pixbuf_new_from_file(
                                  self.load_image(pokenum)),
                            pokenum, pokenum, pokemon.get_name(),
                            pokemon.get_type1(), pokemon.get_type2(),
                            self.pokedex.status(pokenum)]
            self.national_model.append(pokarray)
            if pokenum in regional_dex.kanto_ids:
                pokarray[1] = regional_dex.kanto_ids.index(pokenum)
                self.kanto_model.append(pokarray)
            if pokenum in regional_dex.johto_ids:
                pokarray[1] = regional_dex.johto_ids.index(pokenum)
                self.johto_model.append(pokarray)
            if pokenum in regional_dex.hoenn_ids:
                pokarray[1] = regional_dex.hoenn_ids.index(pokenum)
                self.hoenn_model.append(pokarray)
            if pokenum in regional_dex.sinnoh_ids:
                pokarray[1] = regional_dex.sinnoh_ids.index(pokenum)
                self.sinnoh_model.append(pokarray)
            #if pokenum in regional_dex.isshu_ids:
            #    pokarray[1] = regional_dex.isshu_ids.index(pokenum)
            #    self.isshu_model.append(pokarray)

        for pokepair in self.evolutions.evo:
            pokeold = pokepair.old.get_number()
            pokenew = pokepair.new.get_number()
            if self.pokedex.valid(pokeold, 0b100) and self.pokedex.valid(pokenew, 0b011):
                pokarray = [gtk.gdk.pixbuf_new_from_file(
                                      self.load_image(pokeold)),
                            pokepair.old.get_name(), pokepair.method,
                            gtk.gdk.pixbuf_new_from_file(
                                      self.load_image(pokenew)),
                            pokepair.new.get_name()]
                self.evolution_model.append(pokarray)

        notebook = self.builder.get_object("dex_type")
        self.refresh_status(notebook, None, notebook.get_current_page())

    # Reaction Methods
    def new_file(self, *ignored):
        self.pokedex.new_dex()
        self.builder.get_object("main_window").set_title("New file")
        self.add_pokemon()

    def toggle(self, button):
        if button.get_label() == "Missing":
            self.filter ^= 0b001
        elif button.get_label() == "Seen":
            self.filter ^= 0b010
        elif button.get_label() == "Caught":
            self.filter ^= 0b100
        self.add_pokemon()

    def show_dialog(self, menu_item):
        item_name = get_name(menu_item)
        if item_name == "save_menu_item" and not self.pokedex.get_filename() == "":
            io.write_dex(self.pokedex)
            self.changed = False
            return
        button = self.builder.get_object("continue")
        chooser = self.builder.get_object("file_chooser")
        if item_name == "open_menu_item":
            button.set_label("Open")
            chooser.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
        else:
            button.set_label("Save")
            chooser.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)

        chooser.set_current_folder(io.config_dir)
        chooser.show()

    def hide_dialog(self, button):
        chooser = self.builder.get_object("file_chooser")
        config.get_instance().set_last_file(chooser.get_filename())
        if get_name(button) == "continue":
            if button.get_label() == "Save":
                self.pokedex.set_filename(chooser.get_filename())
                io.write_dex(self.pokedex)
            elif button.get_label() == "Open":
                self.pokedex.user_dex = io.read_dex(chooser.get_filename())
                self.pokedex.set_filename(chooser.get_filename())
                self.add_pokemon()
            self.changed = False
            self.builder.get_object("main_window").set_title(chooser.get_filename())
        chooser.hide()

    def show_info(self, tv, *ignored):
        pokenum = tv.get_model().get_value(
            tv.get_selection().get_selected()[1], 2)
        pokemon = self.pokedex.dex[pokenum - 1]

        self.builder.get_object("number").set_label(str(pokemon.get_number()))
        self.builder.get_object("image").set_from_file(self.load_image(pokemon.get_number(), True))
        self.builder.get_object("info_type1").set_label(pokemon.get_type1())
        if not pokemon.get_type2() == "---":
            self.builder.get_object("info_type2").set_label(pokemon.get_type2())
        else:
            self.builder.get_object("info_type2").set_label("")

        status = self.pokedex.user_dex[pokemon.get_number()]
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
            else:
                print self.pokedex.user_dex[number]
        self.builder.get_object("info_box").hide()

    def show_evo(self, tv, *ignored):
        pokenum = tv.get_model().get_value(
            tv.get_selection().get_selected()[1], 2)
        print pokenum
        pokemon = self.pokedex.dex[pokenum - 1]

        self.builder.get_object("number").set_label(str(pokemon.get_number()))
        self.builder.get_object("image").set_from_file(self.load_image(pokemon.get_number(), True))
        self.builder.get_object("info_type1").set_label(pokemon.get_type1())
        if not pokemon.get_type2() == "---":
            self.builder.get_object("info_type2").set_label(pokemon.get_type2())
        else:
            self.builder.get_object("info_type2").set_label("")

        self.builder.get_object("evolution_dialog").show()

    def hide_evo(self, button):
        self.builder.get_object("evolution_dialog").hide()

    def show_about(self, *ignored):
        self.builder.get_object("about").show()

    def hide_about(self, *ignored):
        self.builder.get_object("about").hide()

    def refresh_status(self, notebook, ignored, new_page_num):
        status = self.builder.get_object("statusbar")
        caught = 0
        seen = 0
        dex = []
        if new_page_num == 0: # National
            dex = self.pokedex.user_dex
        else:
            region = None
            if  new_page_num == 1:
                region = regional_dex.kanto_ids
            elif  new_page_num == 2:
                region = regional_dex.johto_ids
            elif  new_page_num == 3:
                region = regional_dex.hoenn_ids
            elif  new_page_num == 4:
                region = regional_dex.sinnoh_ids
            #elif  new_page_num == 5:
            #    region = regional_dex.isshu_ids
            else:
                status.push(0, str(len(self.evolution_model)) +
                                 " pokemon waiting to evolve")
                return
            for line in self.pokedex.dex:
                if line.number in region:
                    dex.append(self.pokedex.user_dex[line.number])
        for pokestat in dex:
            if pokestat == 4:
                caught += 1
            elif pokestat == 2:
                seen += 1

        seen += caught
        pct_seen = int(seen * 100.0 / len(dex))
        pct_caught = int(caught * 100.0 / len(dex))
        status.push(0, "Seen: " + str(seen) + " (" + str(pct_seen) + "%) " +
                   " Caught: " + str(caught) + " (" + str(pct_caught) + "%)")

    def save_before_quit(self, *ignored):
        if self.changed:
            self.builder.get_object("quit_dialog").show()
            return True
        else:
            io.write_config()
            gtk.main_quit()

    def quit(self, button):
        if button.get_label() == "Save":
            io.write_dex(self.pokedex)
        self.builder.get_object("quit_dialog").hide()
        if button.get_label() == "Cancel":
            return
        io.write_config()
        gtk.main_quit()

    # Convenience Methods
    def clear_models(self):
        self.national_model.clear()
        self.kanto_model.clear()
        self.johto_model.clear()
        self.hoenn_model.clear()
        self.sinnoh_model.clear()
        self.isshu_model.clear()
        self.evolution_model.clear()

    def load_image(self, image_number, portrait=False):
        if portrait and os.path.exists(
                "%sportraits/%d.png" % (self.image_dir, image_number)):
            return "%sportraits/%d.png" % (self.image_dir, image_number)
        elif os.path.exists(
                    "%sicons/%d.png" % (self.image_dir, image_number)):
            return "%sicons/%d.png" % (self.image_dir, image_number)
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
