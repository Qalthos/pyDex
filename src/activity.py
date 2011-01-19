import main_window
    
from sugar.activity import activity
    
class pyDexActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.connect('destroy', self._cleanup_cb)
        
        self.gamename = 'pyDex'
        self.set_title("pyDex")
        
        # connect to the in/out events
        self.connect('focus_in_event', self._focus_in)
        self.connect('focus_out_event', self._focus_out)

        mw = main_window.MainWindow()
        mw.main(self)
        
    def _cleanup_cb(self, data=None):
        return
    
    def _focus_in(self, event, data=None):
        return
    
    def _focus_out(self, event, data=None):
        return
