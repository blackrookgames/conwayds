__all__ = [\
    'DSTileset',]

from typing import\
    Generic as _Generic,\
    TypeVar as _TypeVar

from .mod_DSTile import\
    DSTile as _DSTile
from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil

T = _TypeVar("T", bound = _DSTile)

class DSTileset(_Generic[T]):
    """
    Represents a DS tileset
    """

    #region init

    def __init__(self):
        """
        Initializer for DSTileset
        """
        self.__tiles:list[T] = []

    #endregion

    #region operators

    def __len__(self):
        return len(self.__tiles)

    def __getitem__(self, index) -> T:
        try:
            _index = self.__index(index)
            return self.__tiles[_index]
        except TypeError as _e:
            e = _e
        except IndexError as _e:
            e = _e
        raise e

    def __setitem__(self, index, value):
        try:
            _index = self.__index(index)
            _value = self._validatetile(value)
            self.__tiles[_index] = _value
            return
        except TypeError as _e:
            e = _e
        except IndexError as _e:
            e = _e
        raise e

    def __iter__(self):
        for tile in self.__tiles:
            yield tile

    #endregion

    #region helper methods

    def __index(self, index):
        _index = _ErrorUtil.valid_int(index)
        if _index < 0 or _index >= len(self.__tiles):
            raise IndexError(f"Index is out of range.")
        return _index
    
    def _validatetile(self, tile) -> T:
        """
        :raise TypeError:
            tile is not of a valid type
        """
        raise NotImplementedError("_validatetile has not yet been implemented.")

    #endregion

    #region methods
    
    def add(self, tile:T):
        """
        Adds the specified tile to the end of the tileset
        
        :param tile:
            Tile to add
        """
        self.__tiles.append(tile)
    
    def insert(self, index:int, tile:T):
        """
        Inserts the specified tile into the tileset at the specified index
        
        :param index:
            Index to insert tile
        :param tile:
            Tile to add
        :raise IndexError:
            index is out of range
        """
        if index < 0 or index > len(self.__tiles):
            raise IndexError("index is out of range.")
        self.__tiles.insert(index, tile)
    
    def removeat(self, index:int):
        """
        Removes the tile at the specified index
        
        :param index:
            Index of tile to remove
        :raise IndexError:
            index is out of range
        """
        if index < 0 or index >= len(self.__tiles):
            raise IndexError("index is out of range.")
        self.__tiles.pop(index)

    def clear(self):
        """
        Removes all tiles from the tileset
        """
        self.__tiles.clear()

    #endregion