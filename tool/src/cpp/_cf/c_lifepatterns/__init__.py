from typing import Callable as _Callable
from ..c__HCmdConvert import _HCmdConvert
from .c_lifepattern_databuffer import _create as _create_databuffer, _type as _type_databuffer
from .c_lifepattern_imgimage import _create as _create_imgimage, _type as _type_imgimage
from .c_lifepattern_string import _create as _create_string, _type as _type_string
# Sub-commands
__DICT:dict[type, _Callable[[object, str], _HCmdConvert]] = {
    _type_databuffer.__value__: _create_databuffer,
    _type_imgimage.__value__: _create_imgimage,
    _type_string.__value__: _create_string,
}
