all = []

from typing import\
    cast as _cast

from ...cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef

from ..mod__call import _CmdDef
from ..mod__Creator import _Creator
from .c__HCmd import _HCmd

class _HHCmd(_HCmd):
    __varname = _CLIRequiredDef(name = "varname")
    __varvalue = _CLIRequiredDef(name = "varvalue")
    def _main(self, creator: _Creator):
        self_varname = _cast(str, self.varname) # type: ignore
        self_varvalue = _cast(str, self.varvalue) # type: ignore
        creator.set_var(self_varname, self_varvalue)

def __cmd(creator:_Creator, argv:list[str]):
    _HHCmd().execute(creator, argv)

__def = _CmdDef(__cmd, minargs = 2)