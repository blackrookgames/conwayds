all = []

from typing import\
    cast as _cast

from ....ds.mod_DSBitmap16 import\
    DSBitmap16 as _DSBitmap16
from ....ds.mod_DSSerial import\
    DSSerial as _DSSerial

from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert

class _HHCmdConvert(_HCmdConvert):
    def _main(self, creator: _Creator):
        idata = _cast(_DSBitmap16, self._data)
        odata = _DSSerial.bitmap16_to_bin(idata)
        creator.set_var(self._ovar, odata)

type _type = _DSBitmap16
def _create(data, ovar): return _HHCmdConvert(data, ovar)