__all__ = [\
    'Ptr',]

from typing import\
    Generic as _Generic,\
    TypeVar as _TypeVar

T = _TypeVar('T')

class Ptr(_Generic[T]):
    """
    Represents a "pointer" to a value
    """

    #region init

    def __init__(self, init:T):
        """
        Initializer for Ptr

        :param init: Initial value
        """
        self.__value = init

    #endregion

    #region properties

    @property
    def value(self):
        """ Value """
        return self.__value
    @value.setter
    def value(self, value:T):
        self.__value = value

    #endregion