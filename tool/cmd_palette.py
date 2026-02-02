import numpy
import sys

from enum import auto, Enum
from typing import cast

import src.cli as cli
import src.ds as ds
import src.img as img

from abs_cpp import abs_cpp

class Format(Enum):
    BIN = auto()
    CPP = auto()
    IMG = auto()

class cmd_palette(abs_cpp):

    @property
    def _desc(self) -> None|str:
        return "Creates a palette from an image."

    #region required

    __input = abs_cpp._input()
    __output = abs_cpp._output()

    #endregion

    #region optional

    __itype = abs_cpp._itype(Format)
    __otype = abs_cpp._otype(Format)

    __noalpha = cli.CLIOptionFlagDef(\
        name = "noalpha",\
        short = 'A',\
        desc = "Whether or not to forget alpha information")

    #endregion

    #region helper methods

    @classmethod
    def formatof(cls, path:str):
        """
        Determines the likely format of a file at the specified path
        
        :param path: Path of file
        :return: Determined format
        """
        if path.endswith(".cpp"):
            return Format.CPP
        if cli.helper.ImgCLI.checkext(path):
            return Format.IMG
        return Format.BIN

    def load(self):
        self_input = cast(str, self.input) # type: ignore
        self_itype = cast(None|Format, self.itype) # type: ignore
        # Get format
        if self_itype is None:
            if abs_cpp._cppinput(self_input):
                return None
            self_itype = self.formatof(self_input)
        # Load
        match self_itype:
            case Format.BIN:
                return cli.helper.DSCLI.palette_load_bin(self_input)
            case Format.IMG:
                return cli.helper.DSCLI.palette_load_img(self_input)
            case _: return None # Should never happen
    
    def save(self, palette:ds.DSPalette):
        self_output = cast(str, self.output) # type: ignore
        self_otype = cast(None|Format, self.otype) # type: ignore
        self_noalpha = cast(bool, self.noalpha) # type: ignore
        # Get format
        if self_otype is None:
            self_otype = self.formatof(self_output)
        # Load
        match self_otype:
            case Format.BIN:
                return cli.helper.DSCLI.palette_save_bin(\
                    palette,\
                    self_output,\
                    noalpha = self_noalpha)
            case Format.CPP:
                return cli.helper.DSCLI.palette_save_cpp(\
                    palette,\
                    self_output,\
                    noalpha = self_noalpha)
            case Format.IMG:
                return cli.helper.DSCLI.palette_save_img(\
                    palette,\
                    self_output,\
                    noalpha = self_noalpha)
            case _: return None # Should never happen

    #endregion

    #region methods

    def _main(self):
        # Input
        palette = self.load()
        if palette is None: return 1
        # Output
        result = self.save(palette)
        if not result: return 1
        # Success!!!
        return 0

    #endregion

sys.exit(cmd_palette().execute(sys.argv))