__all__ = ['FrameTileset']

import tkinter as _tk

from async_tkinter_loop import\
    async_handler as _async_handler
from tkinter import\
    ttk as _ttk
from typing import\
    Any as _Any

from .g_FramePath import FramePath as _FramePath
from .m_SignalHandler import SignalHandler as _SignalHandler
from .m_SignalReceiver import SignalReceiver as _SignalReceiver

class FrameTileset(_ttk.Frame):
    """
    Represents a frame for configuring the tileset
    """

    #region init

    def __init__(self,\
            master:None|_tk.Misc = None,\
            **kwargs:_Any):
        """
        Initializer for FrameTileset
        """
        super().__init__(master = master, **kwargs)
        FILETYPES = ( ( "Bitmap", "*.bmp", ), )
        #region Tileset
        self.__widget_t = _ttk.LabelFrame(\
            master = self,\
            padding = (5, 5, 5, 5),\
            text = "Tileset")
        self.__widget_t.pack(fill = 'x')
        # Path
        self.__widget_t_path = _FramePath(\
            master = self.__widget_t)
        self.__widget_t_path.dialog_title = "Browse for a Paletted Bitmap"
        self.__widget_t_path.dialog_filetypes = FILETYPES
        self.__widget_t_path.pack(fill = 'x')
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
        self.__widget_p_path = _FramePath(\
            master = self.__widget_p)
        self.__widget_p_path.enabled = False
        self.__widget_p_path.dialog_title = "Browse for a Paletted Bitmap"
        self.__widget_p_path.dialog_filetypes = FILETYPES
        self.__widget_p_path.pack(fill = 'x')
        #endregion
        #region signals
        
        #endregion
    
    #endregion

    #region properties

    @property
    def tileset_path(self):
        """ Tileset path """
        return self.__widget_t_path.path
    
    @property
    def palette_custom(self):
        """ Whether or not a custom palette should be used """
        return self.__widget_p_path.enabled

    @property
    def palette_path(self):
        """ Palette path """
        return self.__widget_p_path.path

    #endregion

    #region receivers

    def __r_widget_p_custom(self):
        value = self.__widget_p_custom_var.get()
        self.__widget_p_path.enabled = value

    #endregion