__all__ = [\
    'ImgPalette',]

import numpy as _np

from typing import\
    cast as _cast

from .mod_ImgColor import\
    ImgColor as _ImgColor

class ImgPalette:
    """
    Represents an image
    """

    #region init

    def __init__(self,\
            size:int):
        """
        Initializer for ImgPalette
        
        :param size:
            Number of colors
        :raise ValueError:
            size is less than zero
        """
        try:
            self.__setsize(size)
            return
        except ValueError as _e:
            e = _e
        raise e

    #endregion

    #region operators

    def __len__(self):
        return len(self.__colors)
    
    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError(f"{type(index)} is not supported as an index.")
        if index < 0 or index >= len(self.__colors):
            raise ValueError("index is out of range.")
        return _cast(_ImgColor, self.__colors[index])
    
    def __setitem__(self, index, value):
        if not isinstance(index, int):
            raise TypeError(f"{type(index)} is not supported as an index.")
        if not isinstance(value, _ImgColor):
            raise TypeError(f"{type(value)} is not supported as a value.")
        if index < 0 or index >= len(self.__colors):
            raise ValueError("index is out of range.")
        self.__colors[index] = value

    def __iter__(self):
        l = len(self.__colors)
        i = 0
        while i < l:
            yield _cast(_ImgColor, self.__colors[i])
            i += 1

    #endregion

    #region helper methods

    def __setsize(self,\
            size:int):
        if size < 0:
            raise ValueError("size must be greater than or equal to zero.")
        self.__colors = _np.full(size, _ImgColor(), dtype = object)

    #endregion

    #region methods

    def resize(self,\
            size:int,\
            preserve:bool = False):
        """
        Resizes the image
        
        :param size:
            Number of colors
        :param preserve:
            Whether or not to preserve existing colors
        :raise ValueError:
            size is less than zero
        """
        try:
            prev_colors = self.__colors
            # Set size
            self.__setsize(size)
            # Preserve (if requested)
            if preserve:
                for i in range(min(len(self.__colors), len(prev_colors))):
                    self.__colors[i] = prev_colors[i]
            # Success!!!
            return
        except ValueError as _e:
            e = _e
        raise e

    #endregion