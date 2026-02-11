all = []

import types as _types

from typing import\
    Callable as _Callable,\
    cast as _cast,\
    Generic as _Generic,\
    TypeVar as _TypeVar

from ...cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef

from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator
from .c__HCmd import _HCmd

T = _TypeVar('T')

class _HCmdConvert(_Generic[T], _HCmd):
    
    type _TCreate = _Callable[[_HCmdConvert, object], T]
    
    #region variables

    __output = _CLIRequiredDef(name = "output")
    __input = _CLIRequiredDef(name = "input")

    #endregion

    #region helper properties

    @property
    def _create(self) -> dict[type, _TCreate]:
        """
        Delegated function may raise CmdFuncError
        """
        raise NotImplementedError("_create has not yet been implemented.")

    #endregion 

    #region helper methods

    def __gentype(self):
        bases = _types.get_original_bases(type(self))
        for base in bases:
            for arg in base.__args__:
                if isinstance(arg, type):
                    return arg
        # Fallback
        return type(self)

    #endregion 

    #region methods

    def _main(self, creator: _Creator):
        self_output = _cast(str, self.output) # type: ignore
        self_input = _cast(str, self.input) # type: ignore
        # Get input
        idata = creator.get_var(self_input)
        itype = type(idata)
        # Create
        if not (itype in self._create):
            raise _CmdFuncError(f"Cannot create a {self.__gentype().__name__} out of {itype.__name__}.")
        creator.set_var(self_output, self._create[itype](self, idata))

    #endregion