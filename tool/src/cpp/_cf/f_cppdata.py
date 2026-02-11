all = []

from io import\
    StringIO as _StringIO
from typing import\
    cast as _cast

from ...cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef
from ...data.mod_DataBuffer import\
    DataBuffer as _DataBuffer

from ..mod__call import _FuncDef
from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator
from .f__HFunc import _HFunc

class _HHFunc(_HFunc):
    __varname = _CLIRequiredDef(name = "varname")
    def _main(self, creator: _Creator):
        self_varname = _cast(str, self.varname) # type: ignore
        # Get data
        data = creator.get_var(self_varname, types = _DataBuffer)
        data = _cast(_DataBuffer, data)
        # Create string
        if len(data) == 0:
            return "{ }"
        with _StringIO() as _strio:
            # Opening bracket
            _strio.write("{\n")
            # Data
            _i = 0
            while _i < len(data):
                # Indent?
                if (_i % 16) == 0:
                    _strio.write("    ")
                # Write byte
                _strio.write(f"0x{data[_i]:02X}, ")
                # Next
                _i += 1
                # Newline?
                if _i == len(data) or (_i % 16) == 0:
                    _strio.write('\n')
            # Closing bracket (no newline)
            _strio.write("}")
            # Success!!!
            return _strio.getvalue()

def __func(creator:_Creator, argv:list[str]):
    return _HHFunc().execute(creator, argv)

__def = _FuncDef(__func)