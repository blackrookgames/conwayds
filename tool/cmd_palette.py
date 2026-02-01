import numpy
import sys

from typing import cast

import src.cli as cli
import src.img as img

from abs_cpp import abs_cpp

class cmd_palette(abs_cpp):

    @property
    def _desc(self) -> None|str:
        return "Creates a palette from an image."

    #region required

    __input = abs_cpp._input()
    __output = abs_cpp._output()

    #endregion

    #region optional

    __itype = abs_cpp._itype(cli.helper.DSCLIFormat)
    __otype = abs_cpp._otype(cli.helper.DSCLIFormat)

    #endregion

    #region methods

    def _main(self):
        self_input = cast(str, self.input) # type: ignore
        self_output = cast(str, self.output) # type: ignore
        self_itype = cast(None|cli.helper.DSCLIFormat, self.itype) # type: ignore
        self_otype = cast(None|cli.helper.DSCLIFormat, self.otype) # type: ignore
        # Input
        palette = cli.helper.DSCLI.palette_load_img(self_input)
        if palette is None: return 1
        # Output
        result = cli.helper.DSCLI.palette_save_img(palette, self_output)
        if not result: return 1
        # Success!!!
        return 0

    #endregion

sys.exit(cmd_palette().execute(sys.argv))