__all__ = [ 'DictUtil' ]

from typing import\
    TypeVar as _TypeVar

from .mod_Ptr import Ptr as _Ptr

TKey = _TypeVar('TKey')
TValue = _TypeVar('TValue')

class DictUtil:
    """
    Utility for dictionary-related operations
    """

    #region findkey

    @classmethod
    def findkey(cls, d:dict[TKey, TValue], value:TValue):
        """
        Searches the dictionary for a key with the specified value\n
        If the value is not found, an ValueError is raised.

        :param d:
            Dictionary to search
        :param value:
            Value to search for
        :param result:
            Where to store the found key
        :return:
            Key with the specified value
        :raise ValueError:
            Value could not be found
        """
        for _key, _val in d.items():
            if _val == value: return _key
        raise ValueError("Could not find the specified value.")

    @classmethod
    def tryfindkey(cls, d:dict[TKey, TValue], value:TValue, result:None|_Ptr[TKey] = None):
        """
        Searches the dictionary for a key with the specified value

        :param d:
            Dictionary to search
        :param value:
            Value to search for
        :param result:
            Where to store the found key
        :return:
            Whether or not the key was found
        """
        for _key, _val in d.items():
            if _val != value: continue
            if result is not None: result.value = _key
            return True
        return False

    #endregion