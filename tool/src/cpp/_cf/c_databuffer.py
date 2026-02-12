all = []

from ...data.mod_DataBuffer import\
    DataBuffer as _DataBuffer

from ..mod__call import _CmdDef
from .c__HCmdConvert import __cmd
from .c_databuffers import __DICT

__def = _CmdDef(lambda creator, argv: __cmd(creator, argv, _DataBuffer, __DICT))