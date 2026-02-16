from typing import Callable as _Callable
from ..c__HCmdConvert import _HCmdConvert
from .c_dsbitmap_databuffer import _create as _create_databuffer, _type as _type_databuffer
from .c_dsbitmap_imgimage import _create as _create_imgimage, _type as _type_imgimage
# Sub-commands
__DICT:dict[type, _Callable[[object, str], _HCmdConvert]] = {
    _type_databuffer.__value__: _create_databuffer,
    _type_imgimage.__value__: _create_imgimage,
}
