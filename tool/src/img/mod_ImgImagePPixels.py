__all__ = [\
    'ImgImagePPixels',]

import numpy as _np

from typing import\
    cast as _cast

from .mod_ImgImagePixels import\
    ImgImagePixels as _ImgImagePixels

class ImgImagePPixels(_ImgImagePixels[_np.uint8]):
    """
    Represents palette pixel data
    """

    #region init

    def __init__(self, width:int, height:int):
        """
        Initializer for ImgImagePPixels

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
        self.__pixels = _np.zeros(self.size, dtype = _np.uint8)
    
    #endregion

    #region helper methods
    
    def _validatepixel(self, value):
        try: return _np.uint8(value)
        except: pass
        raise TypeError("Pixel value must be an 8-bit unsigned integer.")

    def _getpixel(self, index:int):
        return _cast(_np.uint8, self.__pixels[index])

    def _setpixel(self, index:int, value:_np.uint8):
        self.__pixels[index] = value

    #endregion