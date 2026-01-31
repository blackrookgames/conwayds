__all__ = [\
    'DSColor',\
    'DSCOLOR_MAX',\
    'DSCOLOR_BLACK',\
    'DSCOLOR_WHITE',\
    'DSCOLOR_RED',\
    'DSCOLOR_GREEN',\
    'DSCOLOR_BLUE',\
    'DSCOLOR_YELLOW',\
    'DSCOLOR_CYAN',\
    'DSCOLOR_MAGENTA',]

from numpy import\
    uint8 as _uint8,\
    uint16 as _uint16

DSCOLOR_MAX = 0x1F
"""
Maximum value for a single channel
"""

class DSColor:
    """
    Represents a 16-bit DS color
    """

    #region const

    __MASK = 0x1F
    __SHIFT_G = 5
    __SHIFT_B = 10
    __BIT_A = 1 << 15

    #endregion

    #region init

    def __init__(self, value:int|tuple[int, int, int]|tuple[int, int, int, bool]):
        """
        Initializer for DSColor

        :param value:
            Color value
        """
        if isinstance(value, tuple):
            # r
            self.__r = _uint8(min(DSCOLOR_MAX, value[0]))
            # g
            self.__g = _uint8(min(DSCOLOR_MAX, value[1]))
            # b
            self.__b = _uint8(min(DSCOLOR_MAX, value[2]))
            # a
            if len(value) == 4: self.__a = value[3]
            else: self.__a = True
        else:
            # r
            self.__r = _uint8(value & self.__MASK)
            # g
            self.__g = _uint8((value >> self.__SHIFT_G) & self.__MASK)
            # b
            self.__b = _uint8((value >> self.__SHIFT_B) & self.__MASK)
            # a
            self.__a = (value & self.__BIT_A) != 0

    #endregion

    #region operators

    def __repr__(self):
        return f"DSColor(({self.__r}, {self.__g}, {self.__b}, {self.__a}))"

    def __eq__(self, other):
        return self.__equals(other)
    
    def __ne__(self, other):
        return not self.__equals(other)
    
    def __hash__(self):
        return hash(self.to16())

    def __str__(self):
        return f"{self.__r}, {self.__g}, {self.__b}, {self.__a}"

    #endregion

    #region properties

    @property
    def r(self):
        """
        Red value
        """
        return self.__r

    @property
    def g(self):
        """
        Green value
        """
        return self.__g

    @property
    def b(self):
        """
        Blue value
        """
        return self.__b

    @property
    def a(self):
        """
        Alpha value
        """
        return self.__a

    #endregion

    #region helper methods

    def __equals(self, other):
        if not isinstance(other, DSColor):
            return False
        return self.__r == other.__r and\
            self.__g == other.__g and\
            self.__b == other.__b and\
            self.__a == other.__a
    
    #endregion

    #region methods

    def to16(self):
        """
        Converts the color to a 16-bit value
        """
        return \
            _uint16(self.__r) |\
            (_uint16(self.__g) << self.__SHIFT_G) |\
            (_uint16(self.__b) << self.__SHIFT_B) |\
            (self.__BIT_A if self.__a else 0)

    def to15(self):
        """
        Converts the color to a 15-bit value\n
        This is basically the same as to16() except alpha is not transferred
        """
        return \
            _uint16(self.__r) |\
            (_uint16(self.__g) << self.__SHIFT_G) |\
            (_uint16(self.__b) << self.__SHIFT_B)

    #endregion

DSCOLOR_BLACK = DSColor((0, 0, 0, ))
DSCOLOR_WHITE = DSColor((DSCOLOR_MAX, DSCOLOR_MAX, DSCOLOR_MAX, ))
DSCOLOR_RED = DSColor((DSCOLOR_MAX, 0, 0, ))
DSCOLOR_GREEN = DSColor((0, DSCOLOR_MAX, 0, ))
DSCOLOR_BLUE = DSColor((0, 0, DSCOLOR_MAX, ))
DSCOLOR_YELLOW = DSColor((DSCOLOR_MAX, DSCOLOR_MAX, 0, ))
DSCOLOR_CYAN = DSColor((0, DSCOLOR_MAX, DSCOLOR_MAX, ))
DSCOLOR_MAGENTA = DSColor((DSCOLOR_MAX, 0, DSCOLOR_MAX, ))