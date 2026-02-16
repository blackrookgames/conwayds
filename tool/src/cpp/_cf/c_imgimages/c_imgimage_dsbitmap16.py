all = []

from typing import\
    cast as _cast

from ....ds.mod_DSBitmap16 import\
    DSBitmap16 as _DSBitmap16
from ....ds.mod_DSUtil import\
    DSUtil as _DSUtil
from ....img.mod_ImgImage import\
    ImgImage as _ImgImage

from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert

class _HHCmdConvert(_HCmdConvert):
    def _main(self, creator: _Creator):
        ibmp = _cast(_DSBitmap16, self._data)
        image = _ImgImage()
        _DSUtil.bitmap16_set_img(image, ibmp)
        creator.set_var(self._ovar, image)

type _type = _DSBitmap16
def _create(data, ovar): return _HHCmdConvert(data, ovar)