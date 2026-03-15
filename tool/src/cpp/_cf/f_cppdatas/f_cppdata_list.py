all = []

from io import\
    StringIO as _StringIO
from typing import\
    Callable as _Callable,\
    cast as _cast

from ....data.mod_DataBuffer import\
    DataBuffer as _DataBuffer

from ...mod__CmdFuncError import _CmdFuncError
from ...mod__Creator import _Creator
from ..h_lists import _UniList, _LISTTYPES
from .f__HFuncCppData import _HFuncCppData

def _str_int(obj:object, hexdigits:int):
    pad = '0' * hexdigits
    wrap = 1 << (hexdigits * 4)
    return "0x" + (pad + hex(wrap + _cast(int, obj)))[-hexdigits:]

_SUPPORTED = {\
    'uint8': lambda _obj: _str_int(_obj, 2),\
    'int8': lambda _obj: _str_int(_obj, 2),\
    'uint16': lambda _obj: _str_int(_obj, 4),\
    'int16': lambda _obj: _str_int(_obj, 4),\
    'uint32': lambda _obj: _str_int(_obj, 8),\
    'int32': lambda _obj: _str_int(_obj, 8),\
    'uint64': lambda _obj: _str_int(_obj, 16),\
    'int64': lambda _obj: _str_int(_obj, 16)}

class _HHFuncCppData(_HFuncCppData):
    def _main(self, creator: _Creator):
        # Get data
        data = _cast(_UniList, self._data)
        if not (data.listtype in _SUPPORTED): 
            raise _CmdFuncError(f"Cannot create C++ code out of {data.listtype} list.")
        tostr = _SUPPORTED[data.listtype]
        # Create string
        if len(data) == 0:
            return "{ }"
        with _StringIO() as _strio:
            # Opening bracket
            _strio.write("{\n")
            # Data
            _i = 0
            while _i < len(data.listitems):
                # Indent?
                if (_i % 16) == 0:
                    _strio.write("    ")
                # Write byte
                _strio.write(f"{tostr(data.listitems[_i])}, ")
                # Next
                _i += 1
                # Newline?
                if _i == len(data.listitems) or (_i % 16) == 0:
                    _strio.write('\n')
            # Closing bracket (no newline)
            _strio.write("}")
            # Success!!!
            return _strio.getvalue()

type _type = _UniList
def _create(data): return _HHFuncCppData(data)