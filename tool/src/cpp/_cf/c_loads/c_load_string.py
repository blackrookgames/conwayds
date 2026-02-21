all = []

from typing import\
    cast as _cast

from ....cliutil.mod_CLIStrUtil import\
    CLIStrUtil as _CLIStrUtil
from ....cliutil.mod_CLICommandError import\
    CLICommandError as _CLICommandError

from ...mod__CmdFuncError import _CmdFuncError
from ...mod__Creator import _Creator
from .c__HCmdLoad import _HCmdLoad

class _HHCmdLoad(_HCmdLoad):
    def _main(self, creator: _Creator):
        try:
            self_outvar = _cast(str, self.outvar) # type: ignore
            self_path = _cast(str, self.path) # type: ignore
            path = creator.resolvepath(self_path)
            data = _CLIStrUtil.str_from_file(path)
            creator.set_var(self_outvar, data)
            return
        except _CLICommandError as _e:
            e = _CmdFuncError(_e)
        raise e

def _create(): return _HHCmdLoad()