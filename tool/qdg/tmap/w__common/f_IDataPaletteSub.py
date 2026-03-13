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

    def __init__(self, colors:_Iterable[tuple[int, int, int, int]]):
        """
        Initializer for IDataPaletteSub

        :param colors:
            Palette colors
        """
        self.__data:list[tuple[int, int, int, int]] = []
        # Get colors
        for _color in colors:
            if len(self.__data) == IDATAPALETTESUB_SIZE:
                break
            self.__data.append(self.__fix_color(_color))
        # Pad colors
        while len(self.__data) < IDATAPALETTESUB_SIZE:
            self.__data.append((0, 0, 0, 255))

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
    def __fix_color(cls, value:tuple[int, int, int, int]):
        r, g, b, a = value
        return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)), max(0, min(255, a)))

    #endregion