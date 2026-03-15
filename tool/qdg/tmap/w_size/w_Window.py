__all__ = ['Window']

import numpy as _np
import tkinter as _tk
import tkinter.ttk as _ttk
import tkinter.messagebox as _tk_messagebox

from PIL import\
    Image as _Image,\
    ImageTk as _ImageTk

import qdg.helper as _qdg_helper
import qdg.tmap.w__common as _tmap_common
import src.helper as _helper

from .m_Anchor import Anchor as _Anchor

_SIZES = {\
    "256x256": _tmap_common.ContentSize.W256H256,\
    "512x256": _tmap_common.ContentSize.W512H256,\
    "256x512": _tmap_common.ContentSize.W256H512,\
    "512x512": _tmap_common.ContentSize.W512H512,}

_ANCHORS = {\
    "Top-left": _Anchor.TOPLEFT,\
    "Top": _Anchor.TOP,\
    "Top-right": _Anchor.TOPRIGHT,\
    "Left": _Anchor.LEFT,\
    "Center": _Anchor.CENTER,\
    "Right": _Anchor.RIGHT,\
    "Bottom-left": _Anchor.BOTTOMLEFT,\
    "Bottom": _Anchor.BOTTOM,\
    "Bottom-right": _Anchor.BOTTOMRIGHT}

class Window(_qdg_helper.WinDialog):
    """
    Represents a window for configuring the size
    """

    #region init

    def __init__(self,\
            initsize:_tmap_common.ContentSize = _tmap_common.ContentSize.W256H256,\
            *args, **kwargs):
        """
        Initializer for Window

        :param initsize: Initial size
        """
        # Initialize
        super().__init__(*args, **kwargs)
        self._set_result(_qdg_helper.WinDialogResult.CANCEL)
        self.title("Set Size")
        self.geometry('200x100')
        self.resizable(False, False)
        self.config(padx = 5, pady = 5)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        # Size
        self.__size = initsize
        self.__size_variable = _tk.StringVar()
        self.__size_label = _ttk.Label(\
            master = self,\
            text = "Size")
        self.__size_value = _ttk.Combobox(\
            master = self,\
            state = 'readonly',\
            textvariable = self.__size_variable,\
            values = list(_SIZES.keys()))
        self.__size_value.bind('<<ComboboxSelected>>', self.__r_size_value_changed)
        self.__size_value.set(_helper.DictUtil.findkey(_SIZES, self.__size))
        self.__size_label.grid(column = 0, row = 0, sticky = 'nw', padx = (0, 25))
        self.__size_value.grid(column = 1, row = 0, sticky = 'nwe', pady = (0, 5))
        # Anchor
        self.__anchor = _Anchor.TOPLEFT
        self.__anchor_variable = _tk.StringVar()
        self.__anchor_label = _ttk.Label(\
            master = self,\
            text = "Anchor")
        self.__anchor_value = _ttk.Combobox(\
            master = self,\
            state = 'readonly',\
            textvariable = self.__anchor_variable,\
            values = list(_ANCHORS.keys()))
        self.__anchor_value.bind('<<ComboboxSelected>>', self.__r_anchor_value_changed)
        self.__anchor_value.set(_helper.DictUtil.findkey(_ANCHORS, self.__anchor))
        self.__anchor_label.grid(column = 0, row = 1, sticky = 'nw', padx = (0, 25))
        self.__anchor_value.grid(column = 1, row = 1, sticky = 'nwe', pady = (0, 5))
        # Buttons
        self.__widget_buttons = _qdg_helper.ButtonRow(\
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
        self.__widget_buttons.grid(column = 0, row = 2, columnspan = 2, sticky = 'sw')
    
    #endregion

    #region properties

    @property
    def size(self):
        """ Size """
        return self.__size

    @property
    def anchor(self):
        """ Anchor """
        return self.__anchor
    
    #endregion

    #region receivers

    def __r_size_value_changed(self, *args):
        self.__size = _SIZES[self.__size_variable.get()]

    def __r_anchor_value_changed(self, *args):
        self.__anchor = _ANCHORS[self.__anchor_variable.get()]

    def __r_widget_buttons_ok(self):
        self._set_result(_qdg_helper.WinDialogResult.OK)
        self.destroy()

    def __r_widget_buttons_cancel(self):
        self.destroy()

    #endregion