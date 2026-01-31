import numpy
import sys

from typing import cast

import src.cli as cli
import src.data as data
import src.img as img
import src.life as life

class cmd_life(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Convert a file containing life pattern data to a different format."

    #region required

    __input = cli.CLIRequiredDef(\
        name = "input",\
        desc = "Path to the input file")
    __output = cli.CLIRequiredDef(\
        name = "output",\
        desc = "Path to the output file")

    #endregion

    #region optional

    __itype = cli.CLIOptionWArgDef(\
        name = "itype",\
        short = 'i',\
        desc = f"Input type. Allowed values: txt, rle, img",\
        parse = cli.CLIParseUtil.to_enum,\
        arg = (cli.helper.LifeCLIFormat, True, ),\
        default = None)
    __otype = cli.CLIOptionWArgDef(\
        name = "otype",\
        short = 'o',\
        desc = f"Output type. Allowed values: txt, rle, img",\
        parse = cli.CLIParseUtil.to_enum,\
        arg = (cli.helper.LifeCLIFormat, True, ),\
        default = None)

    #endregion

    #region methods

    def _main(self):
        # Input
        pattern = cli.helper.LifeCLI.pattern_load(self.input, format = self.itype)
        if pattern is None: return 1
        # Output
        result = cli.helper.LifeCLI.pattern_save(pattern, self.output, format = self.otype)
        if not result: return 1
        # Success!!!
        return 0

    #endregion

sys.exit(cmd_life().execute(sys.argv))