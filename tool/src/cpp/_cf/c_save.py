all = []

from ...data.mod_Text import\
    Text as _Text

from ..mod__call import _CmdDef
from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator
from .c_saves import __DICT

def __cmd(creator:_Creator, argv:list[str]):
    if len(argv) <= 1:
        raise _CmdFuncError("Not enough arguments")
    data = creator.get_var(argv[1])
    dtype = type(data)
    if not (dtype in __DICT):
        raise _CmdFuncError(f"Saving {dtype.__name__} data is not supported.")
    savecmd = __DICT[dtype](data)
    savecmd.execute(creator, [argv[_i] for _i in range(1, len(argv))])

__def = _CmdDef(__cmd)