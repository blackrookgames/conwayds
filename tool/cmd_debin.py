import numpy
import sys

from io import StringIO
from typing import cast

import src.cli as cli
import src.cliutil as cliutil
import src.data as data
import src.img as img

TILESIZE = 8

class cmd_debin(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Decode a binary file to a text file."

    #region required

    __input = cli.CLIRequiredDef(\
        name = "input",\
        desc = "Path to the input binary file")
    __output = cli.CLIRequiredDef(\
        name = "output",\
        desc = "Path to the output text file")

    #endregion

    #region optional

    __bare = cli.CLIOptionFlagDef(\
        name = "bare",\
        short = 'b',\
        desc = "If specified, output file will contain no comments with additional information")

    #endregion

    #region methods

    def _main(self):
        try:
            self_input = cast(str, self.input) # type: ignore
            self_bare = cast(bool, self.bare) # type: ignore
            self_output = cast(str, self.output) # type: ignore
            # Open input
            input = cliutil.CLIDataUtil.buffer_from_file(self_input)
            # Create string
            with StringIO() as text:
                # Header info
                if not self_bare:
                    text.write("# This is data from a binary file\n")
                    text.write("# This file be edited and used to encode another binary file\n")
                    text.write("# \n")
                    text.write("# Acceptable input:\n")
                    text.write("# - dec integers (ex: 2, 34, 233)\n")
                    text.write("# - hex integers (ex: 0x23, $13)\n")
                    text.write("# - bin integers (ex: 0b00111111, %01101111)\n")
                    text.write("# \n")
                    text.write("# All values must be 0-255\n")
                    text.write("\n")
                # Data
                beg = 0
                while True:
                    end = min(len(input), beg + 16)
                    # Write row data
                    for i in range(beg, end):
                        text.write(f"${input[i]:02x} ")
                    # Write row comment
                    if not self_bare:
                        gap = (' ' * 4 * (16 - (end - beg)))
                        text.write(f"{gap}   # ${beg:08x} - ${end:08x}")
                    text.write('\n')
                    # Next
                    if end == len(input): break
                    beg = end
                # To string
                string = text.getvalue()
            # Save
            cliutil.CLIStrUtil.str_to_file(string, self_output)
        except cliutil.CLICommandError as e:
            print(f"ERROR: {e}", file = sys.stderr)
            return 1
        return 0

    #endregion

sys.exit(cmd_debin().execute(sys.argv))