__all__ = [\
    'DSBitmap8']

import numpy as _np

from typing import\
    SupportsInt as _SupportsInt

from .mod_DSBitmap import\
    DSBitmap as _DSBitmap

class DSBitmap8(_DSBitmap[_np.uint8]):
    """
    Represents an 8bpp DS bitmap
    """

    #region init

    def __init__(self, width:int = 1, height:int = 1):
        """
        Initializer for DSBitmap8

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
        return _np.zeros(width * height, dtype = _np.uint8)
    
    def _validate(self, raw:object):
        if isinstance(raw, _SupportsInt):
            try: return _np.uint8(raw)
            except: pass
        raise TypeError(f"{raw} is not a valid 8-bit unsigned integer.")

    #endregion