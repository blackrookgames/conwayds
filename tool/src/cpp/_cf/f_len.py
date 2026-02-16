all = []

from typing import\
    Callable as _Callable,\
    cast as _cast

from ...cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef

from ..mod__call import _FuncDef
from ..mod__Creator import _Creator
from .f__HFuncGet import _HFuncGet

from ...data.mod_DataBuffer import\
    DataBuffer as _DataBuffer
from ...ds.mod_DSTileset import\
    DSTileset as _DSTileset

def _get(obj:object): return str(len(obj)) # type: ignore

_DICT:dict[type, _Callable[[object], str]] =\
{\
    _DataBuffer: _get,\
    _DSTileset: _get,\
}

class _HHFunc(_HFuncGet):
    @property
    def _propname(self): return "len"
    @property
    def _gets(self): return _DICT

def __func(creator:_Creator, argv:list[str]):
    return _HHFunc().execute(creator, argv)

__def = _FuncDef(__func)