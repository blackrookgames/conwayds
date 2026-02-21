all = []

from sys import\
    stderr as _stderr
from typing import\
    cast as _cast

from ....img.mod_ImgImage import\
    ImgImage as _ImgImage
from ....life.mod_LifeUtil import\
    LifeUtil as _LifeUtil

from ...mod__CmdFuncError import _CmdFuncError
from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert

class _HHCmdConvert(_HCmdConvert):
    def _main(self, creator: _Creator):
        idata = _cast(_ImgImage, self._data)
        odata = _LifeUtil.pattern_get_img(idata)
        creator.set_var(self._ovar, odata)

type _type = _ImgImage
def _create(data, ovar): return _HHCmdConvert(data, ovar)