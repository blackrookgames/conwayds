__all__ = [\
    'TextReader',]

from io import\
    StringIO as _StringIO

from .mod_Text import\
    Text as _Text
from .mod_TextChar import\
    TextChar as _TextChar,\
    TEXTCHAR_NULL as _TEXTCHAR_NULL

class TextReader:
    """
    Represents a string reader
    """

    #region init

    def __init__(self, src:_Text):
        """
        Initializer for TextReader
        
        :param src:
            Source text
        """
        self.__text = src
        self.__setcursor(0)

    #endregion

    #region properties

    @property
    def text(self):
        """
        Text that is being read
        """
        return self.__text
    
    @property
    def cursor(self):
        """
        Position of the cursor
        """
        return self.__cursor

    @property
    def chr(self):
        """
        Character at the current position of the cursor
        """
        return self.__chr

    @property
    def eof(self):
        """
        Whether or not the cursor has reached the end of the text
        """
        return self.__eof

    @property
    def eol(self):
        """
        Whether or not the cursor has reached the end of the current line in the text
        """
        return self.__eol

    #endregion

    #region helper methods

    def __setcursor(self, pos:int):
        """
        Assume:\n
        pos is in range
        """
        self.__cursor = pos
        if self.__cursor < len(self.__text):
            self.__chr = self.__text[self.__cursor]
            self.__eof = False
            self.__eol = self.__chr.ord == 0x0A
        else:
            self.__chr = _TEXTCHAR_NULL
            self.__eof = True
            self.__eol = True

    #endregion

    #region methods

    def setcursor(self, pos:int):
        """
        Sets the position of the cursor
        
        :param pos:
            Position of the cursor
        :raise ValueError:
            pos is out of range
        """
        if pos < 0 or pos > len(self.__text):
            raise ValueError("pos is out of range.")
        self.__setcursor(pos)

    def next(self):
        """
        Increments the cursor by 1.\n
        If the end of the text has already been reached, nothing happens. 
        """
        if self.__eof: return
        self.__setcursor(self.__cursor + 1)
    
    def read_line(self):
        """
        Reads to the end of the current line

        :return:
            Read content
        """
        line:list[_TextChar] = []
        while not self.__eol:
            line.append(self.__chr)
            self.next()
        return _Text(line)
    
    def skip_eol(self):
        """
        Skips to the end of the current line
        """
        while not self.__eol:
            self.next()
    
    def skip_line(self):
        """
        Skips to the next line
        """
        self.skip_eol()
        if not self.__eof:
            self.next()
    
    def skip_white(self):
        """
        Skips to next non-whitespace character\n
        If current character is not whitespace, nothing happens.
        """
        while (not self.__eof) and self.__chr.iswhite():
            self.next()
    
    def error(self, message, pos:int = -1, lineonly:bool = False):
        """
        Creates an error message about the string

        :param message:
            Error message
        :param pos:
            Position of problematic character (<0 means character at cursor position)
        :param lineonly:
            If true, then the column will not be added
        :raise ValueError:
            pos is out of range
        """
        with _StringIO() as strio:
            if pos > len(self.__text): # Do NOT check lower bound here
                raise ValueError("pos is out of range.")
            if pos < 0: pos = self.__cursor
            # Get row and column
            if len(self.__text) == 0:
                row = 1
                col = 1
            elif pos == len(self.__text):
                _char = self.__text[len(self.__text) - 1]
                row = _char.row
                col = _char.col + 1
            else:
                _char = self.__text[pos]
                row = _char.row
                col = _char.col + 1
            # ERROR
            strio.write("ERROR: ")
            # Line
            strio.write(f"Line: {row} ")
            # Column
            if not lineonly:
                strio.write(f"Column: {col} ")
            # Message
            strio.write(message)
            # Return
            return strio.getvalue()

    def error_unex_char(self):
        """
        Creates an error message about the current character being unexpected
        """
        return self.error(f"Unexpected character: {self.__chr}")

    def error_unex_end(self):
        """
        Creates an error message indicating an unexpected end of file\n
        Note that the actual state of the reader is not checked and will not be modified.
        """
        return self.error(f"Unexpected end of file.", lineonly = True)

    #endregion