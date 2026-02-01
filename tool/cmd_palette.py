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
        palette = cast(None|img.Img, cli.helper.DSCLI.palette_load_img(self.input))
        if palette is None: return 1
        result = cli.helper.DSCLI.palette_save_img(palette, self.output)
        if not result: return 1
        return 0

    #endregion

sys.exit(cmd_palette().execute(sys.argv))