all = []

from sys import\
    stderr as _stderr
from typing import\
    cast as _cast

from ....cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef
from ....ds.mod_DSUtil import\
    DSUtil as _DSUtil
from ....img.mod_ImgImage import\
    ImgImage as _ImgImage

from ...mod__call import _CmdDef
from ...mod__CmdFuncError import _CmdFuncError
from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert
from .c__common import __tobpp as p__tobpp

class _HHCmdConvert(_HCmdConvert):
    __bpp = _CLIRequiredDef(name = "bpp", parse = p__tobpp)
    def _main(self, creator: _Creator):
        self_bpp = _cast(int, self.bpp) # type: ignore
        idata = _cast(_ImgImage, self._data)
        if not idata.haspalette:
            raise _CmdFuncError("Cannot create a DS tileset out of a non-paletted image.")
        odata = _DSUtil.tileset4_get_img(idata) if self_bpp == 4\
            else _DSUtil.tileset8_get_img(idata)
        creator.set_var(self._ovar, odata)

type _type = _ImgImage
def _create(data, ovar): return _HHCmdConvert(data, ovar)