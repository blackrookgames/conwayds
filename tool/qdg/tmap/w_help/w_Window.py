import tkinter as _tk
import tkinter.ttk as _ttk

class Window(_tk.Toplevel):
    """
    Represents a help window
    """

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for Window """
        # Initialize
        super().__init__(*args, **kwargs)
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        self.geometry('200x200')
        self.grid_columnconfigure(1, weight = 1)
        # Items
        items = [\
            ( "F1", "Show help" ),\
            ( "Ctrl+S", "Save" ),]
        for _i in range(len(items)):
            _item = items[_i]
            # Name
            _l_name = _ttk.Label(\
                master = self,\
                justify = 'left',\
                padding = (5, 0, 5, 0),\
                text = _item[0])
            _l_name.grid(column = 0, row = _i, sticky='w')
            # Desc
            _l_desc = _ttk.Label(\
                master = self,\
                justify = 'left',\
                padding = (5, 0, 5, 0),\
                text = _item[1])
            _l_desc.grid(column = 1, row = _i, sticky='w')

    #endregion