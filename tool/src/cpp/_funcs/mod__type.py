all = []

from typing import\
    cast as _cast

from ...cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef

from ..mod__call import _FuncDef
from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator
from .mod___HFunc import _HFunc

class _HHFunc(_HFunc):
    __varname = _CLIRequiredDef(name = "varname")
    def _main(self, creator: _Creator):
        self_varname = _cast(str, self.varname) # type: ignore
        vartype = type(creator.get_var(self_varname))
        return vartype.__name__

def __func(creator:_Creator, argv:list[str]):
    return _HHFunc().execute(creator, argv)

__def = _FuncDef(__func)