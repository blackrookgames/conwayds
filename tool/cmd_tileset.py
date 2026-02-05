import numpy
import sys

from enum import auto, Enum
from typing import cast

import src.cli as cli
import src.cliutil as cliutil
import src.data as data
import src.ds as ds
import src.img as img

#region helper methods

def tobpp(input:str):
    passs, value = cli.CLIParseUtil.to_int(input)
    if not passs: return False, 0
    if value != 4 and value != 8:
        print(f"{value} is not valid for the bits-per-pixel.", file = sys.stderr)
        return False, 0
    return True, value

#endregion

class Format(Enum):
    BIN = auto()
    IMG = auto()
    CPP = auto()

class cmd_tileset(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Converts a tileset."

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
    __bpp = cli.CLIOptionWArgDef(\
        name = "bpp",\
        short = 'b',\
        desc = f"Bits per pixel. Allowed values: 4, 8",\
        parse = tobpp,\
        default = 8)
    __palette = cli.CLIOptionWArgDef(\
        name = "palette",\
        short = 'p',\
        desc = f"Path to palette file (must be bin); useless if output is not IMG",\
        default = None)
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
        desc = f"DEF name; useless output if not C++",\
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
    
    def __from_bin(self):
        # _input = cliutil.CLIDataUtil.buffer_from_file(self_input)
        # palette = ds.DSSerial.palette_from_bin(_input)
        pass

    def __to_bin(self, tileset:ds.DSTileset):
        # _output = ds.DSSerial.palette_to_bin(palette,\
        #     noalpha = self_noalpha)
        # if otype == Format.CPP:
        #     self.__validate_cpp()
        #     cliutil.CLIDataUtil.buffer_to_cpp(_output,\
        #         cast(str, self_header),\
        #         self_output,\
        #         cast(str, self_classname),\
        #         defname = self_defname)
        # else:
        #     cliutil.CLIDataUtil.buffer_to_file(_output, self_output)
        pass

    def __from_img(self):
        self_input = cast(str, self.input) # type: ignore
        self_bpp = cast(int, self.bpp) # type: ignore
        # Open image
        _input = cliutil.CLIImgUtil.image_from_file(self_input)
        if not _input.haspalette:
            raise cliutil.CLICommandError("Input image must be paletted.")
        # Create tileset
        if self_bpp == 4:
            tileset = ds.DSUtil.tileset4_get_img(_input)
        else:
            tileset = ds.DSUtil.tileset8_get_img(_input)
        # Success!!!
        return tileset
    
    def __to_img(self, tileset:ds.DSTileset):
        self_output = cast(str, self.output) # type: ignore
        self_bpp = cast(int, self.bpp) # type: ignore
        self_palette = cast(None|str, self.palette) # type: ignore
        # Create image
        _image = img.ImgImage(palsize = 0, alpha = False)
        # Set palette
        if self_palette is not None:
            _buffer = cliutil.CLIDataUtil.buffer_from_file(self_palette)
            _palette = ds.DSSerial.palette_from_bin(_buffer)
            ds.DSUtil.palette_set_pal(cast(img.ImgPalette, _image.palette), _palette)
        # Set pixels
        if self_bpp == 4:
            ds.DSUtil.tileset4_set_img(_image, cast(ds.DSTileset4, tileset))
        else:
            ds.DSUtil.tileset8_set_img(_image, cast(ds.DSTileset8, tileset))
        # Save image
        cliutil.CLIImgUtil.image_to_file(_image, self_output)
        
    #endregion

    #region methods

    def _main(self):
        try:
            self_input = cast(str, self.input) # type: ignore
            self_output = cast(str, self.output) # type: ignore
            self_itype = cast(None|Format, self.itype) # type: ignore
            self_otype = cast(None|Format, self.otype) # type: ignore
            self_bpp = cast(int, self.bpp) # type: ignore
            self_header = cast(None|str, self.header) # type: ignore
            self_classname = cast(None|str, self.classname) # type: ignore
            self_defname = cast(None|str, self.defname) # type: ignore
            # Input
            itype = self.__getformat(self_itype, self_input)
            if itype == Format.CPP:
                raise cliutil.CLICommandError("C++ source code is not supported input.")
            match itype:
                case Format.BIN:
                    tileset = self.__from_bin()
                    return 1
                case Format.IMG:
                    tileset = self.__from_img()
                case _: return 1 # Should never happen
            # Output
            otype = self.__getformat(self_otype, self_output)
            # BIN, CPP
            if otype == Format.BIN or otype == Format.CPP:
                self.__to_bin(tileset)
                return 1
            # IMG
            elif otype == Format.IMG:
                self.__to_img(tileset)
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

sys.exit(cmd_tileset().execute(sys.argv))