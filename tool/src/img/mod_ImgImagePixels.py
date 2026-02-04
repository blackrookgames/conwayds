__all__ = [\
    'ImgImagePixels',]

from typing import\
    Generic as _Generic,\
    TypeVar as _TypeVar

from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil

T = _TypeVar("T")

class ImgImagePixels(_Generic[T]):
    """
    Represents pixel data
    """

    #region init

    def __init__(self, width:int, height:int):
        """
        Initializer for ImgImagePixels

        :param width:
            Image width
        :param height:
            Image height
        :raise ValueError:
            width is less than 0\n
            or\n
            height is less than 0
        """
        if width < 0:
            raise ValueError("width must be greater than or equal to zero.")
        if height < 0:
            raise ValueError("height must be greater than or equal to zero.")
        self.__width = width
        self.__height = height
        self.__size = self.__width * self.__height
    
    #endregion

    #region operators

    def __len__(self):
        return self.__size
    
    def __iter__(self):
        _i = 0
        while _i < self.__size:
            yield self._getpixel(_i)
            _i += 1
    
    def __getitem__(self, key):
        try:
            _index = self.__index(key)
            return self._getpixel(_index)
        except TypeError as _e:
            e = _e
        except ValueError as _e:
            e = _e
        raise e
    
    def __setitem__(self, key, value):
        try:
            _index = self.__index(key)
            _value = self._validatepixel(value)
            self._setpixel(_index, _value)
            return
        except TypeError as _e:
            e = _e
        except ValueError as _e:
            e = _e
        raise e
    
    #endregion

    #region properties

    @property
    def width(self):
        """
        Image width
        """
        return self.__width

    @property
    def height(self):
        """
        Image height
        """
        return self.__height

    @property
    def size(self):
        """
        Size (width * height)
        """
        return self.__size
    
    #endregion

    #region helper methods
    
    def __index(self, key):
        if not isinstance(key, tuple):
            index = _ErrorUtil.valid_int(key)
            if index < 0 or index >= self.__size:
                raise ValueError("Index is out of range.")
            return index
        if not len(key) == 2:
            raise ValueError("Tuple must contain exactly 2 integers.")
        x = _ErrorUtil.valid_int(key[0])
        y = _ErrorUtil.valid_int(key[1])
        if x < 0 or x >= self.__width:
            raise ValueError("X-coordinate is out of range.")
        if y < 0 or y >= self.__height:
            raise ValueError("Y-coordinate is out of range.")
        return x + y * self.__width

    def _validatepixel(self, value) -> T:
        """
        :raise TypeError:
            value is not of a valid type
        """
        raise NotImplementedError("_getpixel has not yet been implemented.")

    def _getpixel(self, index:int) -> T:
        """
        Assume index is in range
        """
        raise NotImplementedError("_getpixel has not yet been implemented.")

    def _setpixel(self, index:int, value:T) -> None:
        """
        Assume index is in range
        """
        raise NotImplementedError("_setpixel has not yet been implemented.")

    #endregion