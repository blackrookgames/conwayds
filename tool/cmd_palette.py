import numpy
import sys

from enum import auto, Enum
from typing import cast

import src.cli as cli
import src.cliutil as cliutil
import src.data as data
import src.ds as ds
import src.img as img

class Format(Enum):
    BIN = auto()
    IMG = auto()
    CPP = auto()

class cmd_palette(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Converts a palette."

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
        desc = f"Input type. Allowed values: bin, img",\
        parse = cli.CLIParseUtil.to_enum,\
        arg = (Format, True, ),\
        default = None)
    __otype = cli.CLIOptionWArgDef(\
        name = "otype",\
        short = 'o',\
        desc = f"Output type. Allowed values: bin, img, cpp",\
        parse = cli.CLIParseUtil.to_enum,\
        arg = (Format, True, ),\
        default = None)
    __noalpha = cli.CLIOptionFlagDef(\
        name = "noalpha",\
        short = 'A',\
        desc = "Whether or not to forget alpha information")
    __header = cli.CLIOptionWArgDef(\
        name = "header",\
        short = 'h',\
        desc = f"Path to output header file; required if output is C++",\
        default = None)
    __classname = cli.CLIOptionWArgDef(\
        name = "classname",\
        short = 'c',\
        desc = f"Name of C++ class; required if output is C++",\
        default = None)
    __defname = cli.CLIOptionWArgDef(\
        name = "defname",\
        short = 'D',\
        desc = f"DEF name; useless output is not C++",\
        default = None)

    #endregion

    #region helper methods

    @classmethod
    def __getformat(cls, format:None|Format, path):
        if format is not None:
            return format
        if cliutil.CLIImgUtil.checkext(path):
            return Format.IMG
        if path.endswith(".cpp"):
            return Format.CPP
        return Format.BIN
    
    def __validate_cpp(self):
        self_header = cast(None|str, self.header) # type: ignore
        self_classname = cast(None|str, self.classname) # type: ignore
        if self_header is None:
            raise cliutil.CLICommandError("C++ --header must be defined.")
        if self_classname is None:
            raise cliutil.CLICommandError("C++ --classname must be defined.")
        
    #endregion

    #region methods

    def _main(self):
        try:
            self_input = cast(str, self.input) # type: ignore
            self_output = cast(str, self.output) # type: ignore
            self_itype = cast(None|Format, self.itype) # type: ignore
            self_otype = cast(None|Format, self.otype) # type: ignore
            self_noalpha = cast(bool, self.noalpha) # type: ignore
            self_header = cast(None|str, self.header) # type: ignore
            self_classname = cast(None|str, self.classname) # type: ignore
            self_defname = cast(None|str, self.defname) # type: ignore
            # Input
            itype = self.__getformat(self_itype, self_input)
            if itype == Format.CPP:
                raise cliutil.CLICommandError("C++ source code is not supported input.")
            match itype:
                case Format.BIN:
                    _input = cliutil.CLIDataUtil.buffer_from_file(self_input)
                    palette = ds.DSSerial.palette_from_bin(_input)
                case Format.IMG:
                    _input = cliutil.CLIImgUtil.from_file(self_input)
                    palette = ds.DSSerial.palette_from_img(_input)
                case _: return 1 # Should never happen
            
            # Output
            otype = self.__getformat(self_otype, self_output)
            # BIN, CPP
            if otype == Format.BIN or otype == Format.CPP:
                _output = ds.DSSerial.palette_to_bin(palette,\
                    noalpha = self_noalpha)
                if otype == Format.CPP:
                    self.__validate_cpp()
                    cliutil.CLIDataUtil.buffer_to_cpp(_output,\
                        cast(str, self_header),\
                        self_output,\
                        cast(str, self_classname),\
                        defname = self_defname)
                else:
                    cliutil.CLIDataUtil.buffer_to_file(_output, self_output)
            # IMG
            elif otype == Format.IMG:
                _output = ds.DSSerial.palette_to_img(palette,\
                    noalpha = self_noalpha)
                cliutil.CLIImgUtil.to_file(_output, self_output)
            # Nothing (Should never happen)
            else: return 1

        except cliutil.CLICommandError as e:
            print(f"ERROR: {e}", file = sys.stderr)
            return 1
        except data.SerialError as e:
            print(f"ERROR: {e}", file = sys.stderr)
            return 1
        return 0

    #endregion

sys.exit(cmd_palette().execute(sys.argv))