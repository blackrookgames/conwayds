__all__ = ['TaskTileset']

import asyncio as _asyncio
import tkinter as _tk
import tkinter.messagebox as _tk_messagebox

from tkinter import\
    ttk as _ttk
from typing import\
    Any as _Any,\
    NamedTuple as _NamedTuple

import gui.helper as _guihelper
import src.cliutil as _cliutil

from .f_IDataPalette import\
    IDATAPALETTE_SUBCOUNT as _IDATAPALETTE_SUBCOUNT
from .f_IDataTileset import\
    IDATATILESET_SIZE as _IDATATILESET_SIZE,\
    IDATATILESET_TILE_H as _IDATATILESET_TILE_H,\
    IDATATILESET_TILE_W as _IDATATILESET_TILE_W
from .f_IFilePalette import\
    IFilePalette as _IFilePalette
from .f_IFileTileset import\
    IFileTileset as _IFileTileset

class TaskTileset(_guihelper.GUITask):
    """
    Represents a task for processing a tileset
    """

    #region nested

    class Output(_NamedTuple):
        tile_set:_IFileTileset
        tile_pal:None|_IFilePalette
        tile_img:_tk.PhotoImage

    class __Win(_guihelper.WinDialog):
        #region init
        def __init__(self,\
                *args, **kwargs):
            super().__init__(\
                initresult = _guihelper.WinDialogResult.OK,\
                padx = 5, pady = 5,\
                *args, **kwargs)
            self.title("Processing Tileset")
            self.geometry('400x100')
            self.resizable(False, False)
            self.protocol("WM_DELETE_WINDOW", self.__r_wm_delete_window)
            # Desc
            self.__widget_desc = _ttk.Label(\
                master = self)
            self.__widget_desc.pack(fill = 'x')
            # Progress Bar
            self.__widget_progress = _ttk.Progressbar(\
                master = self)
            self.__widget_progress.pack(fill = 'x')
        #endregion
        #region receivers
        def __r_wm_delete_window(self):
            self._set_result(_guihelper.WinDialogResult.CANCEL)
        #endregion
        #region methods
        def set_desc(self, value:str):
            self.__widget_desc.config(text = value)
        def set_progress(self, value:float):
            self.__widget_progress['value'] = value
        #endregion
    
    #endregion

    #region init

    def __init__(self, master:None|_tk.Toplevel, tileset_path:None|str, palette_path:None|str):
        """
        Initializer for TaskTileset

        :param master: Master widget
        :param tileset_path: Path of file containing tileset
        :param palette_path: Path of file containing palette
        """
        super().__init__()
        self.__output:None|TaskTileset.Output = None
        self.__master = master
        self.__tileset_path = tileset_path
        self.__palette_path = palette_path
    
    #endregion

    #region properties

    @property
    def output(self):
        """ Task output """
        return self.__output
    
    #endregion

    #region methods

    async def _start(self):
        # Create window
        win = self.__Win(master = self.__master)
        win.transient(self.__master)
        win.grab_set()
        # Create processing task
        task_stop = False
        task_fail = False
        task_desc = ""
        task_prog = 0.0
        async def _task():
            nonlocal self, task_desc, task_prog, task_fail
            def _error(_title, _e):
                nonlocal task_fail
                _tk_messagebox.showerror(_title, str(_e))
                task_fail = True
            _TILECOUNT = 0x10000
            # Load tileset
            try:
                _tile_set = _IFileTileset(self.__tileset_path)
            except _cliutil.CLICommandError as _e:
                _error("Error Loading Tileset", _e)
                return
            # Load palette
            try:
                if self.__palette_path is None: _tile_pal = None
                else: _tile_pal = _IFilePalette(self.__palette_path)
            except _cliutil.CLICommandError as _e:
                _error("Error Loading Palette", _e)
                return
            # Determine palette to use
            _palette = _tile_set.palette if (_tile_pal is None) else _tile_pal.palette
            # Create image
            task_desc = "Processing tileset"
            task_prog = 0.0
            _tile_img = _tk.PhotoImage(width = 2048, height = 2048)
            for _i in range(_TILECOUNT):
                if task_stop: return
                # Properties
                _tile_index = _i % _IDATATILESET_SIZE
                _tile_props = _i // _IDATATILESET_SIZE
                _tile_sub = _tile_props % _IDATAPALETTE_SUBCOUNT # TODO: Update
                _tile_flip = _tile_props // _IDATAPALETTE_SUBCOUNT # TODO: Update
                _tile_flip_x = (_tile_flip & 0b01) != 0 # TODO: Update
                _tile_flip_y = (_tile_flip & 0b10) != 0 # TODO: Update
                # Input X-coordinates
                if _tile_flip_x:
                    _x_beg = _IDATATILESET_TILE_W - 1
                    _x_inc = -1
                else:
                    _x_beg = 0
                    _x_inc = 1
                # Input Y-coordinates
                if _tile_flip_y:
                    _y_beg = _IDATATILESET_TILE_H - 1
                    _y_inc = -1
                else:
                    _y_beg = 0
                    _y_inc = 1
                # Tile
                _off_x = (_i % 32) * _IDATATILESET_TILE_W
                _off_y = (_i // 32) * _IDATATILESET_TILE_H
                for _x in range(_IDATATILESET_TILE_W):
                    _column:list[str] = []
                    for _y in range(_IDATATILESET_TILE_H):
                        _pixel = _tile_set.tileset[_tile_index, _x_beg + _x * _x_inc, _y_beg + _y * _y_inc]
                        _column.append(_palette[_tile_sub][_pixel])
                    _to = (\
                        _off_x + _x, _off_y,\
                        _off_x + _x + 1, _off_y + _IDATATILESET_TILE_H)
                    _tile_img.put(_column, _to)
                # Next
                task_prog = 100 * ((_i + 1) / _TILECOUNT)
                await _asyncio.sleep(0)
            # Success
            self.__output = self.Output(_tile_set, _tile_pal, _tile_img)
            return
        task = _asyncio.create_task(_task())
        # Wait for task to finish
        while not task.done():
            # Check if user requested to cancel
            if win.result != _guihelper.WinDialogResult.OK:
                task_stop = True
            # Update window visuals
            win.set_desc(task_desc)
            win.set_progress(task_prog)
            # Next
            await _asyncio.sleep(0.1)
        # Destroy window
        win.destroy()
        # Make sure processing completed
        if win.result != _guihelper.WinDialogResult.OK: return _guihelper.GUITaskState.CANCEL
        # Success!!!
        return _guihelper.GUITaskState.FINISH

    #endregion