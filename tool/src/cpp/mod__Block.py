all = []

from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil

class _Block:
    """
    Represents a "block" of text
    """

    #region init

    def __init__(self, line:int, column:int, text:str):
        """
        Initializer for _Block
        
        :param line:
            Line number of beginning of text
        :param column:
            Column of beginning of text
        :param text:
            Text
        """
        self.__line = line
        self.__column = column
        self.__text = text

    #endregion

    #region operators

    def __repr__(self):
        return f"_Block({self.__line}, {self.__column}, {self.__line})"

    def __str__(self):
        return self.__text
    
    def __eq__(self, other):
        return self.__equals(other)
    
    def __ne__(self, other):
        return not self.__equals(other)
    
    def __hash__(self):
        return hash(self.__text)

    def __len__(self):
        return len(self.__text)
    
    def __iter__(self):
        for _c in self.__text:
            yield _c
    
    def __getitem__(self, key):
        try:
            _index = _ErrorUtil.valid_int(key)
            if _index < 0 or _index >= len(self.__text):
                raise IndexError("Index is out of range.")
            return self.__text[_index]
        except TypeError as _e:
            e = _e
        except IndexError as _e:
            e = _e
        raise e

    #endregion

    #region helper methods

    def __equals(self, other):
        if isinstance(other, _Block):
            return\
                self.__line == other.__line and\
                self.__column == other.__column and\
                self.__text == other.__text
        if isinstance(other, str):
            return self.__text == other
        return False

    #endregion

    #region methods

    def linecol(self, index:int):
        """
        Gets the line and column of the character at the specified index\n
        NOTE: The first column in a line is 1.
        
        :param index:
            Index of character
        :return:
            Line and column of the character at index:
        :raise IndexError:
            index is out of range
        """
        if index < 0 or index > len(self.__text):
            raise IndexError("Index is out of range.")
        line = self.__line
        column = self.__column
        for _i in range(index):
            if self.__text[_i] == '\n':
                line += 1
                column = 1
            else:
                column += 1
        return line, column

    def sub(self, beg:None|int = None, end:None|int = None):
        """
        Creates a subblock

        :param beg:
            Start index
        :param end:
            End index
        :return:
            Created subblock
        :raise IndexError:
            Indexes are out of range
        """
        def _valid_int(_index:int):
            if _index < 0: _index += len(self.__text)
            return _index
        # beg
        if beg is None:
            _beg = 0
        else:
            _beg = _valid_int(beg)
        # end
        if end is None:
            _end = len(self.__text)
        else:
            _end = _valid_int(end)
        # Check range
        if _beg > _end:
            raise IndexError("Start index must be less than or equal to stop index.")
        # Success!!!
        _line, _column = self.linecol(_beg)
        return _Block(_line, _column, self.__text[_beg:_end])

    #endregion