all = []

from ....cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef

from ...mod__CmdFuncError import _CmdFuncError
from ...mod__Creator import _Creator
from ..c__HCmd import _HCmd

class _HCmdLoad(_HCmd):
    __outvar = _CLIRequiredDef(name = "outvar")
    __path = _CLIRequiredDef(name = "path")