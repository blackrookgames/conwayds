all = []

from ..mod__call import _CmdDef
from ..mod__Creator import _Creator
from .c__HCmd import _HCmd

class _HHCmd(_HCmd):
    def _main(self, creator: _Creator):
        creator.file_close()

def __cmd(creator:_Creator, argv:list[str]):
    _HHCmd().execute(creator, argv)

__def = _CmdDef(__cmd)