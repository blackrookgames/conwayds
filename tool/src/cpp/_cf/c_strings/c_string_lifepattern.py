all = []

from typing import\
    cast as _cast

from ....cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef
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
    __type = _CLIRequiredDef(name = "type")
    def _main(self, creator: _Creator):
        # Determine type
        self_type = _cast(str, self.type) # type: ignore
        match self_type.lower():
            case "txt": rle = False
            case "rle": rle = True
            case _: raise _CmdFuncError(f"Unknown type: {self_type}")
        # Convert
        idata = _cast(_LifePattern, self._data)
        odata = _LifeSerial.pattern_to_rle(idata) if rle\
            else _LifeSerial.pattern_to_txt(idata)
        # Save
        creator.set_var(self._ovar, odata)

type _type = _LifePattern
def _create(data, ovar): return _HHCmdConvert(data, ovar)