__all__ = [\
    'CLICommand',]

from .mod_CLICommandBase import\
    CLICommandBase as _CLICommandBase

class CLICommand(_CLICommandBase):
    """
    Represents a command
    """

    #region init
    
    def __init__(self):
        """
        Initializer for CLICommand
        """
        super().__init__()

    #endregion

    #region methods
        
    def execute(self, argv:list[str]) -> int:
        """
        Executes the command
        
        :param args:
            Command-line arguments (including the name)
        :return:
            Exit code
        """
        parse = self._parseargs(argv, False)
        if parse != self._PARSEARGS_PASS:
            return parse
        return self._main()
    
    def _main(self) -> int:
        """
        Runs the main command code

        :return:
            Exit code
        """
        raise NotImplementedError()
        
    #endregion