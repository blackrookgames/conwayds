all = []

from ....cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef

from ...mod__CmdFuncError import _CmdFuncError
from ...mod__Creator import _Creator
from ..c__HCmd import _HCmd

class _HCmdSave(_HCmd):
    __path = _CLIRequiredDef(name = "path")
    def __init__(self, data:object):
        super().__init__()
        self.__data = data
    @property
    def _data(self): return self.__data