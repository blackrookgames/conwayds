all = [\
    'Creator',]

from io import\
    StringIO as _StringIO 
from pathlib import\
    Path as _Path

from ..cliutil.mod_CLICommandError import\
    CLICommandError as _CLICommandError
from ..cliutil.mod_CLIStrUtil import\
    CLIStrUtil as _CLIStrUtil
from ..data.mod_StringReader import\
    StringReader as _StringReader
from .mod__Block import _Block

class Creator:
    """
    Represents a "creator" of C++ source code
    """

    #region init

    def __init__(self, blocks:list[_Block], dpath):
        """
        Do NOT create a Creator instance directly. Instead, call Creator.run().
        """
        # These variable may also be accessed by other classes in the cpp module
        self.__blocks = blocks
        self.__dpath = dpath

    #endregion

    #region properties

    

    #endregion

    #region helper methods

    @classmethod
    def __readblocks(cls, path:str):
        try:
            # Open file
            rawtext = _CLIStrUtil.str_from_file(path)
            blocks:list[_Block] = []
            with _StringIO() as _blockio:
                _f_row = 1
                _f_col = 1
                _c_row = 1
                _c_col = 1
                _esc = False
                for _chr in rawtext:
                    _new = False
                    if _esc:
                        if _chr != '\n':
                            _blockio.write('\\')
                        _blockio.write(_chr)
                        _esc = False
                    else:
                        if _chr == '\n':
                            blocks.append(_Block(_f_row, _f_col, _blockio.getvalue()))
                            _new = True
                            _blockio.seek(0)
                            _blockio.truncate(0)
                        elif _chr == '\\':
                            _esc = True
                        else:
                            _blockio.write(_chr)
                    # Update row and column
                    if _chr == '\n':
                        _c_row += 1
                        _c_col = 1
                    else:
                        _c_col += 1
                    if _new:
                        _f_row = _c_row
                        _f_col = _c_col
                blocks.append(_Block(_f_row, _f_col, _blockio.getvalue()))
            # Success!!!
            return blocks
        except _CLICommandError as _e:
            e = _e
        raise e

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
            # Read file
            blocks = cls.__readblocks(fpath)
            # Create instance
            creator = Creator(blocks, dpath)
            # Success!!!
            return
        except _CLICommandError as _e:
            e = _e
        raise e

    #endregion