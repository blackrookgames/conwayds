import tkinter as _tk

from tkinter import\
    ttk as _ttk
from typing import\
    Any as _Any,\
    Callable as _Callable

class MenuBar(_tk.Menu):
    """
    Represents a menu bar
    """

    #region init

    def __init__(self,\
            master:None|_tk.Misc,\
            file_new_cmd:_Callable[[], None],\
            file_open_cmd:_Callable[[], None],\
            file_save_cmd:_Callable[[], None],\
            file_saveas_cmd:_Callable[[], None],\
            file_exit_cmd:_Callable[[], None],\
            map_tile_cmd:_Callable[[], None],\
            map_size_cmd:_Callable[[], None],\
            trans_pos_cmd:_Callable[[], None],\
            **kwargs:_Any):
        """
        Initializer for MenuBar
        """
        super().__init__(\
            master = master,\
            tearoff = 0,\
            **kwargs)
        # File
        self.__widget_mf = _tk.Menu(self, tearoff = 0)
        self.__widget_mf.add_command(\
            label = "New",\
            command =      file_new_cmd)
        self.__widget_mf.add_command(\
            label = "Open",\
            command =      file_open_cmd)
        self.__widget_mf.add_command(\
            label = "Save",\
            command =      file_save_cmd,\
            state = _tk.DISABLED)
        self.__widget_mf.add_command(\
            label = "Save As",\
            command =      file_saveas_cmd,\
            state = _tk.DISABLED)
        self.__widget_mf.add_command(\
            label = "Exit",\
            command =      file_exit_cmd)
        self.add_cascade(label = "File", menu = self.__widget_mf)
        # Map
        self.__widget_mm = _tk.Menu(self, tearoff = 0)
        self.__widget_mm.add_command(\
            label = "Tileset",\
            command =      map_tile_cmd,\
            state = _tk.DISABLED)
        self.__widget_mm.add_command(\
            label = "Size",\
            command =      map_size_cmd,\
            state = _tk.DISABLED)
        self.add_cascade(label = "Map", menu = self.__widget_mm)
        # Transform
        self.__widget_mt = _tk.Menu(self, tearoff = 0)
        self.__widget_mt.add_command(\
            label = "Translate",\
            command =      trans_pos_cmd,\
            state = _tk.DISABLED)
        self.add_cascade(label = "Modify", menu = self.__widget_mt)
    
    #endregion