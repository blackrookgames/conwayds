__all__ = [\
    'ImgImageRGBAPixels',]

import numpy as _np

from typing import\
    cast as _cast

from .mod_ImgColor import\
    ImgColor as _ImgColor
from .mod_ImgImagePixels import\
    ImgImagePixels as _ImgImagePixels

class ImgImageRGBAPixels(_ImgImagePixels[_ImgColor]):
    """
    Represents RGBA pixel data
    """

    #region init

    def __init__(self, width:int, height:int):
        """
        Initializer for ImgImageRGBAPixels

        :param width:
            Image width
        :param height:
            Image height
        :raise ValueError:
            width is less than 0\n
            or\n
            height is less than 0
        """
        super().__init__(width, height)
        self.__pixels = _np.full(self.size, _ImgColor(), dtype = object)
    
    #endregion

    #region helper methods
    
    def _validatepixel(self, value):
        if isinstance(value, _ImgColor):
            return value
        raise TypeError("Pixel value must be an ImgColor.")

    def _getpixel(self, index:int):
        return _cast(_ImgColor, self.__pixels[index])

    def _setpixel(self, index:int, value:_ImgColor):
        self.__pixels[index] = value

    #endregion