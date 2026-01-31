__all__ = [\
    'DSPalette',]

import numpy as _np
from .mod_DSColor import\
    DSColor as _DSColor
from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil

DSPALETTE_SIZE = 256
"""
Number of colors within a single palette
"""

class DSPalette:
    """
    Represents a DS color palette
    """

    #region init

    def __init__(self):
        """
        Initializer for DSPalette
        """
        self.__array = _np.full(DSPALETTE_SIZE, _DSColor(0))

    #endregion

    #region operators

    def __repr__(self):
        return f"SPalette(({self.__r}, {self.__g}, {self.__b}, {self.__a}))"
    
    def __len__(self):
        return len(self.__array)

    def __getitem__(self, index) -> _DSColor:
        try:
            return self.__array[self.__getindex(index)]
        except Exception as _e: e = _e
        raise e

    def __setitem__(self, index, value):
        try:
            self.__array[self.__getindex(index)] = value
            return
        except Exception as _e: e = _e
        raise e

    def __contains__(self, item):
        return item in self.__array

    def __iter__(self):
        i = 0
        l = len(self.__array)
        while i < l:
            yield self.__array[i]
            i += 1

    #endregion

    #region helper methods

    def __getindex(self, index):
        _index = _ErrorUtil.valid_int(index, param = 'index')
        if _index < 0 or _index >= len(self.__array):
            raise IndexError(f"index is out of range")
        return _index

    #endregion