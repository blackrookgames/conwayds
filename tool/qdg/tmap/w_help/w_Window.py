__all__ = ['Window']

import tkinter as _tk
import tkinter.ttk as _ttk

class Window(_tk.Toplevel):
    """
    Represents a help window
    """

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for Window """
        def _items(_start:int, *_items:tuple[str, str]):
            for _i in range(len(_items)):
                _item = _items[_i]
                # Name
                _l_name = _ttk.Label(\
                    master = self, justify = 'left', padding = (5, 0, 5, 0),\
                    text = _item[0])
                _l_name.grid(column = 0, row = _start + _i, sticky='w')
                # Desc
                _l_desc = _ttk.Label(\
                    master = self, justify = 'left', padding = (5, 0, 5, 0),\
                    text = _item[1])
                _l_desc.grid(column = 1, row = _start + _i, sticky='w')
            return _start + len(_items)
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("Help")
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        self.geometry('250x250')
        self.grid_columnconfigure(1, weight = 1)
        # General
        start = _items(0,\
            ( "F1", "Show help"),\
            ( "F2", "Switch Edit Mode"),\
            ( "F3", "Change Palette"),\
            ( "F4", "Change Orientation"),\
            ( "F5", "Set Size"),\
            ( "F6", "Select Tile"),\
            ( "Ctrl+S", "Save"),)
        # Draw mode
        _label_draw = _ttk.Label(\
            master = self, justify = 'left', padding = (5, 5, 5, 0),\
            text = "Draw Mode:")
        _label_draw.grid(column = 0, row = start, sticky='w')
        start = _items(start + 1,\
            ( "Left Mouse", "Draw Tile"),\
            ( "Right Mouse", "Pick Tile"),\
            ( "Scroll", "Change Tile"),)

    #endregion