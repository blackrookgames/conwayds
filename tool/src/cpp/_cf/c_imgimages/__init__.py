from typing import Callable as _Callable
from ..c__HCmdConvert import _HCmdConvert
from .c_imgimage_dstileset4 import _create as _create_dstileset4, _type as _type_dstileset4
from .c_imgimage_dstileset8 import _create as _create_dstileset8, _type as _type_dstileset8
# Sub-commands
__DICT:dict[type, _Callable[[object, str], _HCmdConvert]] = {
    _type_dstileset4.__value__: _create_dstileset4,
    _type_dstileset8.__value__: _create_dstileset8,
}
