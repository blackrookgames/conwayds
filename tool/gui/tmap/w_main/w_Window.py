import asyncio as _asyncio
import tkinter as _tk
import tkinter.messagebox as _tk_messagebox

from async_tkinter_loop import\
    async_handler as _async_handler
from pathlib import\
    Path as _Path
from tkinter import\
    ttk as _ttk

import gui.helper as _guihelper
import gui.tmap.w__common as _tmap_common
import gui.tmap.w_new as _tmap_new
import gui.tmap.w_size as _tmap_size
import gui.tmap.w_tile as _tmap_tile
import gui.tmap.w_trans as _tmap_trans

from gui.tmap.w__common.m_Content import Content as _Content
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
        self.__content:None|_Content = None
        self.__isdirty:bool = False
        #endregion
        #region tkinter
        self.geometry("800x600")
        self.minsize(width = 650, height = 350)
        self.protocol("WM_DELETE_WINDOW", self.__r_wm_delete_window)
        # Menu
        self.__widget_menu = _MenuBar(self,\
            _async_handler(self.__r_widget_menu_file_new),\
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
        self.__update_title()
        #endregion

    #endregion

    #region receivers
    
    #region window

    def __r_wm_delete_window(self): self.__quit()

    #endregion

    #region Menu

    async def __r_widget_menu_file_new(self):
        # Create dialog
        if self.__content is not None:
            dialog_init_tileset_path = self.__content.tile_set.path
            dialog_init_palette_path = None if (self.__content.tile_pal is None) else self.__content.tile_pal.path
            dialog_init_size = self.__content.cells.size
        else:
            dialog_init_tileset_path = None
            dialog_init_palette_path = None
            dialog_init_size = None
        dialog = _tmap_new.Window(\
            init_tileset_path = dialog_init_tileset_path,\
            init_palette_path = dialog_init_palette_path,\
            init_size = dialog_init_size,\
            master = self)
        # Open dialog
        async def _dialog_task():
            nonlocal dialog
            dialog.transient(self)
            dialog.grab_set()
            while dialog.winfo_exists(): await _asyncio.sleep(0)
        dialog_task = _asyncio.create_task(_dialog_task())
        while not dialog_task.done(): await _asyncio.sleep(0)
        if dialog.result != _guihelper.WinDialogResult.OK: return
        # Set content
        self.__set_content(dialog.content)

    def __r_widget_menu_file_open(self):
        print("Open")

    def __r_widget_menu_file_save(self):
        print("Save")

    def __r_widget_menu_file_saveas(self):
        print("Save As")

    def __r_widget_menu_file_exit(self):
        self.__quit()

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

    @classmethod
    def __pathname(cls, path:None|str):
        if path is None: return "Untitled"
        return _Path(path).name

    def __set_content(self, content:None|_Content):
        self.__content = content
        self.__isdirty = False
        # Update title
        self.__update_title()
        # TODO: Remove
        if self.__content is not None:
            self.__widget_f_tile.test(self.__content.tile_img)
        # TODO: Update GUI

    def __update_title(self):
        if self.__content is not None:
            _dirty = "*" if self.__isdirty else ""
            prefix = f"{_dirty}{self.__pathname(self.__content.path)} - "
        else: prefix = ""
        self.title(f"{prefix}tmap")
    
    def __quit(self):
        if self.__content is not None and self.__isdirty:
            _warn = _tk_messagebox.askyesnocancel(\
                "Unsaved Changes",\
                f"Save changes to {self.__pathname(self.__content.path)}?")
            if _warn is None: return
            if _warn:
                # TODO: Save
                pass
        self.destroy()

    #endregion