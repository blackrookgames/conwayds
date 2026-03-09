import tkinter as _tk

from async_tkinter_loop import\
    async_handler as _async_handler
from tkinter import\
    ttk as _ttk
from typing import\
    Any as _Any

import gui.helper as _gui_helper
import src.helper as _helper

_LIST_SIZE = [ "256x256", "512x256", "256x512", "512x512", ]
_LIST_ANCHOR = [ "Top-Left", "Top", "Top-Right", "Left", "Center", "Right", "Bottom-Left", "Bottom", "Bottom-Right", ]

class FrameSize(_ttk.Frame):
    """
    Represents a main window
    """

    #region init

    def __init__(self,\
            master:None|_tk.Misc = None,\
            showanchor:bool = True,\
            **kwargs:_Any):
        """
        Initializer for FrameSize
        """
        _PROMPTWIDTH = 15
        super().__init__(master = master, **kwargs)
        # X
        self.__widget_x_var = _tk.StringVar()
        self.__widget_x = _gui_helper.PVCombobox(\
            master = self,\
            kwargs = _helper.kwargs(\
                padding = (0, 0, 0, 5)),\
            p_kwargs = _helper.kwargs(\
                width = _PROMPTWIDTH,\
                text = "Size"),\
            v_kwargs = _helper.kwargs(\
                values = _LIST_SIZE,\
                textvariable = self.__widget_x_var,\
                state = 'readonly'),\
            )
        self.__widget_x.value.bind("<<ComboboxSelected>>", self.__r_widget_x_changed)
        self.__widget_x.value.set(_LIST_SIZE[0])
        self.__widget_x.pack(fill = 'x')
        # Anchor
        self.__widget_y_var = _tk.StringVar()
        self.__widget_y = _gui_helper.PVCombobox(\
            master = self,\
            kwargs = _helper.kwargs(\
                padding = (0, 0, 0, 5)),\
            p_kwargs = _helper.kwargs(\
                width = _PROMPTWIDTH,\
                text = "Anchor"),\
            v_kwargs = _helper.kwargs(\
                values = _LIST_ANCHOR,\
                textvariable = self.__widget_y_var,\
                state = 'readonly'),\
            )
        self.__widget_y.value.bind("<<ComboboxSelected>>", self.__r_widget_y_changed)
        self.__widget_y.value.set(_LIST_ANCHOR[0])
        if showanchor: self.__widget_y.pack(fill = 'x')
    
    #endregion

    #region receivers

    def __r_widget_x_changed(self, *args):
        selected_item = self.__widget_x.value.get()
        print(f"Selected: {selected_item}")

    def __r_widget_y_changed(self, *args):
        selected_item = self.__widget_y.value.get()
        print(f"Selected: {selected_item}")

    #endregion