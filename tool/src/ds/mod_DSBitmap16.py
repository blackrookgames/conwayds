__all__ = [\
    'DSBitmap16']

import numpy as _np

from typing import\
    SupportsInt as _SupportsInt

from .mod_DSBitmap import\
    DSBitmap as _DSBitmap
from .mod_DSColor import\
    DSColor as _DSColor

class DSBitmap16(_DSBitmap[_DSColor]):
    """
    Represents an 16bpp DS bitmap
    """

    #region init

    def __init__(self, width:int = 1, height:int = 1):
        """
        Initializer for DSBitmap16

        :param width:
            Bitmap width
        :param height:
            Bitmap height
        :raise ValueError:
            width is less than or equal to zero\n
            or\n
            height is less than or equal to zero
        """
        super().__init__(width, height)
        
    #endregion

    #region helper methods

    def _createarray(self, width:int, height:int):
        return _np.full(width * height, _DSColor(0x0000), dtype = object)
    
    def _validate(self, raw:object):
        if isinstance(raw, _DSColor): return raw
        raise TypeError(f"{raw} is not a DSColor.")

    #endregion