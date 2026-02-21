all = []

from typing import\
    cast as _cast

from ....img.mod_ImgImage import\
    ImgImage as _ImgImage
from ....life.mod_LifePattern import\
    LifePattern as _LifePattern
from ....life.mod_LifeUtil import\
    LifeUtil as _LifeUtil

from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert

class _HHCmdConvert(_HCmdConvert):
    def _main(self, creator: _Creator):
        idata = _cast(_LifePattern, self._data)
        odata = _ImgImage()
        _LifeUtil.pattern_set_img(odata, idata)
        creator.set_var(self._ovar, odata)

type _type = _LifePattern
def _create(data, ovar): return _HHCmdConvert(data, ovar)