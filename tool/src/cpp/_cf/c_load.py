all = []

from ...data.mod_Text import\
    Text as _Text

from ..mod__call import _CmdDef
from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator
from .c_loads import  __DICT

def __cmd(creator:_Creator, argv:list[str]):
    if len(argv) <= 1:
        raise _CmdFuncError("Not enough arguments")
    t = argv[1]
    if not (t in __DICT):
        raise _CmdFuncError(f"{t} is not a valid target type.")
    loadcmd = __DICT[t]()
    loadcmd.execute(creator, [argv[_i] for _i in range(1, len(argv))])

__def = _CmdDef(__cmd)