__all__ = [\
    'IDATAPALETTESUB_SIZE',\
    'IDataPaletteSub',]

from collections.abc import\
    Iterable as _Iterable

IDATAPALETTESUB_SIZE = 16
"""
Number of colors within a sub-palette
"""

class IDataPaletteSub:
    """
    Immutable object representing sub-palette data
    """

    #region init

    def __init__(self, colors:_Iterable[str]):
        """
        Initializer for IDataPaletteSub

        :param colors:
            Palette colors (ex: '#FF8040', '#80FF80')
        :raise ValueError:
            One or more colors are invalid
        """
        self.__data:list[str] = []
        # Get colors
        for _color in colors:
            if len(self.__data) == IDATAPALETTESUB_SIZE:
                break
            self.__data.append(self.__valid_color(_color))
        # Pad colors
        while len(self.__data) < IDATAPALETTESUB_SIZE:
            self.__data.append("#000000")

    #endregion

    #region operators

    def __len__(self):
        return IDATAPALETTESUB_SIZE

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
            if index < 0 or index >= IDATAPALETTESUB_SIZE:
                e = IndexError("Index is out of range.")
            else: e = _e
        raise e

    #endregion

    #region helper methods

    @classmethod
    def __valid_color(cls, value:str):
        def _invalid():
            nonlocal value
            return ValueError(f"\"{value}\" is not a valid color value.")
        # Valid size?
        if len(value) != 7: raise _invalid()
        # Valid prefix?
        if value[0] != '#': raise _invalid()
        # Valid digits
        for _i in range(1, len(value)):
            _c = ord(value[_i])
            if _c >= 0x30 and _c <= 0x39: continue
            if _c >= 0x41 and _c <= 0x46: continue
            if _c >= 0x61 and _c <= 0x66: continue
            raise _invalid()
        # Success!!!
        return value

    #endregion