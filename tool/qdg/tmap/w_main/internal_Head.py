__all__ = [\
    '_Head']

import tkinter as _tk
import tkinter.ttk as _ttk

import qdg.helper as _qdg_helper

class _Head(_ttk.Frame):
    """
    Represents a header display
    """

    #region init

    def __init__(self, **kwargs):
        """
        Initializer for Head
        """
        # Const
        _FONT = ("Small Fonts", 7)
        # Initialize
        super().__init__(**kwargs)
        # Text Mode
        self.__textmode = False
        self.__widget_textmode = _ttk.Label(\
            master = self,\
            width = 12,\
            text = "Draw Mode",\
            font = _FONT)
        self.__widget_textmode.grid(column = 0, row = 0, sticky = 'w')
        # Tile
        self.__tile = 0
        self.__widget_tile = _ttk.Label(\
            master = self,\
            width = 12,\
            text = "Tile: 0x000",\
            font = _FONT)
        self.__widget_tile.grid(column = 0, row = 1, sticky = 'w')
        # Palette
        self.__palette = 0
        self.__widget_palette = _ttk.Label(\
            master = self,\
            width = 12,\
            text = "Palette: 0x0",\
            font = _FONT)
        self.__widget_palette.grid(column = 1, row = 1, sticky = 'w')
        # Orientation
        self.__orientation = 0
        self.__widget_orientation = _ttk.Label(\
            master = self,\
            width = 12,\
            text = "Orient: 0",\
            font = _FONT)
        self.__widget_orientation.grid(column = 2, row = 1, sticky = 'w')
        
    #endregion

    #region properties

    @property
    def textmode(self):
        """ Whether or not editor is in text mode """
        return self.__textmode
    @textmode.setter
    def textmode(self, value:bool):
        if self.__textmode == value: return
        self.__textmode = value
        self.__widget_textmode.config(text = "Text Mode" if self.__textmode else "Draw Mode")

    @property
    def tile(self):
        """ Tile index """
        return self.__tile
    @tile.setter
    def tile(self, value:int):
        if self.__tile == value: return
        self.__tile = value
        self.__widget_tile.config(text = f"Tile: 0x{self.__tile:03X}")

    @property
    def palette(self):
        """ Palette index """
        return self.__palette
    @palette.setter
    def palette(self, value:int):
        if self.__palette == value: return
        self.__palette = value
        self.__widget_palette.config(text = f"Palette: 0x{self.__palette:01X}")

    @property
    def orientation(self):
        """ Orientation """
        return self.__orientation
    @orientation.setter
    def orientation(self, value:int):
        if self.__orientation == value: return
        self.__orientation = value
        self.__widget_orientation.config(text = f"Orient: {self.__orientation}")

    #endregion