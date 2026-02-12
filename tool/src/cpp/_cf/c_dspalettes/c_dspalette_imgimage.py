all = []

from typing import\
    cast as _cast

from ....ds.mod_DSUtil import\
    DSUtil as _DSUtil
from ....img.mod_ImgImage import\
    ImgImage as _ImgImage
from ....img.mod_ImgPalette import\
    ImgPalette as _ImgPalette

from ...mod__CmdFuncError import _CmdFuncError
from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert

class _HHCmdConvert(_HCmdConvert):
    def _main(self, creator: _Creator):
        idata = _cast(_ImgImage, self._data)
        if not idata.haspalette:
            raise _CmdFuncError("Cannot create a DS palette out of a non-paletted image.")
        odata = _DSUtil.palette_get_pal(_cast(_ImgPalette, idata.palette))
        creator.set_var(self._ovar, odata)

type _type = _ImgImage
def _create(data, ovar): return _HHCmdConvert(data, ovar)