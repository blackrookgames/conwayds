import numpy
import sys

from enum import auto, Enum
from typing import cast

import src.cli as cli
import src.cliutil as cliutil
import src.data as data
import src.img as img
import src.life as life

class Format(Enum):
    RLE = auto()
    TXT = auto()
    IMG = auto()

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
        arg = (Format, True, ),\
        default = None)
    __otype = cli.CLIOptionWArgDef(\
        name = "otype",\
        short = 'o',\
        desc = f"Output type. Allowed values: txt, rle, img",\
        parse = cli.CLIParseUtil.to_enum,\
        arg = (Format, True, ),\
        default = None)

    #endregion

    #region helper methods

    @classmethod
    def __getformat(cls, format:None|Format, path):
        if format is not None:
            return format
        if cliutil.CLIImgUtil.checkext(path):
            return Format.IMG
        if path.endswith(".rle"):
            return Format.RLE
        return Format.TXT
        
    #endregion

    #region methods

    def _main(self):
        try:
            self_input = cast(str, self.input) # type: ignore
            self_output = cast(str, self.output) # type: ignore
            self_itype = cast(None|Format, self.itype) # type: ignore
            self_otype = cast(None|Format, self.otype) # type: ignore
            # Input
            match self.__getformat(self_itype, self_input):
                case Format.RLE:
                    _input = cliutil.CLIStrUtil.str_from_file(self_input)
                    pattern = life.LifeSerial.pattern_from_rle(_input)
                case Format.TXT:
                    _input = cliutil.CLIStrUtil.str_from_file(self_input)
                    pattern = life.LifeSerial.pattern_from_txt(_input)
                case Format.IMG:
                    _input = cliutil.CLIImgUtil.from_file(self_input)
                    pattern = life.LifeSerial.pattern_from_img(_input)
                case _: return 1 # Should never happen
            # Output
            match self.__getformat(self_otype, self_output):
                case Format.RLE:
                    _output = life.LifeSerial.pattern_to_rle(pattern)
                    cliutil.CLIStrUtil.str_to_file(_output, self_output)
                case Format.TXT:
                    _output = life.LifeSerial.pattern_to_txt(pattern)
                    cliutil.CLIStrUtil.str_to_file(_output, self_output)
                case Format.IMG:
                    _output = life.LifeSerial.pattern_to_img(pattern)
                    cliutil.CLIImgUtil.to_file(_output, self_output)
                case _: return 1 # Should never happen
        except cliutil.CLICommandError as e:
            print(f"ERROR: {e}", file = sys.stderr)
            return 1
        except data.SerialError as e:
            print(f"ERROR: {e}", file = sys.stderr)
            return 1
        return 0

    #endregion

sys.exit(cmd_life().execute(sys.argv))