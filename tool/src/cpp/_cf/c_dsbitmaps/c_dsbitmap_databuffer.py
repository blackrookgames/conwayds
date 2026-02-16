all = []

from sys import\
    stderr as _stderr
from typing import\
    cast as _cast

from ....cli.mod_CLIParseUtil import\
    CLIParseUtil as _CLIParseUtil
from ....cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef
from ....data.mod_DataBuffer import\
    DataBuffer as _DataBuffer
from ....ds.mod_DSSerial import\
    DSSerial as _DSSerial

from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert
from .c__common import _tobpp

class _HHCmdConvert(_HCmdConvert):
    __width = _CLIRequiredDef("width", parse = _CLIParseUtil.to_uint32)
    __height = _CLIRequiredDef("height", parse = _CLIParseUtil.to_uint32)
    __bpp = _CLIRequiredDef(name = "bpp", parse = _tobpp)
    def _main(self, creator: _Creator):
        self_width = int(self.width) # type: ignore
        self_height = int(self.height) # type: ignore
        self_bpp = _cast(int, self.bpp) # type: ignore
        idata = _cast(_DataBuffer, self._data)
        odata = _DSSerial.bitmap8_from_bin(idata, self_width, self_height) if (self_bpp == 8)\
            else _DSSerial.bitmap16_from_bin(idata, self_width, self_height)
        creator.set_var(self._ovar, odata)

type _type = _DataBuffer
def _create(data, ovar): return _HHCmdConvert(data, ovar)