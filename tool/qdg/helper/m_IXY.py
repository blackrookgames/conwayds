__all__ = [\
    'IXY',\
    'IXY_ZERO',\
    'IXY_LEFT',\
    'IXY_RIGHT',\
    'IXY_UP',\
    'IXY_DOWN',]

class IXY:
    """ Represents XY integer coordinates """

    #region init

    def __init__(self, x:int = 0, y:int = 0):
        """
        Initializer for IXY

        :param x: X-coordinate
        :param y: Y-coordinate
        """
        self.__x = x
        self.__y = y

    #endregion

    #region operators

    def __repr__(self):
        return f"IXY(x = {self.__x}, y = {self.__y})"
    
    def __str__(self):
        return f"({self.__x}, {self.__y})"
    
    def __eq__(self, other:object):
        return self.__eq(other)
    
    def __ne__(self, other:object):
        return not self.__eq(other)
    
    def __hash__(self):
        return self.__x
    
    def __add__(self, other:'IXY|int|tuple[int, int]'):
        if isinstance(other, int): return self.__add(other, other)
        if isinstance(other, tuple): return self.__add(other[0], other[1])
        return self.__add(other.__x, other.__y)
    
    def __sub__(self, other:'IXY|int|tuple[int, int]'):
        if isinstance(other, int): return self.__sub(other, other)
        if isinstance(other, tuple): return self.__sub(other[0], other[1])
        return self.__sub(other.__x, other.__y)
    
    def __mul__(self, other:'IXY|int|tuple[int, int]'):
        if isinstance(other, int): return self.__mul(other, other)
        if isinstance(other, tuple): return self.__mul(other[0], other[1])
        return self.__mul(other.__x, other.__y)
    
    def __floordiv__(self, other:'IXY|int|tuple[int, int]'):
        if isinstance(other, int): return self.__floordiv(other, other)
        if isinstance(other, tuple): return self.__floordiv(other[0], other[1])
        return self.__floordiv(other.__x, other.__y)
    
    def __mod__(self, other:'IXY|int|tuple[int, int]'):
        if isinstance(other, int): return self.__mod(other, other)
        if isinstance(other, tuple): return self.__mod(other[0], other[1])
        return self.__mod(other.__x, other.__y)
    
    def __pow__(self, other:'IXY|int|tuple[int, int]'):
        if isinstance(other, int): return self.__pow(other, other)
        if isinstance(other, tuple): return self.__pow(other[0], other[1])
        return self.__pow(other.__x, other.__y)

    #endregion

    #region properties

    @property
    def x(self):
        """ X-coordinate """
        return self.__x
    
    @property
    def y(self):
        """ Y-coordinate """
        return self.__y

    #endregion

    #region helper methods

    def __eq(self, other:object):
        if not isinstance(other, IXY): return False
        return self.__x == other.__x and self.__y == other.__y

    def __add(self, other_x:int, other_y:int):
        return self.__class__(self.__x + other_x, self.__y + other_y)

    def __sub(self, other_x:int, other_y:int):
        return self.__class__(self.__x - other_x, self.__y - other_y)

    def __mul(self, other_x:int, other_y:int):
        return self.__class__(self.__x * other_x, self.__y * other_y)

    def __floordiv(self, other_x:int, other_y:int):
        return self.__class__(self.__x // other_x, self.__y // other_y)

    def __mod(self, other_x:int, other_y:int):
        return self.__class__(self.__x % other_x, self.__y % other_y)

    def __pow(self, other_x:int, other_y:int):
        return self.__class__(self.__x ** other_x, self.__y ** other_y)

    #endregion

#region const

IXY_ZERO = IXY(x = 0, y = 0)
IXY_LEFT = IXY(x = -1, y = 0)
IXY_RIGHT = IXY(x = 1, y = 0)
IXY_UP = IXY(x = 0, y = -1)
IXY_DOWN = IXY(x = 0, y = 1)

#endregion