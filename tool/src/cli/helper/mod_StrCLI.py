__all__ = [\
    'StrCLI',]

from sys import\
    stderr as _stderr

class StrCLI:
    """
    CLI-utility for string-related operations
    """

    #region str

    @classmethod
    def load(cls, path:str):
        """
        Attempts to create a string by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created string (or None if load failed)
        """
        try:
            with open(path, 'rt') as input:
                return input.read()
        except Exception as e:
            print(f"ERROR: {e}", file = _stderr)
            return None

    @classmethod
    def save(cls, string:str, path:str):
        """
        Attempts to save a string to a file
        
        :param string:
            String to save
        :param path:
            Path of output file
        :return:
            Whether or not successful
        """
        try: 
            with open(path, 'wt') as output:
                output.write(string)
            return True
        except Exception as e:
            print(f"ERROR: {e}", file = _stderr)
            return False

    #endregion