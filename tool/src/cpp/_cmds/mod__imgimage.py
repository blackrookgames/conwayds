all = []

from ...cliutil.mod_CLICommandError import\
    CLICommandError as _CLICommandError
from ...cliutil.mod_CLIImgUtil import\
    CLIImgUtil as _CLIImgUtil
from ...data.mod_Text import\
    Text as _Text

from ..mod__call import _CmdDef
from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator

def __cmd(creator:_Creator, argv:list[_Text]):
    try:
        if len(argv) <= 2:
            raise _CLICommandError("Expected variable name and input filepath.")
        variable = argv[1]
        path = creator.resolvepath(argv[2])
        creator.set_var(variable, _CLIImgUtil.image_from_file(str(path)))
        return
    except _CLICommandError as _e:
        e = _CmdFuncError(_e)
    raise e

__def = _CmdDef(__cmd)