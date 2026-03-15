all = []

from typing import\
    cast as _cast

from ....cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef
from ....cliutil.mod_CLICommandError import\
    CLICommandError as _CLICommandError

from ...mod__CmdFuncError import _CmdFuncError
from ...mod__Creator import _Creator
from ..h_lists import _UniList, _LISTTYPES
from .c__HCmdLoad import _HCmdLoad

class _HHCmdLoad(_HCmdLoad):
    __type = _CLIRequiredDef(name = "type")
    def _main(self, creator: _Creator):
        try:
            self_outvar = _cast(str, self.outvar) # type: ignore
            self_path = _cast(str, self.path) # type: ignore
            self_type = _cast(str, self.type) # type: ignore
            path = creator.resolvepath(self_path)
            listtype = self_type.lower()
            if not (listtype in _LISTTYPES): raise _CmdFuncError(f"Invalid item type: {listtype}")
            creator.set_var(self_outvar, _UniList(listtype, _LISTTYPES[listtype].load(path)))
            return
        except _CLICommandError as _e:
            e = _CmdFuncError(_e)
        raise e

def _create(): return _HHCmdLoad()