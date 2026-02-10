all = []

from ...cli.mod_CLICommandBase import\
    CLICommandBase as _CLICommandBase

from ..mod__Creator import _Creator
from ..mod__CmdFuncError import _CmdFuncError

class _HCmd(_CLICommandBase):
    """
    Represents a command helper class
    """
    
    #region methods
 
    def execute(self, creator:_Creator, argv:list[str]):
        """
        Executes the command
        
        :param creator:
            C++ source creator
        :param argv:
            Input arguments (including command name)
        :raise _CmdFuncError:
            An error occurred
        """
        parse = self._parseargs(argv, True)
        if parse != self._PARSEARGS_PASS:
            raise _CmdFuncError() # Assume fail
        self._main(creator)
    
    def _main(self, creator:_Creator) -> None:
        """
        :raise _CmdFuncError:
            An error occurred
        """
        raise NotImplementedError("_main has not yet been implemented.")
        
    #endregion