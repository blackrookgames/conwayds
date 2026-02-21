all = []

from typing import\
    cast as _cast

from ....data.mod_DataBuffer import\
    DataBuffer as _DataBuffer
from ....data.mod_SerialError import\
    SerialError as _SerialError
from ....img.mod_ImgImage import\
    ImgImage as _ImgImage
from ....life.mod_LifePattern import\
    LifePattern as _LifePattern
from ....life.mod_LifeSerial import\
    LifeSerial as _LifeSerial

from ...mod__CmdFuncError import _CmdFuncError
from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert

class _HHCmdConvert(_HCmdConvert):
    def _main(self, creator: _Creator):
        try:
            idata = _cast(_LifePattern, self._data)
            odata = _LifeSerial.pattern_to_bin(idata)
            creator.set_var(self._ovar, odata)
            return
        except _SerialError as _e:
            e = _CmdFuncError(_e)
        raise e

type _type = _LifePattern
def _create(data, ovar): return _HHCmdConvert(data, ovar)