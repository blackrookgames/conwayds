import tkinter as _tk
import tkinter.messagebox as _tk_messagebox

from async_tkinter_loop import\
    async_handler as _async_handler
from tkinter import\
    ttk as _ttk

import gui.tmap.w__common as _tmap_common
import gui.tmap.w_new as _tmap_new
import gui.tmap.w_size as _tmap_size
import gui.tmap.w_tile as _tmap_tile
import gui.tmap.w_trans as _tmap_trans

from .d_TileData import TileData as _TileData
from .g_MapView import MapView as _MapView
from .g_MenuBar import MenuBar as _MenuBar
from .g_StatusBar import StatusBar as _StatusBar
from .g_TilePane import TilePane as _TilePane
from .g_ToolPane import ToolPane as _ToolPane

class Window(_tk.Tk):
    """
    Represents a main window
    """

    #region init

    def __init__(self, *args, **kwargs):
        """
        Initializer for Window
        """
        super().__init__(*args, **kwargs)
        #region fields
        self.__tiledata:None|_TileData = None
        #endregion
        #region tkinter
        self.title("tmap")
        self.geometry("800x600")
        self.minsize(width = 650, height = 350)
        # Menu
        self.__widget_menu = _MenuBar(self,\
            self.__r_widget_menu_file_new,\
            self.__r_widget_menu_file_open,\
            self.__r_widget_menu_file_save,\
            self.__r_widget_menu_file_saveas,\
            self.__r_widget_menu_file_exit,\
            self.__r_widget_menu_map_tileset,\
            self.__r_widget_menu_map_size,\
            self.__r_widget_menu_trans_pos)
        self.config(menu = self.__widget_menu)
        # Main Frame
        self.__widget_f = _ttk.Frame(self, padding = 5)
        self.__widget_f.columnconfigure(1, weight = 1)
        self.__widget_f.rowconfigure(0, weight = 1)
        self.__widget_f.pack(fill = 'both', expand = True)
        # Tool Pane
        self.__widget_f_tools = _ToolPane(\
            self.__widget_f,\
            width = 60,\
            padding = (0, 0, 5, 0))
        self.__widget_f_tools.grid(column = 0, row = 0, sticky = 'ns')
        # Map View
        self.__widget_f_map = _MapView(\
            self.__widget_f)
        self.__widget_f_map.grid(column = 1, row = 0, sticky = 'nsew')
        # Tileset
        self.__widget_f_tile = _TilePane(\
            self.__widget_f,\
            width = 270,\
            padding = (5, 0, 0, 0))
        self.__widget_f_tile.grid(column = 2, row = 0, sticky = 'ns')
        # Status
        self.__widget_status = _StatusBar(self)
        self.__widget_status.pack(fill = 'x', anchor = 's')
        #endregion
        #region post-init

        #endregion

    #endregion

    #region receivers

    #region Menu

    def __r_widget_menu_file_new(self):
        dialog = _tmap_new.Window(self)
        dialog.transient(self)
        dialog.grab_set()
        dialog.wait_window()

    def __r_widget_menu_file_open(self):
        print("Open")

    def __r_widget_menu_file_save(self):
        print("Save")

    def __r_widget_menu_file_saveas(self):
        print("Save As")

    def __r_widget_menu_file_exit(self):
        print("Exit")

    def __r_widget_menu_map_tileset(self):
        dialog = _tmap_tile.Window(self)
        dialog.transient(self)
        dialog.grab_set()
        dialog.wait_window()

    def __r_widget_menu_map_size(self):
        dialog = _tmap_size.Window(self)
        dialog.transient(self)
        dialog.grab_set()
        dialog.wait_window()

    def __r_widget_menu_trans_pos(self):
        dialog = _tmap_trans.Window(self)
        dialog.transient(self)
        dialog.grab_set()
        dialog.wait_window()

    #endregion

    #endregion

    #region helper methods

    #endregion