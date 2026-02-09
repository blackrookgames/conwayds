all = [\
    'run',]

from .mod__Creator import _Creator
from .mod__call import _CmdDef, _FuncDef

from ._cmds.mod__databuffer import __def as _cmd_databuffer
from ._cmds.mod__dspalette import __def as _cmd_dspalette
from ._cmds.mod__dstileset import __def as _cmd_dstileset
from ._cmds.mod__imgimage import __def as _cmd_imgimage
from ._cmds.mod__print import __def as _cmd_print
from ._cmds.mod__var import __def as _cmd_var
from ._funcs.mod__type import __def as _func_type

_CMDS:dict[str, _CmdDef] = {
    "@databuffer": _cmd_databuffer,
    "@dspalette": _cmd_dspalette,
    "@dstileset": _cmd_dstileset,
    "@imgimage": _cmd_imgimage,
    "@print": _cmd_print,
    "@var": _cmd_var,
}

_FUNCS:dict[str, _FuncDef] = {
    "type": _func_type,
}

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