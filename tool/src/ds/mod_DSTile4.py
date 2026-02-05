__all__ = [\
    'DSTile4',]

import numpy as _np
from .mod_DSTile import\
    DSTile as _DSTile

class DSTile4(_DSTile):
    """
    Represents a DS 4bpp tile
    """

    #region init

    def __init__(self):
        """
        Initializer for DSTile4
        """
        super().__init__()

    #endregion

    #region helper methods
    
    def _validatepixel(self, value):
        try:
            _value = _np.uint8(value)
            if (_value & 0b1111) == _value:
                return _value
        except: pass
        raise TypeError(f"{value} is not a valid 4-bit unsigned integer.")

    #endregion