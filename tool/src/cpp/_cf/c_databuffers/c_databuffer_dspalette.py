all = []

from typing import\
    cast as _cast

from ....data.mod_DataBuffer import\
    DataBuffer as _DataBuffer
from ....ds.mod_DSPalette import\
    DSPalette as _DSPalette
from ....ds.mod_DSSerial import\
    DSSerial as _DSSerial

from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert

class _HHCmdConvert(_HCmdConvert):
    def _main(self, creator: _Creator):
        idata = _cast(_DSPalette, self._data)
        odata = _DSSerial.palette_to_bin(idata)
        creator.set_var(self._ovar, odata)

type _type = _DSPalette
def _create(data, ovar): return _HHCmdConvert(data, ovar)