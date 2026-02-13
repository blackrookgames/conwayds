all = []

from ...img.mod_ImgImage import\
    ImgImage as _ImgImage

from ..mod__call import _CmdDef
from .c__HCmdConvert import __cmd
from .c_imgimages import __DICT

__def = _CmdDef(lambda creator, argv: __cmd(creator, argv, _ImgImage, __DICT))