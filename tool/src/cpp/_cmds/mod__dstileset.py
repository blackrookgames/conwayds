all = []

from typing import\
    cast as _cast

from ...data.mod_Text import\
    Text as _Text
from ...ds.mod_DSUtil import\
    DSUtil as _DSUtil
from ...img.mod_ImgImage import\
    ImgImage as _ImgImage
from ...img.mod_ImgPalette import\
    ImgPalette as _ImgPalette

from ..mod__call import _CmdDef
from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator

def __cmd(creator:_Creator, argv:list[_Text]):
    if len(argv) <= 3:
        raise _CmdFuncError("Expected an output variable name, input variable name, and bpp.")
    # Output variable
    output = argv[1]
    # Input variable
    input = creator.get_var(argv[2])
    if not isinstance(input, _ImgImage):
        raise _CmdFuncError(f"{input} is not an image.")
    if not input.haspalette:
        raise _CmdFuncError(f"{input} does not contain a palette.")
    # BPP
    bpp = argv[3]
    # Create
    if bpp == '4': data = _DSUtil.tileset4_get_img(input)
    elif bpp == '8': data = _DSUtil.tileset8_get_img(input)
    else: raise _CmdFuncError(f"{bpp} is not valid for bits-per-pixel.")
    creator.set_var(output, data)

__def = _CmdDef(__cmd)