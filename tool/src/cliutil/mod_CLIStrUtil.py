__all__ = [\
    'CLIStrUtil',]

from .mod_CLICommandError import\
    CLICommandError as _CLICommandError

class CLIStrUtil:
    """
    CLI-utility for string-related operations
    """

    #region str

    @classmethod
    def str_from_file(cls, path:str):
        """
        Creates a string by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created string
        :raise CLICommandError:
            An error occurred
        """
        try:
            with open(path, 'rt') as input:
                return input.read()
        except Exception as e:
            error = _CLICommandError(e)
        raise error

    @classmethod
    def str_to_file(cls, string:str, path:str):
        """
        Saves a string to a file
        
        :param string:
            String to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        try: 
            with open(path, 'wt') as output:
                output.write(string)
            return
        except Exception as e:
            error = _CLICommandError(e)
        raise error

    #endregion