all = []

from typing import\
    cast as _cast

from ...data.mod_Text import\
    Text as _Text
from ...ds.mod_DSPalette import\
    DSPalette as _DSPalette
from ...ds.mod_DSSerial import\
    DSSerial as _DSSerial

from ..mod__call import _CmdDef
from ..mod__CmdFuncError import _CmdFuncError
from ..mod__Creator import _Creator

def __cmd(creator:_Creator, argv:list[_Text]):
    if len(argv) <= 2:
        raise _CmdFuncError("Expected an output variable name and an input variable name.")
    # Output variable
    output = argv[1]
    # Input variable
    input = creator.get_var(argv[2])
    # Create
    if isinstance(input, _DSPalette):
        data = _DSSerial.palette_to_bin(input)
    else:
        raise _CmdFuncError(f"Cannot create a databuffer out of {type(input).__name__}.")
    creator.set_var(output, data)
    return

__def = _CmdDef(__cmd)