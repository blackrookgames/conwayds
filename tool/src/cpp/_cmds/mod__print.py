all = []

from ...data.mod_Text import\
    Text as _Text

from ..mod__call import _CmdDef
from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator

def __cmd(creator:_Creator, argv:list[str]):
    if len(argv) <= 1: print()
    print(argv[1])

__def = _CmdDef(__cmd, minargs = 1)