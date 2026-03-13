__all__ = ['_ViewMap']

import numpy as _np

from typing import\
    TYPE_CHECKING as _TYPE_CHECKING

if _TYPE_CHECKING:
    from .internal_View import _View

class _ViewMap:
    """
    Represents a tilemap within a tilemap view
    """

    #region init

    def __init__(self, view:'_View', width:int, height:int):
        """
        Initializer for ViewMap

        :param view: Owning view
        :param width: Width (must be >= 1)
        :param height: Height (must be >= 1)

        :raise ValueError:
            width is less than 1\n
            or\n
            height is less than 1
        """
        view._raise_if_init()
        self.__view = view
        self._format(width, height)

    #endregion

    #region operators

    def __len__(self): return len(self.__data)

    def __getitem__(self, key:int|tuple[int, int]) -> _np.uint16:
        """
        Gets the cell at the specified coordinates

        :raise IndexError: Coordinates are out of range
        """
        return self.__data[self.__index(key)]

    def __setitem__(self, key:int|tuple[int, int], value:_np.uint16):
        """
        Sets the cell at the specified coordinates

        :raise IndexError: Coordinates are out of range
        """
        index = self.__index(key)
        # Make sure value is being changed
        oldvalue = self.__data[index]
        if oldvalue == value: return
        # Set value
        self.__data[index] = value
        # Tell view
        self.__view._map_tilechanged(index % self.__width, index // self.__width, oldvalue, value)

    #endregion

    #region properties

    @property
    def width(self):
        """ Width (in data) """
        return self.__width
    
    @property
    def height(self):
        """ Height (in data) """
        return self.__height

    #endregion

    #region helper methods

    def _format(self, width:int, height:int):
        """
        Also accessed by _View
        """
        # Error check
        if width < 1:
            raise ValueError("Width must be greater than or equal to 1.")
        if height < 1:
            raise ValueError("Height must be greater than or equal to 1.")
        # Format
        self.__width = width
        self.__height = height
        self.__data = _np.zeros(self.__width * self.__height, dtype = _np.uint16)
    
    def __index(self, key:int|tuple[int, int]):
        if isinstance(key, int):
            if key < 0 or key >= len(self.__data):
                raise IndexError("Index is out of range.")
            return key
        else:
            x, y = key
            if x < 0 or x >= self.__width:
                raise IndexError("X-coordinate is out of range.")
            if y < 0 or y >= self.__height:
                raise IndexError("Y-coordinate is out of range.")
            return x + y * self.__width

    #endregion

    #region methods

    def format(self, width:int = 1, height:int = 1):
        """
        Formats the tilemap

        :param width: Width (must be >= 1)
        :param height: Height (must be >= 1)

        :raise ValueError:
            width is less than 1\n
            or\n
            height is less than 1
        """
        # Format
        self._format(width, height)
        # Tell view
        self.__view._map_formatted()

    #endregion