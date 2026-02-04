__all__ = [\
    'ImgPalette',\
    'IMGPALETTE_MAX',]

import numpy as _np

from typing import\
    cast as _cast

from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil
from .mod_ImgColor import\
    ImgColor as _ImgColor

IMGPALETTE_MAX = 256
"""
Maximum palette size
"""

class ImgPalette:
    """
    Represents a color palette
    """

    #region init

    def __init__(self, size:int = IMGPALETTE_MAX):
        """
        Initializer for ImgPalette
        
        :param size:
            Number of colors in palette
        :raise ValueError:
            size is less than 0 or greater than IMGPALETTE_MAX
        """
        try:
            self.format(size = size)
            return
        except ValueError as _e:
            e = _e
        raise e

    #endregion

    #region operator
    
    def __len__(self):
        return len(self.__colors)
    
    def __getitem__(self, index):
        try:
            _index = self.__index(index)
            return _cast(_ImgColor, self.__colors[_index])
        except TypeError as _e:
            e = _e
        except ValueError as _e:
            e = _e
        raise e
    
    def __setitem__(self, index, value):
        try:
            _index = self.__index(index)
            if not isinstance(value, _ImgColor):
                raise TypeError("Value must be an ImgColor.")
            self.__colors[_index] = value
            return
        except TypeError as _e:
            e = _e
        except ValueError as _e:
            e = _e
        raise e
    
    def __iter__(self):
        _len = len(self.__colors)
        _i = 0
        while _i < _len:
            yield _cast(_ImgColor, self.__colors[_i])
            _i += 1

    #endregion

    #region helper methods

    def __setsize(self, size:int):
        if size < 0 or size > IMGPALETTE_MAX:
            raise ValueError("size must be >= 0 and <= IMGPALETTE_MAX.")
        self.__colors = _np.full(size, _ImgColor(), dtype = object)
    
    def __index(self, index):
        _index = _ErrorUtil.valid_int(index)
        if _index < 0 or _index >= len(self.__colors):
            raise ValueError("index is out of range.")
        return _index

    #endregion

    #region methods

    def format(self, size:int = IMGPALETTE_MAX):
        """
        Formats the palette\n
        NOTE: All existing data will be lost
        
        :param size:
            Number of colors in palette
        :raise ValueError:
            size is less than 0 or greater than IMGPALETTE_MAX
        """
        try:
            self.__setsize(size)
            return
        except ValueError as _e:
            e = _e
        raise e

    def resize(self, size:int):
        """
        Resizes the palette
        
        :param size:
            Number of colors in palette
        :raise ValueError:
            size is less than 0 or greater than IMGPALETTE_MAX
        """
        try:
            prev_colors = self.__colors
            self.__setsize(size)
            for _i in range(min(len(self.__colors), len(prev_colors))):
                self.__colors[_i] = prev_colors[_i]
            return
        except ValueError as _e:
            e = _e
        raise e

    #endregion