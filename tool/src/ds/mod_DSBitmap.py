__all__ = [\
    'DSBitmap']

import numpy as _np
import numpy.typing as _npt

from typing import\
    cast as _cast,\
    Generic as _Generic,\
    TypeVar as _TypeVar

from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil

T = _TypeVar('T')

class DSBitmap(_Generic[T]):
    """
    Represents a DS bitmap
    """

    #region init

    def __init__(self, width:int, height:int):
        """
        Initializer for DSBitmap

        :param width:
            Bitmap width
        :param height:
            Bitmap height
        :raise ValueError:
            width is less than or equal to zero\n
            or\n
            height is less than or equal to zero
        """
        self.__setsize(width, height)
        
    #endregion

    #region operators

    def __len__(self):
        return len(self.__pixels)

    def __getitem__(self, index):
        try:
            _index = self.__index(index)
            return _cast(T, self.__pixels[_index])
        except TypeError as _e:
            e = _e
        except IndexError as _e:
            e = _e
        raise e

    def __setitem__(self, index, value):
        try:
            _index = self.__index(index)
            _value = self._validate(value)
            self.__pixels[_index] = _value
            return
        except TypeError as _e:
            e = _e
        except IndexError as _e:
            e = _e
        raise e

    def __iter__(self):
        i = 0
        l = len(self.__pixels)
        while i < l:
            yield _cast(T, self.__pixels[i])
            i += 1

    #endregion

    #region properties

    @property
    def width(self):
        """
        Bitmap width
        """
        return self.__width

    @property
    def height(self):
        """
        Bitmap height
        """
        return self.__height

    #endregion

    #region helper methods

    def _createarray(self, width:int, height:int) -> _npt.NDArray:
        """
        Assume
        - width > 0
        - height > 0
        """
        raise NotImplementedError("_createarray has not yet been implemented.")
    
    def _validate(self, raw:object) -> T:
        """
        :raises TypeError:
            raw is not of a valid type
        """
        raise NotImplementedError("_validate has not yet been implemented.")

    def __setsize(self, width:int, height:int):
        if width <= 0: raise ValueError("width be must greater than zero.")
        if height <= 0: raise ValueError("height be must greater than zero.")
        self.__width = width
        self.__height = height
        self.__pixels = self._createarray(self.__width, self.__height)
    
    def __index(self, key):
        if not isinstance(key, tuple):
            index = _ErrorUtil.valid_int(key)
            if index < 0 or index >= len(self.__pixels):
                raise IndexError("Index is out of range.")
            return index
        if not len(key) == 2:
            raise IndexError("Tuple must contain exactly 2 integers.")
        x = _ErrorUtil.valid_int(key[0])
        y = _ErrorUtil.valid_int(key[1])
        if x < 0 or x >= self.__width:
            raise IndexError("X-coordinate is out of range.")
        if y < 0 or y >= self.__height:
            raise IndexError("Y-coordinate is out of range.")
        return x + y * self.__width

    #endregion

    #region methods

    def setsize(self, width:int, height:int):
        """
        Sets the size of the bitmap\n
        NOTE: All existing data will be lost. To preserve data, use resize(width, height) instead.

        :param width:
            Bitmap width
        :param height:
            Bitmap height
        :raise ValueError:
            width is less than or equal to 0\n
            or\n
            height is less than or equal to 0
        """
        try:
            self.__setsize(width, height)
            return
        except ValueError as _e:
            e = _e
        raise e
    
    def resize(self, width:int, height:int):
        """
        Resizes the image
        
        :param width:
            Image width
        :param height:
            Image height
        :raise ValueError:
            width is less than or equal to 0\n
            or\n
            height is less than or equal to 0
        """
        try:
            prev_width = self.__width
            prev_height = self.__height
            prev_pixels = self.__pixels
            # Set new size
            self.__setsize(width, height)
            # Set pixels
            _min_w = min(prev_width, self.__width)
            _min_h = min(prev_height, self.__height)
            for _y in range(_min_h):
                _iindex = _y * prev_width
                _oindex = _y * self.__width
                for _x in range(_min_w):
                    self.__pixels[_oindex] = prev_pixels[_iindex]
                    _iindex += 1
                    _oindex += 1
            # Success!!!
            return
        except ValueError as _e:
            e = _e
        raise e

    #endregion