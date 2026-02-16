all = []

from typing import\
    Callable as _Callable,\
    cast as _cast

from ...cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef

from ..mod__call import _FuncDef
from ..mod__Creator import _Creator
from .f__HFuncGet import _HFuncGet

from ...ds.mod_DSBitmap import\
    DSBitmap as _DSBitmap
from ...img.mod_ImgImage import\
    ImgImage as _ImgImage

def _get(obj:object): return str(obj.width) # type: ignore

_DICT:dict[type, _Callable[[object], str]] =\
{\
    _DSBitmap: _get,\
    _ImgImage: _get,\
}

class _HHFunc(_HFuncGet):
    @property
    def _propname(self): return "width"
    @property
    def _gets(self): return _DICT

def __func(creator:_Creator, argv:list[str]):
    return _HHFunc().execute(creator, argv)

__def = _FuncDef(__func)