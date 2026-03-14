__all__ = [\
    '_Foot']

import tkinter as _tk
import tkinter.ttk as _ttk

import qdg.helper as _qdg_helper

class _Foot(_ttk.Frame):
    """
    Represents a footer display
    """

    #region init

    def __init__(self, **kwargs):
        """
        Initializer for Foot
        """
        # Const
        _FONT = ("Small Fonts", 7)
        # Initialize
        super().__init__(**kwargs)
        # Cursor position
        self.__cursor = _qdg_helper.IXY_ZERO
        self.__widget_cursor = _ttk.Label(\
            master = self,\
            width = 8,\
            text = "0, 0",\
            font = _FONT)
        self.__widget_cursor.grid(column = 0, row = 0)
        # Map size
        self.__mapsize = _qdg_helper.IXY_ZERO
        self.__widget_mapsize = _ttk.Label(\
            master = self,\
            width = 8,\
            text = "0 x 0",\
            font = _FONT)
        self.__widget_mapsize.grid(column = 1, row = 0)
        
    #endregion

    #region properties

    @property
    def cursor(self):
        """ Cursor position """
        return self.__cursor
    @cursor.setter
    def cursor(self, value:_qdg_helper.IXY):
        if self.__cursor == value: return
        self.__cursor = value
        self.__widget_cursor.config(text = f"{self.__cursor.x}, {self.__cursor.y}")

    @property
    def mapsize(self):
        """ Map size """
        return self.__mapsize
    @mapsize.setter
    def mapsize(self, value:_qdg_helper.IXY):
        if self.__mapsize == value: return
        self.__mapsize = value
        self.__widget_mapsize.config(text = f"{self.__mapsize.x} x {self.__mapsize.y}")

    #endregion