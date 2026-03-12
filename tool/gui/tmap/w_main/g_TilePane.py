import tkinter as _tk

from tkinter import\
    ttk as _ttk
from typing import\
    Any as _Any

class TilePane(_ttk.Frame):
    """
    Represents a tileset pane
    """

    #region init

    def __init__(self,\
            master:None|_tk.Misc,\
            **kwargs:_Any):
        """
        Initializer for TilePane
        """
        super().__init__(master = master, **kwargs)
        self.columnconfigure(3, weight = 1)
        self.rowconfigure(1, pad = 10)
        self.rowconfigure(2, weight = 1)
        # Sub-palette
        self.__widget_sub_var = _tk.StringVar()
        self.__widget_sub = _ttk.Combobox(\
            self,\
            textvariable = self.__widget_sub_var,\
            values = [f"Sub-Pallete {_i:01X}" for _i in range(16)],\
            state = 'readonly',\
            width = 12)
        self.__widget_sub.configure(\
            state = _tk.DISABLED)
        self.__widget_sub.bind("<<ComboboxSelected>>", self.__r_widget_sub_selected)
        self.__widget_sub.set("Sub-Pallete 0")
        self.__widget_sub.grid(column = 0, row = 0)
        # Flip X
        self.__widget_flipx_var = _tk.BooleanVar(value=False)
        self.__widget_flipx = _ttk.Checkbutton(\
            self,\
            text = "Flip X",\
            variable = self.__widget_flipx_var,\
            command = self.__r_widget_flipx,\
            padding = (5, 0, 0, 0))
        self.__widget_flipx.configure(\
            state = _tk.DISABLED)
        self.__widget_flipx.grid(column = 1, row = 0)
        # Flip Y
        self.__widget_flipy_var = _tk.BooleanVar(value=False)
        self.__widget_flipy = _ttk.Checkbutton(\
            self,\
            text = "Flip Y",\
            variable = self.__widget_flipy_var,\
            command = self.__r_widget_flipy,\
            padding = (5, 0, 0, 0))
        self.__widget_flipy.configure(\
            state = _tk.DISABLED)
        self.__widget_flipy.grid(column = 2, row = 0)
        # Tiles
        self.__widget_tiles_image:None|int = None
        self.__widget_tiles = _tk.Canvas(\
            self,\
            width = 256,\
            height = 256,\
            bg = '#D0D0D0',\
            highlightthickness = 0)
        self.__widget_tiles.config()
        self.__widget_tiles.grid(column = 0, row = 1, columnspan = 4)
    
    #endregion

    #region receivers

    def __r_widget_sub_selected(self, event):
        selected_item = self.__widget_sub.get()
        print(f"Selected: {selected_item}")

    def __r_widget_flipx(self):
        print(self.__widget_flipx_var.get())

    def __r_widget_flipy(self):
        print(self.__widget_flipy_var.get())

    #endregion

    #region methods

    def test(self, image:_tk.PhotoImage):
        self.__widget_tiles_image = self.__widget_tiles.create_image(\
            (0, 0),\
            image = image,\
            anchor = "nw")
    
    #endregion