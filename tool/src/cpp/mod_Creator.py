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

    #region "helper" methods

    def readblock(self):
        """
        Reads a "block" of text
        """
        _line = self.reader.read_line()
        if len(_line) > 0:
            _last = _line[len(_line) - 1]
            while _last == '\\':
                self.reader.next()
                _line = _cast(_Text, _line.sub(end = -1) + _TextChar(0x20, _last.row, _last.col) + self.reader.read_line())
                _last = _line[len(_line) - 1]
        return _line

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
            # Parse TODO: Rewrite
            while True:
                # Skip whitespace
                creator.reader.skip_white()
                if creator.reader.eof: break
                # Parse line
                _line = creator.readblock()
                print(f"({_line[0].row}, {_line[0].col}) {_line}")
            # Success!!!
            return
        except _CLICommandError as _e:
            e = _e
        raise e

    #endregion