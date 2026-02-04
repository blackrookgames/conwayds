import numpy
import sys

from enum import auto, Enum
from typing import cast

import src.cli as cli
import src.cliutil as cliutil
import src.img as img

class cmd_imgwpal(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Converts an image to a paletted image."

    #region required

    __input = cli.CLIRequiredDef(\
        name = "input",\
        desc = "Path to the input file")
    __output = cli.CLIRequiredDef(\
        name = "output",\
        desc = "Path to the output file")

    #endregion

    #region optional

    __noalpha = cli.CLIOptionFlagDef(\
        name = "noalpha",\
        short = 'A',\
        desc = "Whether or not to forget alpha information")

    #endregion

    #region methods

    def _main(self):
        try:
            self_input = cast(str, self.input) # type: ignore
            self_output = cast(str, self.output) # type: ignore
            self_noalpha = cast(bool, self.noalpha) # type: ignore
            # Input
            srcimg = cliutil.CLIImgUtil.image_from_file(self_input)
            # Output
            outimg = img.ImgUtil.image_pal(srcimg)
            if self_noalpha: outimg.alpha = False
            cliutil.CLIImgUtil.image_to_file(outimg, self_output)
        except cliutil.CLICommandError as e:
            print(f"ERROR: {e}", file = sys.stderr)
            return 1
        return 0

    #endregion

sys.exit(cmd_imgwpal().execute(sys.argv))