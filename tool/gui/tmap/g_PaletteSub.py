__all__ = [\
    'PALETTESUB_SIZE',\
    'PaletteSub',]

PALETTESUB_SIZE = 16
"""
Number of colors within a sub-palette
"""

class PaletteSub:
    """
    Represents a sub-palette
    """

    #region init

    def __init__(self):
        """
        Initializer for PaletteSub
        """
        self.__data:list[str] = ["#000000" for _i in range(PALETTESUB_SIZE)]

    #endregion

    #region operators

    def __len__(self):
        return PALETTESUB_SIZE

    def __getitem__(self, index:int):
        """
        Gets the color at the specified index

        :param index:
            Index of color
        :returns:
            String representing the hex value of the color
        :raise IndexError:
            Index is out of range
        """
        try:
            return self.__data[index]
        except Exception as _e:
            if index < 0 or index >= PALETTESUB_SIZE:
                e = IndexError("Index is out of range.")
            else: e = _e
        raise e

    def __setitem__(self, index:int, value:str):
        """
        Sets the color at the specified index
        
        :param index:
            Index of color
        :param value:
            String representing the hex value of the color
        :raise IndexError:
            Index is out of range
        :raise ValueError:
            value is not valid
        """
        try:
            # Ensure value is valid
            _bad = False
            if len(value) == 7 and value[0] == '#':
                for _i in range(1, len(value)):
                    _c = ord(value[_i])
                    if _c >= 0x30 and _c <= 0x39: continue
                    if _c >= 0x41 and _c <= 0x46: continue
                    if _c >= 0x61 and _c <= 0x66: continue
                    _bad = True
                    break
            else: _bad = True
            if _bad: raise ValueError(f"\"{value}\" is not a valid color value.")
            # Set
            self.__data[index] = value
            # Success!!!
            return
        except Exception as _e:
            if index < 0 or index >= PALETTESUB_SIZE:
                e = IndexError("Index is out of range.")
            else: e = _e
        raise e

    #endregion