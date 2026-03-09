import tkinter as _tk

from async_tkinter_loop import\
    async_handler as _async_handler
from tkinter import\
    ttk as _ttk
from typing import\
    Any as _Any

class FrameTileset(_ttk.Frame):
    """
    Represents a main window
    """

    #region init

    def __init__(self,\
            master:None|_tk.Misc = None,\
            **kwargs:_Any):
        """
        Initializer for FrameTileset
        """
        _PROMPTWIDTH = 15
        super().__init__(master = master, **kwargs)
        #region Tileset
        self.__widget_t = _ttk.LabelFrame(\
            master = self,\
            padding = (5, 5, 5, 5),\
            text = "Tileset")
        self.__widget_t.pack(fill = 'x')
        # Path
        self.__widget_tp = _ttk.Frame(\
            master = self.__widget_t)
        self.__widget_tp.pack(fill = 'x')
        self.__widget_tp_label = _ttk.Label(\
            master = self.__widget_tp,\
            text = "/path/to/the/tileset.bmp")
        self.__widget_tp_label.pack(anchor = 'w', side = 'left', fill = 'x', expand = True)
        self.__widget_tp_button = _ttk.Button(\
            master = self.__widget_tp,\
            command = self.__r_widget_tp_button,\
            text = "Open")
        self.__widget_tp_button.pack(anchor = 'w', side = 'left')
        #endregion
        #region Palette
        self.__widget_p = _ttk.LabelFrame(\
            master = self,\
            padding = (5, 5, 5, 5),\
            text = "Palette")
        self.__widget_p.pack(fill = 'x')
        # Custom
        self.__widget_p_custom_var = _tk.BooleanVar(value = False)
        self.__widget_p_custom = _ttk.Checkbutton(\
            master = self.__widget_p,\
            variable = self.__widget_p_custom_var,\
            command = self.__r_widget_p_custom,\
            text = "Use custom palette")
        self.__widget_p_custom.pack(fill = 'x')
        # Path
        self.__widget_pp = _ttk.Frame(\
            master = self.__widget_p)
        self.__widget_pp.pack(fill = 'x')
        self.__widget_pp_label = _ttk.Label(\
            master = self.__widget_pp,\
            text = "/path/to/the/palette.bmp")
        self.__widget_pp_label.pack(anchor = 'w', side = 'left', fill = 'x', expand = True)
        self.__widget_pp_button = _ttk.Button(\
            master = self.__widget_pp,\
            command = self.__r_widget_pp_button,\
            text = "Open")
        self.__widget_pp_button.pack(anchor = 'w', side = 'left')
        #endregion
    
    #endregion

    #region receivers

    def __r_widget_tp_button(self):
        print("Open Tileset")

    def __r_widget_p_custom(self):
        print(self.__widget_p_custom_var.get())

    def __r_widget_pp_button(self):
        print("Open Palette")

    #endregion