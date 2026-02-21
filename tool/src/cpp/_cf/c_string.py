all = []

from ..mod__call import _CmdDef
from .c__HCmdConvert import __cmd
from .c_strings import __DICT

__def = _CmdDef(lambda creator, argv: __cmd(creator, argv, str, __DICT))