all = []

from typing import\
    cast as _cast

from ...cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef
from ...data.mod_DataBuffer import\
    DataBuffer as _DataBuffer

from ..mod__call import _FuncDef
from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator

from .f_cppdatas import __DICT
from .h_helper import _tryfindtype

def __func(creator:_Creator, argv:list[str]):
    if len(argv) <= 1:
        raise _CmdFuncError("Not enough arguments")
    data = creator.get_var(argv[1])
    dtype = type(data)
    found, func = _tryfindtype(__DICT, dtype)
    if not found:
        raise _CmdFuncError(f"Cannot create C++ code out of {dtype.__name__} data.")
    assert func is not None
    savefunc = func(data)
    return savefunc.execute(creator, [argv[_i] for _i in range(1, len(argv))])

__def = _FuncDef(__func)