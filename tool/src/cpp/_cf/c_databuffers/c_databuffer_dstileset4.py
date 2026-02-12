all = []

from typing import\
    cast as _cast

from ....data.mod_DataBuffer import\
    DataBuffer as _DataBuffer
from ....ds.mod_DSTileset4 import\
    DSTileset4 as _DSTileset4
from ....ds.mod_DSSerial import\
    DSSerial as _DSSerial

from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert

class _HHCmdConvert(_HCmdConvert):
    def _main(self, creator: _Creator):
        idata = _cast(_DSTileset4, self._data)
        odata = _DSSerial.tileset4_to_bin(idata)
        creator.set_var(self._ovar, odata)

type _type = _DSTileset4
def _create(data, ovar): return _HHCmdConvert(data, ovar)