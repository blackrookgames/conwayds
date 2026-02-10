all = []

from ...cli.mod_CLICommandBase import\
    CLICommandBase as _CLICommandBase

from ..mod__Creator import _Creator
from ..mod__CmdFuncError import _CmdFuncError

class _HFunc(_CLICommandBase):
    """
    Represents a function helper class
    """

    #region methods
 
    def execute(self, creator:_Creator, argv:list[str]):
        """
        Executes the function
        
        :param creator:
            C++ source creator
        :param argv:
            Input arguments (including function name)
        :return:
            String value
        :raise _CmdFuncError:
            An error occurred
        """
        parse = self._parseargs(argv, True)
        if parse != self._PARSEARGS_PASS:
            raise _CmdFuncError() # Assume fail
        return self._main(creator)
    
    def _main(self, creator:_Creator) -> str:
        """
        :raise _CmdFuncError:
            An error occurred
        """
        raise NotImplementedError("_main has not yet been implemented.")
        
    #endregion