import tkinter as _tk

from async_tkinter_loop import\
    async_handler as _async_handler
from tkinter import\
    ttk as _ttk

import gui.helper as _guihelper
import src.helper as _helper

import gui.tmap.w__common as _tmap_common

class Window(_guihelper.WinDialog):
    """
    Represents a window for configuring a new tilemap
    """

    #region init

    def __init__(self,\
            init_tileset_path:None|str = None,\
            init_palette_path:None|str = None,\
            init_size:None|_tmap_common.ContentSize = None,\
            *args, **kwargs):
        """
        Initializer for Window

        :param init_tileset_path: Initial tileset path
        :param init_palette_path: Initial palette path
        :param init_size: Initial size
        """
        super().__init__(\
            initresult = _guihelper.WinDialogResult.CANCEL,\
            *args, **kwargs)
        # Fields
        self.__content:None|_tmap_common.Content = None
        # Window Properties
        self.title("New Tilemap")
        self.geometry('400x200')
        self.resizable(False, False)
        self.config(padx = 5, pady = 5)
        # Tileset
        self.__widget_tileset = _tmap_common.FrameTileset(\
            master = self,\
            padding = (0, 0, 0, 5))
        self.__widget_tileset.pack(fill = 'x')
        # Size
        self.__widget_size = _tmap_common.FrameSize(\
            master = self,\
            showanchor = False,\
            padding = (0, 0, 0, 5))
        self.__widget_size.pack(fill = 'x')
        # Buttons
        self.__widget_buttons = _guihelper.ButtonRow(\
            self,\
            buttons = [\
                _helper.kwargs(\
                    command = _async_handler(self.__r_widget_buttons_ok),\
                    text = "OK"),\
                _helper.kwargs(\
                    command = self.__r_widget_buttons_cancel,\
                    text = "Cancel"),\
                ],\
            )
        self.__widget_buttons.pack(fill = 'x', anchor = 's', expand = True)
    
    #endregion

    #region properties

    @property
    def content(self):
        """ Content """
        return self.__content
    
    #endregion

    #region receivers

    async def __r_widget_buttons_ok(self):
        # Run task
        task_tileset_path = self.__widget_tileset.tileset_path
        task_palette_path = self.__widget_tileset.palette_path if self.__widget_tileset.palette_custom else None
        task = _tmap_common.TaskTileset(self, task_tileset_path, task_palette_path)
        await task.start()
        # Check result
        if task.state != _guihelper.GUITaskState.FINISH: return
        self.destroy()
        self._set_result(_guihelper.WinDialogResult.OK)
        # Create content
        assert task.output is not None
        self.__content = _tmap_common.Content(\
            None,\
            task.output.tile_set,\
            task.output.tile_pal,\
            task.output.tile_img,\
            _tmap_common.ContentSize.W256H256) # TODO: Fix size

    def __r_widget_buttons_cancel(self):
        self.destroy()

    #endregion