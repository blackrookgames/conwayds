from __future__ import annotations
from typing import TYPE_CHECKING

all = [\
    '_Creator',]

from io import\
    StringIO as _StringIO
from pathlib import\
    Path as _Path
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

from .mod__CmdFuncError import _CmdFuncError


if TYPE_CHECKING:
    from .mod__call import _CmdCall, _CmdDef, _FuncCall, _FuncDef

class _Creator:
    """
    Represents a "creator" of C++ source code
    """

    #region init

    def __init__(self, reader:_TextReader, dpath:_Path, cmds:dict[str, _CmdDef], funcs:dict[str, _FuncDef]):
        """
        Do NOT create a _Creator instance directly. Instead, call _Creator.run().
        """
        self.__reader = reader
        self.__dpath = dpath.resolve()
        self.__cmds = cmds
        self.__funcs = funcs
        self.__vars:dict[str, object] = {}

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

    def __parse_cmd(self, argv:list[str]):
        if len(argv) == 0:
            raise _CmdFuncError("Command name expected")
        # Get name
        name = str(argv[0])
        if not (name in self.__cmds):
            raise _CmdFuncError(f"Unknown command: {name}")
        # Call function
        self.__cmds[name].call(self, argv)

    def __parse_func(self, argv:list[str]):
        if len(argv) == 0:
            raise _CmdFuncError("Function name expected")
        # Get name
        name = str(argv[0])
        if not (name in self.__funcs):
            raise _CmdFuncError(f"Unknown function: {name}")
        # Call function
        return self.__funcs[name].call(self, argv)

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
        def _getchar(_digits, _bspos):
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
            return chr(_ord)
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
            char = chr(self.__ESCSEQ[self.__reader.chr.ord])
        elif self.__reader.chr.ord == 0x78:
            char = _getchar(2, bspos)
        elif self.__reader.chr.ord == 0x75:
            char = _getchar(4, bspos)
        else:
            raise _CLICommandError(_unrecognized(bspos, self.__reader.cursor + 1))
        # Success!!!
        self.__reader.next()
        return char

    def __read_arg(self, endchr:int, noneifeol:bool):
        with _StringIO() as strio:
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
                    strio.write(self.__read_esc())
                    continue
                # Dollar sign?
                if self.reader.chr.ord == 0x24:
                    self.__read_dollar(strio)
                    continue
                # Quote?
                if self.reader.chr.ord == 0x22:
                    self.__read_quote(strio)
                    continue
                # Anything else
                strio.write(chr(self.reader.chr.ord))
                self.__reader.next()
            # Success!!!
            return strio.getvalue()

    def __read_quote(self, strio:_StringIO):
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
                strio.write(self.__read_esc())
                continue
            # Dollar sign?
            if self.reader.chr.ord == 0x24:
                self.__read_dollar(strio)
                continue
            # Anything else
            strio.write(chr(self.reader.chr.ord))
            self.__reader.next()
    
    def __read_toline(self):
        with _StringIO() as strio:
            while not self.reader.eol:
                # Escape?
                if self.reader.chr.ord == 0x5c:
                    strio.write(self.__read_esc())
                    continue
                # Dollar sign?
                if self.reader.chr.ord == 0x24:
                    self.__read_dollar(strio)
                    continue
                # Anything else
                strio.write(chr(self.reader.chr.ord))
                self.__reader.next()
            # Success!!!
            return strio.getvalue()

    def __read_dollar(self, strio:_StringIO):
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
        try:
            # Variable?
            if self.__reader.chr.ord == 0x7B:
                self.__reader.next()
                varname = self.__read_varname()
                if varname is None:
                    raise _CLICommandError(self.__reader.error(\
                        "Missing closing bracket",\
                        pos = opos))
                varvalue = self.get_var(varname)
                if not isinstance(varvalue, str):
                    raise _CLICommandError(self.__reader.error(\
                        f"{varname} is not a string variable.",\
                        pos = opos))
                strio.write(varvalue)
                return
            # Function?
            if self.__reader.chr.ord == 0x28:
                self.__reader.next()
                funcargs = self.__read_cmdorfunc(True)
                if funcargs is None:
                    raise _CLICommandError(self.__reader.error(\
                        "Missing closing parenthesis",\
                        pos = opos))
                strio.write(self.__parse_func(funcargs))
                return
            # Invalid
            raise _CLICommandError(self.__reader.error(\
                "Expected ( or {",\
                pos = opos))
        except _CmdFuncError as _e:
            e = _CLICommandError(self.__reader.error(_e, pos = opos))
        raise e
    
    def __read_cmdorfunc(self, readfunc:bool):
        # Compute end character
        endchr = 0x29 if readfunc else -1
        # Read arguments
        argv:list[str] = []
        minargs = None # This is the minimum before reading the rest as one argument
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
                    _arg = str(arg)
                    if _arg in self.__cmds:
                        minargs = self.__cmds[_arg].minargs
                # If minimum is met, read the rest as one argument
                if minargs is not None and len(argv) == minargs:
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

    #region run method

    @classmethod
    def run(cls, fpath:str, dpath:str, cmds:dict[str, _CmdDef], funcs:dict[str, _FuncDef]):
        """
        Creates C++ sources.

        :param fpath:
            Path of configuration file
        :param dpath:
            Path of working directory
        :param cmds:
            Dictionary of commands
        :param funcs:
            Dictionary of functions
        :raise CLICommandError:
            An error occurred
        """
        try:
            # Create instance
            rawtext = _CLIStrUtil.str_from_file(fpath)
            creator = _Creator(_TextReader(_Text(rawtext)), _Path(dpath), cmds, funcs)
            # Parse
            while not creator.reader.eof:
                start = creator.reader.cursor
                # Read command
                argv = _cast(list[str], creator.__read_cmdorfunc(False))
                if len(argv) == 0:
                    continue
                # Execute command
                try:
                    creator.__parse_cmd(argv)
                    continue
                except _CmdFuncError as _e:
                    e = _CLICommandError(creator.__reader.error(_e, pos = start))
                raise e
            # Success!!!
            return
        except _CLICommandError as _e:
            e = _e
        raise e

    #endregion

    #region methods

    def set_var(self, name, value:object):
        """
        Sets the value of the variable with the specified name. If the variable does not 
        exist, it will be created.
        
        :param name:
            Variable name
        :param value:
            Value of variable
        """
        self.__vars[str(name)] = value

    def get_var(self, name):
        """
        Gets the value of the variable with the specified name
        
        :param name:
            Variable name
        :param errorpos:
            Cursor position for raising an error
        :return:
            Value of variable
        :raise CLICommandError:
            Variable could not be found
        """
        # Get name
        name = str(name)
        if not (name in self.__vars):
            raise _CLICommandError(f"Unknown variable: {name}")
        # Get value
        return self.__vars[name]

    def resolvepath(self, path):
        """
        Resolves the path. If the path is relative, it is assumed it is relative to the working directory.
        
        :param self: Description
        :param path: Description
        """
        path = _Path(str(path))
        if not path.is_absolute():
            path = self.__dpath / path
        return str(path.resolve())

    #endregion