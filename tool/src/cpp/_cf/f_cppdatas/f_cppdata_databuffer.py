all = []

from io import\
    StringIO as _StringIO
from typing import\
    cast as _cast

from ....data.mod_DataBuffer import\
    DataBuffer as _DataBuffer

from ...mod__Creator import _Creator
from .f__HFuncCppData import _HFuncCppData

class _HHFuncCppData(_HFuncCppData):
    def _main(self, creator: _Creator):
        # Get data
        data = _cast(_DataBuffer, self._data)
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

type _type = _DataBuffer
def _create(data): return _HHFuncCppData(data)