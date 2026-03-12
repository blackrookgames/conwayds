import numpy as _np
import tkinter as _tk

import gui.tmap.w__common as _tmap_common
from .m_ContentSize import ContentSize as _ContentSize

class ContentCells:
    """
    Represents tile cell content
    """
    
    #region init

    def __init__(self,\
            size:_ContentSize):
        """
        Initializer for ContentCells

        :param size: Map size
        """
        self.__format_map(size)

    #endregion

    #region operators

    def __len__(self): return len(self.__cells)

    def __getitem__(self, key:int|tuple[int, int]):
        """
        Gets the cell at the specified coordinates

        :raise IndexError: Coordinates are out of range
        """
        return self.__cells[self.__index(key)]

    def __setitem__(self, key:int|tuple[int, int], value:_np.uint16):
        """
        Sets the cell at the specified coordinates

        :raise IndexError: Coordinates are out of range
        """
        self.__cells[self.__index(key)] = value

    #endregion

    #region properties

    @property
    def size(self):
        """ Map size """
        return self.__size
    
    @property
    def width(self):
        """ Map width """
        return self.__width
    
    @property
    def height(self):
        """ Map height """
        return self.__height

    #endregion

    #region helper methods

    def __format_map(self, size:_ContentSize):
        def _format(_width:int, _height:int):
            return _width, _height, _np.zeros(_width * _height, dtype = _np.uint16)
        match size:
            case _ContentSize.W256H256:
                self.__width, self.__height, self.__cells = _format(256, 256)
            case _ContentSize.W512H256:
                self.__width, self.__height, self.__cells = _format(512, 256)
            case _ContentSize.W256H512:
                self.__width, self.__height, self.__cells = _format(256, 512)
            case _:
                self.__width, self.__height, self.__cells = _format(512, 512)
        self.__size = size
    
    def __index(self, key:int|tuple[int, int]):
        if isinstance(key, int):
            if key < 0 or key >= len(self.__cells):
                raise IndexError("Index is out of range.")
            return key
        else:
            x, y = key
            if x < 0 or x >= self.__width:
                raise IndexError("X-coordinate is out of range.")
            if y < 0 or y >= self.__height:
                raise IndexError("Y-coordinate is out of range.")
            return x + y * self.__width

    #endregion

    #region methods

    def resize(self, size:_ContentSize, offset_x:int = 0, offset_y:int = 0):
        """
        Resizes the map

        :param size: New size
        :param offset_x: X-offset
        :param offset_y: Y-offset
        """
        # Remember previous
        prev_width = self.__width
        prev_height = self.__height
        prev_cells = self.__cells
        # Format
        self.__format_map(size)
        # Copy data
        _beg_x = max(0, min(self.__width, offset_x))
        _beg_y = max(0, min(self.__height, offset_y))
        _end_x = max(0, min(self.__width, offset_x + prev_width))
        _end_y = max(0, min(self.__height, offset_y + prev_height))
        _off_x = _beg_x - offset_x
        _off_y = _beg_y - offset_y
        for _y in range(_beg_y, _end_y):
            for _x in range(_beg_x, _end_x):
                _i = (_off_x + _x) + (_off_y + _y) * prev_width
                _o = _x + _y * self.__width
                self.__cells[_o] = prev_cells[_i]

    #endregion