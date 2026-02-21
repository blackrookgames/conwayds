from typing import Callable as _Callable
from ..c__HCmdConvert import _HCmdConvert
from .c_string_lifepattern import _create as _create_lifepattern, _type as _type_lifepattern
# Sub-commands
__DICT:dict[type, _Callable[[object, str], _HCmdConvert]] = {
    _type_lifepattern.__value__: _create_lifepattern,
}
