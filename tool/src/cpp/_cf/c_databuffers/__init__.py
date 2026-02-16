from typing import Callable as _Callable
from ..c__HCmdConvert import _HCmdConvert
from .c_databuffer_dsbitmap16 import _create as _create_dsbitmap16, _type as _type_dsbitmap16
from .c_databuffer_dsbitmap8 import _create as _create_dsbitmap8, _type as _type_dsbitmap8
from .c_databuffer_dspalette import _create as _create_dspalette, _type as _type_dspalette
from .c_databuffer_dstileset4 import _create as _create_dstileset4, _type as _type_dstileset4
from .c_databuffer_dstileset8 import _create as _create_dstileset8, _type as _type_dstileset8
# Sub-commands
__DICT:dict[type, _Callable[[object, str], _HCmdConvert]] = {
    _type_dsbitmap16.__value__: _create_dsbitmap16,
    _type_dsbitmap8.__value__: _create_dsbitmap8,
    _type_dspalette.__value__: _create_dspalette,
    _type_dstileset4.__value__: _create_dstileset4,
    _type_dstileset8.__value__: _create_dstileset8,
}
