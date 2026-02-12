all = []

from typing import\
    cast as _cast

from ....cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef
from ....data.mod_DataBuffer import\
    DataBuffer as _DataBuffer
from ....ds.mod_DSSerial import\
    DSSerial as _DSSerial

from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert
from .c__common import __tobpp as p__tobpp

class _HHCmdConvert(_HCmdConvert):
    __bpp = _CLIRequiredDef(name = "bpp", parse = p__tobpp)
    def _main(self, creator: _Creator):
        self_bpp = _cast(int, self.bpp) # type: ignore
        idata = _cast(_DataBuffer, self._data)
        odata = _DSSerial.tileset4_from_bin(idata) if (self_bpp == 4)\
            else _DSSerial.tileset8_from_bin(idata)
        creator.set_var(self._ovar, odata)

type _type = _DataBuffer
def _create(data, ovar): return _HHCmdConvert(data, ovar)