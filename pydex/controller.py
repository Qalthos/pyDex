import os

from pydex import io
from pydex.gui.mainwindow import MainWindow

class PokeController(object):
    def __init__(self):
        self.config = io.read_config()
        self.data_filename = None

        # If we can find the file, load it.
        if 'filename' in self.config:
            filename = self.config['filename']
            if os.path.exists(filename):
                self.data_filename = filename

        self.view = MainWindow()
        self.view.Show(True)
