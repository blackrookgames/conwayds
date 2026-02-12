from typing import Callable as _Callable
from .c__HCmdSave import _HCmdSave
from .c_save_databuffer import _create as _create_databuffer, _type as _type_databuffer
from .c_save_imgimage import _create as _create_imgimage, _type as _type_imgimage
# Sub-commands
__DICT:dict[type, _Callable[[object], _HCmdSave]] = {
    _type_databuffer.__value__: _create_databuffer,
    _type_imgimage.__value__: _create_imgimage,
}
