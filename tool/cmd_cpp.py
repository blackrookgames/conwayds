import sys

from pathlib import Path
from typing import cast

import src.cli as cli
import src.cliutil as cliutil
import src.cpp as cpp

class cmd_cpp(cli.CLICommand):

    @property
    def _desc(self):
        return "Creates C++ source files"

    #region required

    __config = cli.CLIRequiredDef(\
        name = "config",\
        desc = "Path to the configuration file")

    #endregion

    #region helper methods

    @classmethod
    def __evalpath(cls, path:str):
        try:
            fpath = Path(path)
            dpath = fpath.parent
            return fpath, dpath
        except Exception as _e:
            e = cliutil.CLICommandError(_e)
        raise e

    #endregion

    #region methods

    def _main(self):
        try:
            self_config = cast(str, self.config) # type: ignore
            fpath, dpath = self.__evalpath(self_config)
            cpp.Creator.run(str(fpath), str(dpath))
            return 0
        except cliutil.CLICommandError as e:
            print(f"ERROR: {e}", file = sys.stderr)
        return 1

    #endregion

if __name__ == '__main__':
    sys.exit(cmd_cpp().execute(sys.argv))