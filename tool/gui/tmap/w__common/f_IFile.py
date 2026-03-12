__all__ = ['IFile',]

import src.cliutil as _cliutil

class IFile:
    """
    Immutable object representing data from a file
    """

    #region init

    def __init__(self, path:None|str):
        """
        Initializer for IFile
        
        :param path:
            Path of input file
        :raise CLICommandError:
            An error occurred
        """
        # path
        self.__path = path

    #endregion

    #region properties

    @property
    def path(self):
        """
        File path
        """
        return self.__path

    #endregion