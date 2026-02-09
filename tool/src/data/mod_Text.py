__all__ = [\
    'Text',]

import numpy as _np

from io import\
    StringIO as _StringIO
from typing import\
    cast as _cast

from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil
from .mod_TextChar import\
    TextChar as _TextChar

class Text:
    """
    Represents a text of characters
    """

    #region init

    def __init__(self, src, norowcol:bool = False):
        """
        Initializer for Text
        
        :param src:
            Source; this can be anything that can be converted to a string
        :param norowcol:
            If true, all row and column values will be set to 0
        :raise TypeError:
            src is not of a valid type
        """
        try:
            self.__chars = self.__getchars(src, norowcol)
            return
        except TypeError as _e:
            e = _e
        except IndexError as _e: # Do NOT add to documentatio
            e = _e
        raise e
        
    #endregion

    #region operators

    def __len__(self):
        return len(self.__chars)
    
    def __iter__(self):
        for _char in self.__chars:
            yield _cast(_TextChar, _char)
    
    def __getitem__(self, index):
        try:
            _index = _ErrorUtil.valid_int(index)
            if _index < 0 or _index >= len(self.__chars):
                raise IndexError("Index is out of range.")
            return _cast(_TextChar, self.__chars[_index])
        except TypeError as _e:
            e = _e
        except IndexError as _e:
            e = _e
        raise e

    def __repr__(self):
        return f"Text({self.__chars})"
    
    def __str__(self):
        with _StringIO() as strio:
            for _char in self.__chars:
                strio.write(str(_char))
            return strio.getvalue()
    
    def __eq__(self, other):
        return self.__equals(other)
    
    def __ne__(self, other):
        return not self.__equals(other)
    
    def __gt__(self, other):
        _cmp = self.compare(other)
        if _cmp is None: return False
        return _cmp > 0
    
    def __ge__(self, other):
        _cmp = self.compare(other)
        if _cmp is None: return False
        return _cmp >= 0
    
    def __lt__(self, other):
        _cmp = self.compare(other)
        if _cmp is None: return False
        return _cmp < 0
    
    def __le__(self, other):
        _cmp = self.compare(other)
        if _cmp is None: return False
        return _cmp <= 0
    
    def __hash__(self):
        return len(self.__chars)
    
    def __add__(self, other):
        if isinstance(other, Text) or isinstance(other, _TextChar):
            return Text((self, other))
        return NotImplemented

    #endregion

    #region helper methods

    @classmethod
    def __getchars_fromstr(cls, src):
        string = _ErrorUtil.valid_str(src)
        chars = _np.empty(len(string), dtype = object)
        _row = 1
        _col = 1
        for _i in range(len(string)):
            # Set character
            _ord = ord(string[_i])
            chars[_i] = _TextChar(_ord, _row, _col)
            # Determine next row and column
            if _ord == 0x0A:
                _row += 1
                _col = 1
            else:
                _col += 1
        return chars

    @classmethod
    def __getchars(cls, src, norowcol:bool):
        def _chrval(_chr:_TextChar):
            if norowcol: return _chr
            return _TextChar(_chr.ord, 0, 0)
        # Check if source is a text
        if isinstance(src, Text):
            if not norowcol:
                return src.__chars
            chars = _np.empty(len(src.__chars), dtype = object)
            for _i in range(len(src.__chars)):
                _char = _cast(_TextChar, src.__chars[_i])
                chars[_i] = _TextChar(_char.ord, 0, 0)
            return chars
        # Check if source is a list
        if isinstance(src, list):
            # Determine length
            length = 0
            for _item in src:
                if isinstance(_item, _TextChar):
                    length += 1
                elif isinstance(_item, Text):
                    length += len(_item.__chars)
            # Create array
            chars = _np.empty(length, dtype = object)
            # Add characters
            _i = 0
            for _item in src:
                if isinstance(_item, _TextChar):
                    chars[_i] = _chrval(_item)
                    _i += 1
                elif isinstance(_item, Text):
                    for _c in _item.__chars:
                        chars[_i] = _chrval(_c)
                        _i += 1
            return chars
        # Check if source is a non-tuple
        if not isinstance(src, tuple):
            return cls.__getchars_fromstr(src)
        # Check if source is a tuple with Text, int, int
        if len(src) == 3:
            _text = src[0]
            _beg = src[1]
            _end = src[2]
            if isinstance(_text, Text) and isinstance(_beg, int) and isinstance(_end, int):
                if _beg < 0 or _beg > len(_text.__chars):
                    raise IndexError("Start index is out of range.")
                if _end < 0 or _end > len(_text.__chars):
                    raise IndexError("Stop index is out of range.")
                if _beg > _end:
                    raise IndexError("Start index must be less than or equal to stop index.")
                chars = _np.empty(_end - _beg, dtype = object)
                for _i in range(len(chars)):
                    chars[_i] = _chrval(_text.__chars[_beg + _i])
                return chars
        # Prepare to concatenate multiple texts
        count = 0
        for _item in src:
            if isinstance(_item, Text):
                count += len(_item)
            elif isinstance(_item, _TextChar):
                count += 1
            else:
                raise TypeError("Tuples are not supported sources.")
        # Concatenate texts
        chars = _np.empty(count, dtype = object)
        _i = 0
        for _item in src:
            if isinstance(_item, Text):
                for _char in _item.__chars:
                    chars[_i] = _chrval(_char)
                    _i += 1
            else:
                chars[_i] = _chrval(_cast(_TextChar, _item))
                _i += 1
        return chars

    def __equ(self, indexedother):
        if len(self.__chars) != len(indexedother):
            return False
        for _i in range(len(self.__chars)):
            if self.__chars[_i] != indexedother[_i]:
                return False
        return True
    
    def __cmp(self, indexedother):
        # Compare length
        lencmp = len(self.__chars) - len(indexedother)
        minlen = len(self.__chars) if (lencmp < 0) else len(indexedother)
        # Compare characters
        for _i in range(minlen):
            _cmp = _cast(_TextChar, self.__chars[_i]).compare(indexedother[_i])
            if _cmp != 0: return _cmp
        # Return length result
        return lencmp

    def __equals(self, other):
        if isinstance(other, Text) or isinstance(other, str):
            return self.__equ(other)
        return False

    #endregion

    #region methods
    
    def compare(self, other):
        """
        Compares the value of the current object with the value of another object
        
        :param other:
            Other object
        :return:
            lt 0: Current object is less than other object\n
            eq 0: Current object is equal to other object\n
            gt 0: Current object is greater than other object\n
            None: Comparison cannot be made
        """
        if isinstance(other, Text) or isinstance(other, str):
            return self.__cmp(other)
        return None
    
    def sub(self, beg:None|int = None, end:None|int = None):
        """
        Creates a subtext

        :param beg:
            Start index
        :param end:
            End index
        :return:
            Created subtext
        :raise IndexError:
            Indexes are out of range
        """
        def _valid_int(_index:int):
            if _index < 0:
                _index += len(self.__chars)
            return _index
        try:
            # beg
            if beg is None: _beg = 0
            else: _beg = _valid_int(beg)
            # end
            if end is None: _end = len(self.__chars)
            else: _end = _valid_int(end)
            # Create text
            return Text((self, _beg, _end))
        except TypeError as _e:
            e = _e
        except IndexError as _e:
            e = _e
        raise e

    #endregion
    