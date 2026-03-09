import tkinter as _tk

from async_tkinter_loop import\
    async_handler as _async_handler
from tkinter import\
    ttk as _ttk

import gui.helper as _gui_helper
import src.helper as _helper

from .w_FrameSize import\
    FrameSize as _FrameSize
from .w_FrameTileset import\
    FrameTileset as _FrameTileset

class WinNew(_tk.Toplevel):
    """
    Represents a window for configuring a new tilemap
    """

    #region init

    def __init__(self, *args, **kwargs):
        """
        Initializer for WinNew
        """
        super().__init__(*args, **kwargs)
        # Window Properties
        self.title("New Tilemap")
        self.geometry('400x200')
        self.resizable(False, False)
        self.config(padx = 5, pady = 5)
        # Tileset
        self.__tileset = _FrameTileset(\
            master = self,\
            padding = (0, 0, 0, 5))
        self.__tileset.pack(fill = 'x')
        # Size
        self.__size = _FrameSize(\
            master = self,\
            showanchor = False,\
            padding = (0, 0, 0, 5))
        self.__size.pack(fill = 'x')
        # Buttons
        self.__widget_buttons = _gui_helper.ButtonRow(\
            self,\
            buttons = [\
                _helper.kwargs(\
                    command = self.__r_widget_buttons_ok,\
                    text = "OK"),\
                _helper.kwargs(\
                    command = self.__r_widget_buttons_cancel,\
                    text = "Cancel"),\
                ],\
            )
        self.__widget_buttons.pack(fill = 'x', anchor = 's', expand = True)
    
    #endregion

    #region receivers

    def __r_widget_buttons_ok(self):
        print("OK")

    def __r_widget_buttons_cancel(self):
        print("Cancel")

    #endregion