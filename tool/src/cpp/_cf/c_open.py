all = []

from typing import\
    cast as _cast

from ...cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef

from ..mod__call import _CmdDef
from ..mod__Creator import _Creator
from .c__HCmd import _HCmd

class _HHCmd(_HCmd):
    __path = _CLIRequiredDef(name = "path")
    def _main(self, creator: _Creator):
        self_path = _cast(str, self.path) # type: ignore
        creator.file_open(creator.resolvepath(self_path))

def __cmd(creator:_Creator, argv:list[str]):
    _HHCmd().execute(creator, argv)

__def = _CmdDef(__cmd)