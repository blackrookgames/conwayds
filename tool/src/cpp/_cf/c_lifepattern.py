all = []

from ...life.mod_LifePattern import\
    LifePattern as _LifePattern

from ..mod__call import _CmdDef
from .c__HCmdConvert import __cmd
from .c_lifepatterns import __DICT

__def = _CmdDef(lambda creator, argv: __cmd(creator, argv, _LifePattern, __DICT))