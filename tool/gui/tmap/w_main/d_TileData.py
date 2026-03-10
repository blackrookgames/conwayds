import tkinter as _tk

import gui.tmap.w__common as _tmap_common

class TileData:
    """
    Represents a main window's tile data
    """
    
    #region init

    def __init__(self,\
            tileset:_tmap_common.FileTileset,\
            custompal:None|_tmap_common.FilePalette,\
            image:_tk.PhotoImage):
        """
        Initializer for TileData

        :param tileset: Tileset
        :param custompal: Custom palette
        :param image: Image representation of all 65536 tiles
        """
        self.__tileset = tileset
        self.__custompal = custompal
        self.__image = image

    #endregion

    #region properties

    @property
    def tileset(self):
        """Tileset"""
        return self.__tileset

    @property
    def custompal(self):
        """Custom palette"""
        return self.__custompal

    @property
    def image(self):
        """Image representation of all 65536 tiles"""
        return self.__image

    #endregion