import numpy
import sys

from enum import auto, Enum
from typing import cast

import src.cli as cli
import src.cliutil as cliutil
import src.img as img

class cmd_image(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Converts an image."

    #region required

    __input = cli.CLIRequiredDef(\
        name = "input",\
        desc = "Path to the input file")
    __output = cli.CLIRequiredDef(\
        name = "output",\
        desc = "Path to the output file")

    #endregion

    #region optional

    __palette = cli.CLIOptionWArgDef(\
        name = "palette",\
        short = 'p',\
        desc = "Path for palette swapping; useless if input image does not have a palette",\
        default = None)

    #endregion

    #region methods

    def _main(self):
        try:
            self_input = cast(str, self.input) # type: ignore
            self_output = cast(str, self.output) # type: ignore
            self_palette = cast(None|str, self.palette) # type: ignore
            # Input
            ima = cliutil.CLIImgUtil.image_from_file(self_input)
            # Palette
            if ima.haspalette and self_palette is not None:
                pal = cliutil.CLIImgUtil.image_from_file(self_palette)
                if not pal.haspalette:
                    raise cliutil.CLICommandError("Palette image does not contain a palette")
                pal_palette = cast(img.ImgPalette, pal.palette)
                img_palette = cast(img.ImgPalette, ima.palette)
                img_palette.resize(len(pal_palette))
                for _i in range(len(pal_palette)):
                    img_palette[_i] = pal_palette[_i]
            # Output
            cliutil.CLIImgUtil.image_to_file(ima, self_output)
        except cliutil.CLICommandError as e:
            print(f"ERROR: {e}", file = sys.stderr)
            return 1
        return 0

    #endregion

sys.exit(cmd_image().execute(sys.argv))