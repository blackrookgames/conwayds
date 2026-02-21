all = []

from typing import\
    cast as _cast

from ....cliutil.mod_CLIStrUtil import\
    CLIStrUtil as _CLIStrUtil
from ....cliutil.mod_CLICommandError import\
    CLICommandError as _CLICommandError

from ...mod__CmdFuncError import _CmdFuncError
from ...mod__Creator import _Creator
from .c__HCmdSave import _HCmdSave

class _HHCmdSave(_HCmdSave):
    def _main(self, creator: _Creator):
        try:
            self_path = _cast(str, self.path) # type: ignore
            path = creator.resolvepath(self_path)
            data = _cast(str, self._data)
            _CLIStrUtil.str_to_file(data, path)
            return
        except _CLICommandError as _e:
            e = _CmdFuncError(_e)
        raise e

type _type = str
def _create(data): return _HHCmdSave(data)