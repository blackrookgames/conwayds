all = []

from typing import\
    cast as _cast

from ...data.mod_DataBuffer import\
    DataBuffer as _DataBuffer
from ...ds.mod_DSPalette import\
    DSPalette as _DSPalette
from ...ds.mod_DSSerial import\
    DSSerial as _DSSerial

from ..mod__call import _CmdDef
from ..mod__Creator import _Creator
from .mod___HCmdConvert import _HCmdConvert

class _HHCmd(_HCmdConvert[_DataBuffer]):
    @property
    def _create(self):
        return self.__create
    def __init__(self):
        super().__init__()
        self.__create:dict[type, _HCmdConvert._TCreate] = {}
        # DSPalette
        def _create_DSPalette(cmd:_HCmdConvert[_DataBuffer], input:object):
            return _DSSerial.palette_to_bin(_cast(_DSPalette, input))
        self.__create[_DSPalette] = _create_DSPalette

def __cmd(creator:_Creator, argv:list[str]):
    _HHCmd().execute(creator, argv)

__def = _CmdDef(__cmd)