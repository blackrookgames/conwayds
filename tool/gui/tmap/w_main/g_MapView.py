import tkinter as _tk

from async_tkinter_loop import\
    async_handler as _async_handler
from tkinter import\
    ttk as _ttk
from typing import\
    Any as _Any

class MapView(_ttk.Frame):
    """
    Represents a map view
    """

    #region init

    def __init__(self,\
            master:None|_tk.Misc,\
            **kwargs:_Any):
        """
        Initializer for MapView
        """
        super().__init__(\
            master = master,\
            style = 'My.TFrame',\
            **kwargs)
        self.pack_propagate(False)
        # Style
        self.__style = _ttk.Style()
        self.__style.configure('My.TFrame', background='#D0D0D0')
        # Canvas
        self.__widget_fc_canvas = _tk.Canvas(\
            master = self,\
            width = 512,\
            height = 512,\
            bg = '#D0D0D0',\
            highlightthickness = 0)
        self.__widget_fc_canvas.pack(anchor = 'nw')
    
    #endregion