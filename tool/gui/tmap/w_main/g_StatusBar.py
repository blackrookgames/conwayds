import tkinter as _tk

from async_tkinter_loop import\
    async_handler as _async_handler
from tkinter import\
    ttk as _ttk
from typing import\
    Any as _Any

class StatusBar(_ttk.Frame):
    """
    Represents a status bar
    """

    #region init

    def __init__(self,\
            master:None|_tk.Misc,\
            **kwargs:_Any):
        """
        Initializer for StatusBar
        """
        super().__init__(\
            master = master,\
            height = 10,\
            **kwargs)
        # Position
        self.__widget_sp = _ttk.Label(self, text = "X, Y", width = 10)
        self.__widget_sp.grid(column = 0, row = 0)
        # Size
        self.__widget_ss = _ttk.Label(self, text = "W, H", width = 10)
        self.__widget_ss.grid(column = 1, row = 0)
    
    #endregion