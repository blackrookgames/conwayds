all = []

from ...ds.mod_DSPalette import\
    DSPalette as _DSPalette

from ..mod__call import _CmdDef
from .c__HCmdConvert import __cmd
from .c_dspalettes import __DICT

__def = _CmdDef(lambda creator, argv: __cmd(creator, argv, _DSPalette, __DICT))