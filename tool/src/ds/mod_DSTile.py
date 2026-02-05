__all__ = [\
    'DSTile',\
    'DSTILE_W',\
    'DSTILE_H']

import numpy as _np

from typing import\
    cast as _cast

from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil

__DSTILE_DIM = 8

DSTILE_W = __DSTILE_DIM
"""
Width of a DS tile
"""

DSTILE_H = __DSTILE_DIM
"""
Height of a DS tile
"""

class DSTile:
    """
    Represents a DS tile
    """

    #region init

    def __init__(self):
        """
        Initializer for DSTile
        """
        self.__array = _np.zeros(DSTILE_W * DSTILE_H, dtype = _np.uint8)

    #endregion

    #region operators

    def __len__(self):
        return len(self.__array)

    def __getitem__(self, index):
        try:
            _index = self.__index(index)
            return _cast(_np.uint8, self.__array[_index])
        except TypeError as _e:
            e = _e
        except IndexError as _e:
            e = _e
        raise e

    def __setitem__(self, index, value):
        try:
            _index = self.__index(index)
            _value = self._validatepixel(value)
            self.__array[_index] = _value
            return
        except TypeError as _e:
            e = _e
        except IndexError as _e:
            e = _e
        raise e

    def __iter__(self):
        i = 0
        l = len(self.__array)
        while i < l:
            yield _cast(_np.uint8, self.__array[i])
            i += 1

    #endregion

    #region helper methods
    
    def __index(self, key):
        if not isinstance(key, tuple):
            index = _ErrorUtil.valid_int(key)
            if index < 0 or index >= len(self.__array):
                raise IndexError("Index is out of range.")
            return index
        if not len(key) == 2:
            raise IndexError("Tuple must contain exactly 2 integers.")
        x = _ErrorUtil.valid_int(key[0])
        y = _ErrorUtil.valid_int(key[1])
        if x < 0 or x >= DSTILE_W:
            raise IndexError("X-coordinate is out of range.")
        if y < 0 or y >= DSTILE_H:
            raise IndexError("Y-coordinate is out of range.")
        return x + y * DSTILE_W
    
    def _validatepixel(self, value):
        """
        :raise TypeError:
            value is not of a valid type
        """
        try: return _np.uint8(value)
        except: pass
        raise TypeError(f"{value} is not a valid 8-bit unsigned integer.")

    #endregion