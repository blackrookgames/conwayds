all = []

from typing import\
    cast as _cast

from ....cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef
from ....data.mod_SerialError import\
    SerialError as _SerialError
from ....life.mod_LifeSerial import\
    LifeSerial as _LifeSerial

from ...mod__CmdFuncError import _CmdFuncError
from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert

class _HHCmdConvert(_HCmdConvert):
    __type = _CLIRequiredDef(name = "type")
    def _main(self, creator: _Creator):
        try:
            # Determine type
            self_type = _cast(str, self.type) # type: ignore
            match self_type.lower():
                case "txt": rle = False
                case "rle": rle = True
                case _: raise _CmdFuncError(f"Unknown type: {self_type}")
            # Convert
            idata = _cast(str, self._data)
            odata = _LifeSerial.pattern_from_rle(idata) if rle\
                else _LifeSerial.pattern_from_txt(idata)
            # Save
            creator.set_var(self._ovar, odata)
            # Success!!!
            return
        except _SerialError as _e:
            e = _CmdFuncError(_e)
        raise e

type _type = str
def _create(data, ovar): return _HHCmdConvert(data, ovar)