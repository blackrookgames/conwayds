all = []

from ...data.mod_Text import\
    Text as _Text

from ..mod__call import _FuncDef
from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator

def __func(creator:_Creator, argv:list[_Text]):
    if len(argv) <= 1:
        raise _CmdFuncError("Expected variable name")
    varname = argv[1]
    vartype = type(creator.get_var(varname))
    return _Text(vartype.__name__, norowcol = True)

__def = _FuncDef(__func)