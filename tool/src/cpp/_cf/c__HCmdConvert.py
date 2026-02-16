all = []

from typing import\
    Callable as _Callable

from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator
from .c__HCmd import _HCmd

from .h_helper import _tryfindtype

class _HCmdConvert(_HCmd):
    """
    Represents a conversion command helper class
    """

    #region init

    def __init__(self, data:object, ovar:str):
        """
        Initializer for _HCmdConvert
        
        :param data:
            Input data
        :param ovar:
            Output variable
        """
        super().__init__()
        self.__data = data
        self.__ovar = ovar

    #endregion

    #region helper properties

    @property
    def _data(self): return self.__data
    
    @property
    def _ovar(self): return self.__ovar

    #endregion



def __cmd(creator:_Creator, argv:list[str],\
        otype:type,\
        compatible:dict[type, _Callable[[object, str], _HCmdConvert]]):
    if len(argv) <= 2:
        raise _CmdFuncError("Not enough arguments")
    ovar = argv[1]
    ivar = argv[2]
    data = creator.get_var(ivar)
    dtype = type(data)
    found, cmd = _tryfindtype(compatible, dtype)
    if not found:
        raise _CmdFuncError(f"Cannot create a {otype.__name__} out of {dtype.__name__}.")
    assert cmd is not None
    convertcmd = cmd(data, ovar)
    convertcmd.execute(creator, [argv[_i] for _i in range(2, len(argv))])