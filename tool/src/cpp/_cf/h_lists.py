all = []

from collections.abc import\
    Collection as _Collection
from typing import\
    Callable as _Callable,\
    NamedTuple as _NamedTuple

from ...cliutil.mod_CLIListUtil import\
    CLIListUtil as _CLIListUtil

class _ListIO(_NamedTuple):
    load:_Callable[[str], list]
    save:_Callable[[_Collection, str], None]

class _UniList(_NamedTuple):
    listtype:str
    listitems:list

_LISTTYPES = {\
    'uint8': _ListIO(_CLIListUtil.uint8_from_file, _CLIListUtil.uint8_to_file),\
    'int8': _ListIO(_CLIListUtil.int8_from_file, _CLIListUtil.int8_to_file),\
    'uint16': _ListIO(_CLIListUtil.uint16_from_file, _CLIListUtil.uint16_to_file),\
    'int16': _ListIO(_CLIListUtil.int16_from_file, _CLIListUtil.int16_to_file),\
    'uint32': _ListIO(_CLIListUtil.uint32_from_file, _CLIListUtil.uint32_to_file),\
    'int32': _ListIO(_CLIListUtil.int32_from_file, _CLIListUtil.int32_to_file),\
    'uint64': _ListIO(_CLIListUtil.uint64_from_file, _CLIListUtil.uint64_to_file),\
    'int64': _ListIO(_CLIListUtil.int64_from_file, _CLIListUtil.int64_to_file),\
    'uint8': _ListIO(_CLIListUtil.uint8_from_file, _CLIListUtil.uint8_to_file),}