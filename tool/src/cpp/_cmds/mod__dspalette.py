all = []

from typing import\
    cast as _cast

from ...data.mod_DataBuffer import\
    DataBuffer as _DataBuffer
from ...ds.mod_DSPalette import\
    DSPalette as _DSPalette
from ...ds.mod_DSSerial import\
    DSSerial as _DSSerial
from ...ds.mod_DSUtil import\
    DSUtil as _DSUtil
from ...img.mod_ImgImage import\
    ImgImage as _ImgImage
from ...img.mod_ImgPalette import\
    ImgPalette as _ImgPalette

from ..mod__call import _CmdDef
from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator
from .mod___HCmdConvert import _HCmdConvert

class _HHCmd(_HCmdConvert[_DSPalette]):
    @property
    def _create(self):
        return self.__create
    def __init__(self):
        super().__init__()
        self.__create:dict[type, _HCmdConvert._TCreate] = {}
        # DataBuffer
        def _create_DataBuffer(cmd:_HCmdConvert[_DSPalette], input:object):
            return _DSSerial.palette_from_bin(_cast(_DataBuffer, input))
        self.__create[_DataBuffer] = _create_DataBuffer
        # ImgImage
        def _create_ImgImage(cmd:_HCmdConvert[_DSPalette], input:object):
            _input = _cast(_ImgImage, input)
            if not _input.haspalette:
                raise _CmdFuncError(f"{input} does not contain a palette.")
            return _DSUtil.palette_get_pal(_cast(_ImgPalette, _input.palette))
        self.__create[_ImgImage] = _create_ImgImage

def __cmd(creator:_Creator, argv:list[str]):
    _HHCmd().execute(creator, argv)

__def = _CmdDef(__cmd)