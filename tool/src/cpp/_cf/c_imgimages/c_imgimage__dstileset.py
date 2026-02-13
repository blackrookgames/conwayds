all = []

from typing import\
    cast as _cast

from ....cli.mod_CLIOptionFlagDef import\
    CLIOptionFlagDef as _CLIOptionFlagDef
from ....cli.mod_CLIOptionWArgDef import\
    CLIOptionWArgDef as _CLIOptionWArgDef
from ....cli.mod_CLIParseUtil import\
    CLIParseUtil as _CLIParseUtil
from ....cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef

from ..c__HCmdConvert import _HCmdConvert

class _HHCmdConvert(_HCmdConvert):
    __palette = _CLIRequiredDef("palette")
    __tpr = _CLIOptionWArgDef("tpr", parse = _CLIParseUtil.to_int, default = 16)
    __noalpha = _CLIOptionFlagDef("noalpha")