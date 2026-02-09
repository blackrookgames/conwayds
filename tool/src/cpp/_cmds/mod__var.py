all = []

from ...data.mod_Text import\
    Text as _Text

from ..mod__call import _CmdDef
from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator

def __cmd(creator:_Creator, argv:list[_Text]):
    # Variable name
    if len(argv) <= 1: raise _CmdFuncError("Expected variable name")
    name = argv[1]
    # Variable value
    if len(argv) <= 2: value = None
    else: value = argv[2]
    # Set variable
    creator.set_var(name, value)

__def = _CmdDef(__cmd, minargs = 2)