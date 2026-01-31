import numpy
import sys

from typing import cast

import src.cli as cli
import src.ds as ds
import src.gb as gb
import src.data as data
import src.img as img

class cmd_palette(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Creates a palette from an image."

    #region required

    __input = cli.CLIRequiredDef(\
        name = "input",\
        desc = "Path to the input file")
    __output = cli.CLIRequiredDef(\
        name = "output",\
        desc = "Path to the output *.bin file")

    #endregion

    #region methods

    def _main(self):
        # Open input
        input = cast(None|img.Img, cli.helper.ImgUtil.load(self.input))
        if input is None:
            return 1
        # Palette
        palette = ds.DSPaletteUtil.from_img(input)
        # Test
        output = ds.DSPaletteUtil.to_img(palette)
        if not cli.helper.ImgUtil.save(output, self.output):
            return 1
        # Success
        return 0

    #endregion

sys.exit(cmd_palette().execute(sys.argv))