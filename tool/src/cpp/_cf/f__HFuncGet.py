all = []

from typing import\
    Callable as _Callable,\
    cast as _cast

from ...cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef

from ..mod__Creator import _Creator
from ..mod__CmdFuncError import _CmdFuncError
from .f__HFunc import _HFunc
from .h_helper import _tryfindtype

class _HFuncGet(_HFunc):
    """
    Represents a get function helper class
    """

    #region input

    __varname = _CLIRequiredDef(name = "varname")

    #endregion

    #region helper properties

    @property
    def _propname(self) -> str:
        raise NotImplementedError("_propname has not yet been implemented.")

    @property
    def _gets(self) -> dict[type, _Callable[[object], str]]:
        raise NotImplementedError("_gets has not yet been implemented.")

    #endregion

    #region methods
 
    def _main(self, creator:_Creator):
        self_varname = _cast(str, self.varname) # type: ignore
        obj = creator.get_var(self_varname)
        t = type(obj)
        found, get = _tryfindtype(self._gets, t)
        if not found:
            raise _CmdFuncError(f"{t.__name__} has not have a {self._propname} property.")
        assert get is not None
        return get(obj)
        
    #endregion