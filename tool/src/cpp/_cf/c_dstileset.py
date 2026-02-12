all = []

from ...ds.mod_DSTileset import\
    DSTileset as _DSTileset

from ..mod__call import _CmdDef
from .c__HCmdConvert import __cmd
from .c_dstilesets import __DICT

__def = _CmdDef(lambda creator, argv: __cmd(creator, argv, _DSTileset, __DICT))