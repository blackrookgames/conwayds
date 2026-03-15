from typing import Callable as _Callable
from .f__HFuncCppData import _HFuncCppData
from .f_cppdata_databuffer import _create as _create_databuffer, _type as _type_databuffer
from .f_cppdata_list import _create as _create_list, _type as _type_list
# Sub-commands
__DICT:dict[type, _Callable[[object], _HFuncCppData]] = {
    _type_databuffer.__value__: _create_databuffer,
    _type_list.__value__: _create_list,
}
