all = []

from sys import\
    stderr as _stderr
from typing import\
    cast as _cast

from ....cli.mod_CLIOptionFlagDef import\
    CLIOptionFlagDef as _CLIOptionFlagDef
from ....cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef
from ....ds.mod_DSUtil import\
    DSUtil as _DSUtil
from ....img.mod_ImgImage import\
    ImgImage as _ImgImage

from ...mod__CmdFuncError import _CmdFuncError
from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert
from .c__common import _tobpp

class _HHCmdConvert(_HCmdConvert):
    __bpp = _CLIRequiredDef(name = "bpp", parse = _tobpp)
    def _main(self, creator: _Creator):
        self_bpp = _cast(bool, self.bpp) # type: ignore
        idata = _cast(_ImgImage, self._data)
        if self_bpp == 8:
            if not idata.haspalette:
                raise _CmdFuncError("Cannot create an 8bpp DS bitmap out of a non-paletted image.")
            odata = _DSUtil.bitmap8_get_img(idata)
        else:
            odata = _DSUtil.bitmap16_get_img(idata)
        creator.set_var(self._ovar, odata)

type _type = _ImgImage
def _create(data, ovar): return _HHCmdConvert(data, ovar)