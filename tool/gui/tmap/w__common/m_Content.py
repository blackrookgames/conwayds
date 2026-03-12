import numpy as _np
import tkinter as _tk

from .f_IFilePalette import IFilePalette as _IFilePalette
from .f_IFileTileset import IFileTileset as _IFileTileset
from .m_ContentCells import ContentCells as _ContentCells
from .m_ContentSize import ContentSize as _ContentSize

class Content:
    """
    Represents the content being edited
    """
    
    #region init

    def __init__(self,\
            path:None|str,\
            tile_set:_IFileTileset,\
            tile_pal:None|_IFilePalette,\
            tile_img:_tk.PhotoImage,\
            size:_ContentSize):
        """
        Initializer for Content

        :param path: Filepath
        :param tile_set: Tileset data
        :param tile_pal: Custom palette data
        :param tile_img: Image representation of all 65536 tiles
        :param size: Map size
        """
        self.__path = path
        self.__tile_set = tile_set
        self.__tile_pal = tile_pal
        self.__tile_img = tile_img
        self.__cells = _ContentCells(size)

    #endregion

    #region properties

    @property
    def path(self):
        """ Filepath """
        return self.__path
    @path.setter
    def path(self, value:None|str):
        self.__path = value

    @property
    def tile_set(self):
        """ Tileset data """
        return self.__tile_set
    @tile_set.setter
    def tile_set(self, value:_IFileTileset):
        self.__tile_set = value

    @property
    def tile_pal(self):
        """ Custom palette data """
        return self.__tile_pal
    @tile_pal.setter
    def tile_pal(self, value:None|_IFilePalette):
        self.__tile_pal = value

    @property
    def tile_img(self):
        """ Image representation of all 65536 tiles """
        return self.__tile_img
    @tile_img.setter
    def tile_img(self, value:_tk.PhotoImage):
        self.__tile_img = value

    @property
    def cells(self):
        """ Map cells """
        return self.__cells

    #endregion