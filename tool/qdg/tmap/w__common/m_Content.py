import numpy as _np

from pathlib import\
    Path as _Path

import src.cliutil as _cliutil
from .m_ContentCells import ContentCells as _ContentCells
from .m_ContentSize import ContentSize as _ContentSize

class Content:
    """
    Represents the content being edited
    """
    
    #region init

    def __init__(self, path:_Path):
        """
        Initializer for Content

        :param path: Filepath
        """
        self.__path = path
        self.__cells = _ContentCells()

    #endregion

    #region properties

    @property
    def path(self):
        """ Filepath """
        return self.__path

    @property
    def cells(self):
        """ Map cells """
        return self.__cells

    #endregion

    #region methods

    def load(self):
        """
        Loads content from path

        :raise CLICommandError: An error occurred
        """
        # Load file content
        content = _cliutil.CLIRLEUtil.uint16_from_file(str(self.__path))
        # Size
        def _size():
            try: return _ContentSize(content[0])
            except Exception as _e: e = _cliutil.CLICommandError(_e)
            raise e
        self.__cells.format(_size())
        # Cells
        _i = 1
        for _y in range(self.__cells.height):
            for _x in range(self.__cells.width):
                if _i >= len(content): break
                self.__cells[_x, _y] = _np.uint16(content[_i])
                _i += 1

    def save(self):
        """
        Saves content to path

        :raise CLICommandError: An error occurred
        """
        # Create file content
        content:list[int] = []
        content.append(self.__cells.size.value)
        for _y in range(self.__cells.height):
            for _x in range(self.__cells.width):
                content.append(int(self.__cells[_x, _y]))
        # Save file content
        _cliutil.CLIRLEUtil.uint16_to_file(content, str(self.__path))

    #endregion