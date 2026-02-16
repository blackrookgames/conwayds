all = []

from ...ds.mod_DSBitmap import\
    DSBitmap as _DSBitmap

from ..mod__call import _CmdDef
from .c__HCmdConvert import __cmd
from .c_dsbitmaps import __DICT

__def = _CmdDef(lambda creator, argv: __cmd(creator, argv, _DSBitmap, __DICT))