all = ['run']
from .mod__Creator import _Creator
from .mod__call import _CmdDef, _FuncDef
from ._cf.c_close import __def as _c_close
from ._cf.c_databuffer import __def as _c_databuffer
from ._cf.c_dspalette import __def as _c_dspalette
from ._cf.c_dstileset import __def as _c_dstileset
from ._cf.c_imgimage import __def as _c_imgimage
from ._cf.c_line import __def as _c_line
from ._cf.c_load import __def as _c_load
from ._cf.c_open import __def as _c_open
from ._cf.c_print import __def as _c_print
from ._cf.c_save import __def as _c_save
from ._cf.c_var import __def as _c_var
from ._cf.f_cppdata import __def as _f_cppdata
from ._cf.f_cppsize import __def as _f_cppsize
from ._cf.f_type import __def as _f_type
# Commands
_CMDS:dict[str, _CmdDef] = {
    '@close': _c_close,
    '@databuffer': _c_databuffer,
    '@dspalette': _c_dspalette,
    '@dstileset': _c_dstileset,
    '@imgimage': _c_imgimage,
    '@line': _c_line,
    '@load': _c_load,
    '@open': _c_open,
    '@print': _c_print,
    '@save': _c_save,
    '@var': _c_var,
}
# Functions
_FUNCS:dict[str, _FuncDef] = {
    'cppdata': _f_cppdata,
    'cppsize': _f_cppsize,
    'type': _f_type,
}
# Run
def run(fpath:str, dpath:str):
    """
    Creates C++ sources.
    
    :param fpath:
        Path of configuration file
    :param dpath:
        Path of working directory
    :raise CLICommandError:
        An error occurred
    """
    _Creator.run(fpath, dpath, _CMDS, _FUNCS)
