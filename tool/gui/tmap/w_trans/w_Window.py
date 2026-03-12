import tkinter as _tk

from async_tkinter_loop import\
    async_handler as _async_handler
from tkinter import\
    ttk as _ttk

import gui.helper as _guihelper
import src.helper as _helper

class Window(_tk.Toplevel):
    """
    Represents a window for translating map tiles
    """

    #region init

    def __init__(self, *args, **kwargs):
        """
        Initializer for Window
        """
        _PROMPTWIDTH = 15
        super().__init__(*args, **kwargs)
        # Window Properties
        self.title("Translate")
        self.geometry('400x150')
        self.resizable(False, False)
        self.config(padx = 5, pady = 5)
        # X
        self.__widget_x_var = _tk.StringVar(value = "0")
        self.__widget_x_var.trace('w', self.__r_widget_x_changed)
        self.__widget_x = _guihelper.PVEntry(\
            master = self,\
            kwargs = _helper.kwargs(\
                padding = (0, 0, 0, 5)),\
            p_kwargs = _helper.kwargs(\
                text = "X",\
                width = _PROMPTWIDTH),\
            v_kwargs = _helper.kwargs(\
                textvariable = self.__widget_x_var),\
            )
        self.__widget_x.pack(fill = 'x')
        # Y
        self.__widget_y_var = _tk.StringVar(value = "0")
        self.__widget_y_var.trace('w', self.__r_widget_y_changed)
        self.__widget_y = _guihelper.PVEntry(\
            master = self,\
            kwargs = _helper.kwargs(\
                padding = (0, 0, 0, 5)),\
            p_kwargs = _helper.kwargs(\
                text = "Y",\
                width = _PROMPTWIDTH),\
            v_kwargs = _helper.kwargs(\
                textvariable = self.__widget_y_var),\
            )
        self.__widget_y.pack(fill = 'x')
        # Wrap X
        self.__widget_wrapx_var = _tk.BooleanVar(value = False)
        self.__widget_wrapx = _ttk.Checkbutton(\
            master = self,\
            variable = self.__widget_wrapx_var,\
            command = self.__r_widget_wrapx,\
            text = "Wrap X",\
            padding = (0, 0, 0, 5))
        self.__widget_wrapx.pack(fill = 'x')
        # Wrap Y
        self.__widget_wrapy_var = _tk.BooleanVar(value = False)
        self.__widget_wrapy = _ttk.Checkbutton(\
            master = self,\
            variable = self.__widget_wrapy_var,\
            command = self.__r_widget_wrapy,\
            text = "Wrap Y",\
            padding = (0, 0, 0, 5))
        self.__widget_wrapy.pack(fill = 'x')
        # Buttons
        self.__widget_buttons = _guihelper.ButtonRow(\
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

    def __r_widget_x_changed(self, *args):
        selected_item = self.__widget_x.value.get()
        print(f"Selected: {selected_item}")

    def __r_widget_y_changed(self, *args):
        selected_item = self.__widget_y.value.get()
        print(f"Selected: {selected_item}")

    def __r_widget_wrapx(self):
        print(self.__widget_wrapx_var.get())

    def __r_widget_wrapy(self):
        print(self.__widget_wrapy_var.get())

    def __r_widget_buttons_ok(self):
        print("OK")

    def __r_widget_buttons_cancel(self):
        print("Cancel")

    #endregion