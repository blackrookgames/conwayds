all = []

from ....cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef

from ..f__HFunc import _HFunc

class _HFuncCppData(_HFunc):
    def __init__(self, data:object):
        super().__init__()
        self.__data = data
    @property
    def _data(self): return self.__data