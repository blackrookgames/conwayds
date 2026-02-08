all = [\
    'Creator',]

from io import\
    StringIO as _StringIO 
from typing import\
    cast as _cast

from ..cliutil.mod_CLICommandError import\
    CLICommandError as _CLICommandError
from ..cliutil.mod_CLIStrUtil import\
    CLIStrUtil as _CLIStrUtil
from ..data.mod_StringReader import\
    StringReader as _StringReader
from ..data.mod_Text import\
    Text as _Text
from ..data.mod_TextChar import\
    TextChar as _TextChar
from ..data.mod_TextReader import\
    TextReader as _TextReader

class Creator:
    """
    Represents a "creator" of C++ source code
    """

    #region init

    def __init__(self, reader:_TextReader, dpath):
        """
        Do NOT create a Creator instance directly. Instead, call Creator.run().
        """
        self.__reader = reader
        self.__dpath = dpath

    #endregion

    #region const

    __ESCSEQ = {
        ord('n'): ord('\n'),
        ord('t'): ord('\t'),
        ord('\\'): ord('\\'),
        ord('\"'): ord('\"'),
        ord('b'): ord('\b'),
        ord('r'): ord('\r'),
        ord('a'): ord('\a'),
        ord('0'): ord('\0'),
        ord('$'): ord('$'),
        ord('#'): ord('#'),
    }

    __ONELINERS = [
        ("@print", 1),
        ("@var", 2),
        ("@line", 1),
    ]

    #endregion

    #region properties

    @property
    def reader(self):
        """
        Reader
        """
        return self.__reader
    
    @property
    def dpath(self):
        """
        Path of working directory
        """
        return self.__dpath

    #endregion

    #region helper methods

    @classmethod
    def __addtextchars(cls, l:list[_TextChar], t:_Text):
        for c in t: l.append(c)

    def __parse_cmd(self, argv:list[_Text]):
        # TODO: Rewrite
        for arg in argv:
            print(f"\"{arg}\"", end = ' ')
        print()

    def __parse_func(self, argv:list[_Text]):
        # TODO: Rewrite
        a = []
        for arg in argv:
            a.append(arg)
            a.append(_TextChar(0x20, 0, 0))
        return _Text(a)

    def __get_var(self, name:_Text):
        # TODO: Rewrite
        return name

    def __read_esc(self):
        """
        Assume
        - self.__reader.chr == '\\'
        """
        def _end(_bspos):
            return self.__reader.error(
                "Line ends before escape sequence is fully parsed.",
                pos = _bspos)
        def _unrecognized(_pos0, _pos1):
            _badseq = self.__reader.text.sub(_pos0, _pos1)
            return self.__reader.error(
                f"Unrecognized escape sequence: {_badseq}",
                pos = _pos0)
        def _getchar(_digits, _bspos, _bsrow, _bscol):
            _ord = 0
            while _digits > 0:
                _digits -= 1
                _ord <<= 4
                # Next char
                self.__reader.next()
                if self.__reader.eol:
                    raise _CLICommandError(_end(_bspos))
                # Check char
                if self.__reader.chr.ord >= 0x30 and self.__reader.chr.ord <= 0x39:
                    _ord |= self.__reader.chr.ord - 0x30
                    continue
                if self.__reader.chr.ord >= 0x41 and self.__reader.chr.ord <= 0x46:
                    _ord |= self.__reader.chr.ord + 10 - 0x41
                    continue
                if self.__reader.chr.ord >= 0x61 and self.__reader.chr.ord <= 0x66:
                    _ord |= self.__reader.chr.ord + 10 - 0x61
                    continue
                # Invalid
                raise _CLICommandError(self.__reader.error(
                    f"Invalid hex character: {self.__reader.chr}",
                    pos = _bspos))
            return _TextChar(_ord, _bsrow, _bscol)
        # Copy position of blackslash
        bspos = self.__reader.cursor
        bschr = self.__reader.chr
        # Next
        self.__reader.next()
        # End of line?
        if self.__reader.eol:
            raise _CLICommandError(_end(bspos))
        # Compute character
        if self.__reader.chr.ord in self.__ESCSEQ:
            char = _TextChar(self.__ESCSEQ[self.__reader.chr.ord], bschr.row, bschr.col)
        elif self.__reader.chr.ord == 0x78:
            char = _getchar(2, bspos, bschr.row, bschr.col)
        elif self.__reader.chr.ord == 0x75:
            char = _getchar(4, bspos, bschr.row, bschr.col)
        else:
            raise _CLICommandError(_unrecognized(bspos, self.__reader.cursor + 1))
        # Success!!!
        self.__reader.next()
        return char

    def __read_arg(self, endchr:int, noneifeol:bool):
        arg:list[_TextChar] = []
        while True:
            # End of line?
            if self.reader.eol:
                if noneifeol: return None
                break
            # End character?
            if self.reader.chr.ord == endchr:
                break
            # Whitespace?
            if self.reader.chr.iswhite():
                break
            # Comment?
            if self.reader.chr.ord == 0x23:
                break
            # Escape?
            if self.reader.chr.ord == 0x5c:
                arg.append(self.__read_esc())
                continue
            # Dollar sign?
            if self.reader.chr.ord == 0x24:
                self.__read_dollar(arg)
                continue
            # Quote?
            if self.reader.chr.ord == 0x22:
                self.__read_quote(arg)
                continue
            # Anything else
            arg.append(self.reader.chr)
            self.__reader.next()
        # Success!!!
        return _Text(arg)

    def __read_quote(self, arg:list[_TextChar]):
        """
        Assume
        - self.__reader.chr == '"'
        """
        qpos = self.__reader.cursor
        self.__reader.next()
        while True:
            if self.reader.eof:
                raise _CLICommandError(self.__reader.error(\
                    "Missing end quote", pos = qpos))
            # End quote
            if self.__reader.chr.ord == 0x22:
                self.__reader.next()
                break
            # Escape?
            if self.reader.chr.ord == 0x5c:
                arg.append(self.__read_esc())
                continue
            # Dollar sign?
            if self.reader.chr.ord == 0x24:
                self.__read_dollar(arg)
                continue
            # Anything else
            arg.append(self.reader.chr)
            self.__reader.next()
        # Success!!!
        return _Text(arg)
    
    def __read_toline(self):
        arg:list[_TextChar] = []
        while not self.reader.eol:
            # Escape?
            if self.reader.chr.ord == 0x5c:
                arg.append(self.__read_esc())
                continue
            # Dollar sign?
            if self.reader.chr.ord == 0x24:
                self.__read_dollar(arg)
                continue
            # Anything else
            arg.append(self.reader.chr)
            self.__reader.next()
        # Success!!!
        return _Text(arg)

    def __read_dollar(self, arg:list[_TextChar]):
        """
        Assume
        - self.__reader.chr == '"'
        """
        # Copy position of dollar sign
        dspos = self.__reader.cursor
        dschr = self.__reader.chr
        # Goto next character
        opos = self.__reader.cursor
        self.__reader.next()
        # Variable?
        if self.__reader.chr.ord == 0x7B:
            self.__reader.next()
            varname = self.__read_varname()
            if varname is None:
                raise _CLICommandError(self.__reader.error(\
                    "Missing closing bracket",\
                    pos = opos))
            self.__addtextchars(arg, self.__get_var(varname))
            return
        # Function?
        if self.__reader.chr.ord == 0x28:
            self.__reader.next()
            funcargs = self.__read_cmdorfunc(True)
            if funcargs is None:
                raise _CLICommandError(self.__reader.error(\
                    "Missing closing parenthesis",\
                    pos = opos))
            self.__addtextchars(arg, self.__parse_func(funcargs))
            return
        # Invalid
        raise _CLICommandError(self.__reader.error(\
            "Expected ( or {",\
            pos = opos))
    
    def __read_cmdorfunc(self, readfunc:bool):
        # Compute end character
        endchr = 0x29 if readfunc else -1
        # Read arguments
        argv:list[_Text] = []
        argmin = None # This is the minimum before reading the rest as one argument
        while (not self.reader.eol) and self.reader.chr.ord != endchr:
            # Whitespace?
            if self.reader.chr.iswhite():
                self.reader.next()
                continue
            # Comment?
            if self.reader.chr.ord == 0x23:
                self.reader.read_line()
                break
            # Backslash?
            if self.reader.chr.ord == 0x5c:
                # Check if next line is whitespace?
                self.reader.next()
                if self.reader.eol:
                    # Goto next line
                    self.reader.next()
                    continue
                if self.reader.chr.iswhite():
                    # Ensure there's only whitespace or comments
                    while not self.reader.eol:
                        # Whitespace?
                        if self.reader.chr.iswhite():
                            self.reader.next()
                            continue
                        # Comment?
                        if self.reader.chr.ord == 0x23:
                            self.reader.read_line()
                            break
                        # Invalid
                        raise _CLICommandError(self.reader.error_unex_char())
                    # Goto next line
                    self.reader.next()
                    continue
                # Return to blackslash
                self.reader.setcursor(self.reader.cursor - 1)
            # Parse argument
            arg = self.__read_arg(endchr, readfunc)
            if arg is None: return None
            argv.append(arg)
            # If looking for commands
            if not readfunc:
                # Get minimum arguments
                if len(argv) == 1:
                    for ol_name, ol_min in self.__ONELINERS:
                        if arg == ol_name:
                            argmin = ol_min
                            break
                # If minimum is met, read the rest as one argument
                if argmin is not None and len(argv) == argmin:
                    self.reader.next()
                    argv.append(self.__read_toline())
                    break
        # Goto next line
        self.reader.next()
        # Success!!!
        return argv

    def __read_varname(self):
        # Read variable name as single argument
        name = self.__read_arg(0x7D, True)
        if name is None: return None
        # Look for closing bracket
        while not self.__reader.eol:
            # Closing bracket?
            if self.__reader.chr.ord == 0x7D:
                self.__reader.next()
                return name
            # Whitespace?
            if self.__reader.chr.iswhite():
                self.__reader.next()
            # Invalid
            raise _CLICommandError(self.__reader.error("Expected }"))
        # Fail
        return None
        
    #endregion

    #region methods

    @classmethod
    def run(cls, fpath:str, dpath:str):
        """
        Creates C++ sources.

        :param fpath:
            Path of configuration file
        :param dpath:
            Path of working directory
        :raise CLICommandError:
            An error occurred
        """
        try:
            # Create instance
            rawtext = _CLIStrUtil.str_from_file(fpath)
            creator = Creator(_TextReader(_Text(rawtext)), dpath)
            # Parse
            while not creator.reader.eof:
                # Read command
                argv = _cast(list[_Text], creator.__read_cmdorfunc(False))
                if len(argv) == 0:
                    continue
                creator.__parse_cmd(argv)
            # Success!!!
            return
        except _CLICommandError as _e:
            e = _e
        raise e

    #endregion