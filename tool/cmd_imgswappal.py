import numpy
import sys

from enum import auto, Enum
from typing import cast

import src.cli as cli
import src.cliutil as cliutil
import src.img as img

class cmd_imgswappal(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Swaps the palette of a paletted image"

    #region required

    __input = cli.CLIRequiredDef(\
        name = "input",\
        desc = "Path to the input file")
    __palette = cli.CLIRequiredDef(\
        name = "palette",\
        desc = "Path to the palette file")
    __output = cli.CLIRequiredDef(\
        name = "output",\
        desc = "Path to the output file")

    #endregion

    #region methods

    def _main(self):
        try:
            self_input = cast(str, self.input) # type: ignore
            self_palette = cast(str, self.palette) # type: ignore
            self_output = cast(str, self.output) # type: ignore
            # Open image
            img_image = cliutil.CLIImgUtil.image_from_file(self_input)
            if not img_image.haspalette:
                raise cliutil.CLICommandError("Input image must have a palette.")
            # Open palette
            img_palette = cliutil.CLIImgUtil.image_from_file(self_palette)
            if not img_palette.haspalette:
                raise cliutil.CLICommandError("Palette image must have a palette.")
            # Swap palette
            pal_input = cast(img.ImgPalette, img_image.palette)
            pal_palette = cast(img.ImgPalette, img_palette.palette)
            pal_input.format(size = len(pal_palette))
            for _i in range(len(pal_palette)):
                pal_input[_i] = pal_palette[_i]
            # Save image
            cliutil.CLIImgUtil.image_to_file(img_image, self_output)
        except cliutil.CLICommandError as e:
            print(f"ERROR: {e}", file = sys.stderr)
            return 1
        return 0

    #endregion

sys.exit(cmd_imgswappal().execute(sys.argv))