all = []

from sys import\
    stderr as _stderr
from typing import\
    cast as _cast

from ...cli.mod_CLIParseUtil import\
    CLIParseUtil as _CLIParseUtil
from ...cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef
from ...data.mod_DataBuffer import\
    DataBuffer as _DataBuffer
from ...ds.mod_DSSerial import\
    DSSerial as _DSSerial
from ...ds.mod_DSTileset import\
    DSTileset as _DSTileset
from ...ds.mod_DSUtil import\
    DSUtil as _DSUtil
from ...img.mod_ImgImage import\
    ImgImage as _ImgImage
from ...img.mod_ImgPalette import\
    ImgPalette as _ImgPalette

from ..mod__call import _CmdDef
from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator
from .c__HCmdConvert import _HCmdConvert

def tobpp(input:str):
    passs, value = _CLIParseUtil.to_int(input)
    if not passs: return False, 0
    if value != 4 and value != 8:
        print(f"{value} is not valid for the bits-per-pixel.", file = _stderr)
        return False, 0
    return True, value

class _HHCmd(_HCmdConvert[_DSTileset]):
    __bpp = _CLIRequiredDef(name = "bpp", parse = tobpp)
    @property
    def _create(self):
        return self.__create
    def __init__(self):
        super().__init__()
        self.__create:dict[type, _HCmdConvert._TCreate] = {}
        # ImgImage
        def _create_ImgImage(cmd:_HCmdConvert[_DSTileset], input:object):
            _input = _cast(_ImgImage, input)
            cmd_bpp = _cast(int, cmd.bpp) # type: ignore
            if cmd_bpp == 4:
                return _DSUtil.tileset4_get_img(_input)
            return _DSUtil.tileset8_get_img(_input)
        self.__create[_ImgImage] = _create_ImgImage

def __cmd(creator:_Creator, argv:list[str]):
    _HHCmd().execute(creator, argv)

__def = _CmdDef(__cmd)