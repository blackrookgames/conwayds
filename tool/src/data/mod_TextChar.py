__all__ = [\
    'TextChar',\
    'TEXTCHAR_NULL']

class TextChar:
    """
    Represents a text character
    """

    #region init

    def __init__(self, ord:int, row:int, col:int):
        """
        Initializer for TextChar
        
        :param ord:
            Ordinal
        :param row:
            Row
        :param col:
            Column
        :raise ValueError:
            ord is less than 0 or greater than 1114111
        """
        if ord < 0 or ord > 1114111:
            raise ValueError("ord must be >= 0 and <= 1114111.")
        self.__ord = ord
        self.__row = row
        self.__col = col
        

    #endregion

    #region operators

    def __repr__(self):
        return f"TextChar({self.ord}, {self.row}, {self.col})"
    
    def __str__(self):
        return chr(self.__ord)
    
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
        return hash(self.__ord)

    #endregion

    #region properties

    @property
    def ord(self):
        """
        Ordinal
        """
        return self.__ord

    @property
    def row(self):
        """
        Row
        """
        return self.__row

    @property
    def col(self):
        """
        Column
        """
        return self.__col

    #endregion

    #region helper methods

    def __equals(self, other):
        if isinstance(other, TextChar):
            return \
                self.__ord == other.__ord and \
                self.__row == other.__row and \
                self.__col == other.__col
        if isinstance(other, int):
            return self.__ord == other
        if isinstance(other, str):
            return chr(self.__ord) == other
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
        if isinstance(other, TextChar):
            # Compare ord
            _cmp = self.__ord - other.__ord
            if _cmp != 0: return _cmp
            # Compare row
            _cmp = self.__row - other.__row
            if _cmp != 0: return _cmp
            # Compare col
            return self.__col - other.__col
        if isinstance(other, int):
            return self.__ord - other
        if isinstance(other, str):
            if len(other) == 0: return 1
            # Compare character
            _cmp = self.__ord - ord(other[0])
            if _cmp != 0: return _cmp
            # Compare "length"
            return 1 - len(other)
        return None
    
    def iswhite(self):
        """
        Checks whether or not the character is whitespace
        """
        return self.__ord <= 0x20
    
    def isdigit(self):
        """
        Checks whether or not the character is a digit
        """
        return self.__ord >= 0x30 and self.__ord <= 0x39
    
    def isletter(self):
        """
        Checks whether or not the character is a letter
        """
        return self.isupper() or self.islower()
    
    def isupper(self):
        """
        Checks whether or not the character is an uppercase letter
        """
        return self.__ord >= 0x41 and self.__ord <= 0x5A
    
    def islower(self):
        """
        Checks whether or not the character is an lowercase letter
        """
        return self.__ord >= 0x61 and self.__ord <= 0x7A

    #endregion

TEXTCHAR_NULL = TextChar(0, 0, 0)