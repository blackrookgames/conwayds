import numpy
import sys

from enum import auto, Enum
from pathlib import Path
from typing import cast

import src.cli as cli
import src.cliutil as cliutil
import src.img as img

class cmd_imgnpal(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Converts an image to a non-paletted image."

    #region required

    __input = cli.CLIRequiredDef(\
        name = "input",\
        desc = "Path to the input file")

    #endregion

    #region optional

    __output = cli.CLIOptionWArgDef(\
        name = "output",\
        short = 'o',\
        desc = "Prefix for output paths",\
        default = None)

    __cols = cli.CLIOptionWArgDef(\
        name = "cols",\
        short = 'c',\
        desc = "Number of columns",\
        parse = cli.CLIParseUtil.to_int,
        default = -1)

    __rows = cli.CLIOptionWArgDef(\
        name = "rows",\
        short = 'r',\
        desc = "Number of rows",\
        parse = cli.CLIParseUtil.to_int,
        default = -1)

    __width = cli.CLIOptionWArgDef(\
        name = "width",\
        short = 'w',\
        desc = "Width of each output image",\
        parse = cli.CLIParseUtil.to_int,
        default = -1)

    __height = cli.CLIOptionWArgDef(\
        name = "height",\
        short = 'h',\
        desc = "Height of each output image",\
        parse = cli.CLIParseUtil.to_int,
        default = -1)
    
    __count = cli.CLIOptionWArgDef(\
        name = "count",\
        short = 'n',\
        desc = "Total number of output images",\
        parse = cli.CLIParseUtil.to_int,
        default = -1)

    #endregion

    #region helper methods

    @classmethod
    def __extension(cls, path:Path):
        parent = path.parent
        name = path.name
        # Find extension
        extpos = 0
        for _i in range(len(name)):
            if name[_i] != '.': continue
            extpos = _i
        # Return
        return parent.joinpath(name[:extpos]), name[extpos:]
    
    @classmethod
    def __raise_width0(cls):
        raise cliutil.CLICommandError("Output width cannot be zero.")
    
    @classmethod
    def __raise_height0(cls):
        raise cliutil.CLICommandError("Output height cannot be zero.")
    
    @classmethod
    def __raise_width2lg(cls):
        raise cliutil.CLICommandError("Output width cannot be larger than input width.")
    
    @classmethod
    def __raise_height2lg(cls):
        raise cliutil.CLICommandError("Output height cannot be larger than input height.")

    #endregion

    #region methods

    def _main(self):
        try:
            self_input = cast(str, self.input) # type: ignore
            self_output = cast(None|str, self.output) # type: ignore
            self_cols = cast(int, self.cols) # type: ignore
            self_rows = cast(int, self.rows) # type: ignore
            self_width = cast(int, self.width) # type: ignore
            self_height = cast(int, self.height) # type: ignore
            self_count = cast(int, self.count) # type: ignore
            # Extract input path
            input_pre, input_ext = self.__extension(Path(self_input))
            # Determine output prefix
            output_pre = input_pre if (self_output is None) else Path(self_output)
            # Open input image
            input_img = cliutil.CLIImgUtil.image_from_file(self_input)
            input_pal = len(input_img.palette) if input_img.haspalette else -1 # type: ignore
            # Compute dimensions
            defined = \
                (0b0001 if (self_cols > 0) else 0) |\
                (0b0010 if (self_width > 0) else 0)|\
                (0b0100 if (self_rows > 0) else 0)|\
                (0b1000 if (self_height > 0) else 0)
            if defined != 0:
                _rows = 1
                # Horizontal
                _defined = defined & 0b0011
                if _defined == 0b0000:
                    final_width = input_img.width
                    _cols = 1
                elif _defined == 0b0001:
                    if self_cols > input_img.width: self.__raise_width0()
                    final_width = input_img.width // self_cols
                    _cols = self_cols
                else:
                    if self_width > input_img.width: self.__raise_width2lg()
                    if _defined == 0b0010:
                        final_width = self_width
                        _cols = input_img.width // self_width
                    else:
                        if (self_width * self_cols) > input_img.width:
                            raise cliutil.CLICommandError("Horizontal out of range")
                        final_width = self_width
                        _cols = self_cols
                # Vertical
                _defined = defined & 0b1100
                if _defined == 0b0000:
                    final_height = input_img.height
                    _rows = 1
                elif _defined == 0b0100:
                    if self_rows > input_img.height: self.__raise_height0()
                    final_height = input_img.height // self_rows
                    _rows = self_rows
                else:
                    if self_height > input_img.height: self.__raise_height2lg()
                    if _defined == 0b1000:
                        final_height = self_height
                        _rows = input_img.height // self_height
                    else:
                        if (self_height * self_rows) > input_img.height:
                            raise cliutil.CLICommandError("Vertical out of range")
                        final_height = self_height
                        _rows = self_rows
                # Compute count
                final_cols = _cols
                final_count = _cols * _rows
                if self_count > 0 and self_count < final_count:
                    final_count = self_count
            elif self_count > 0:
                # Split by count
                if self_count > input_img.width: self.__raise_width0()
                final_cols = self_count
                final_width = input_img.width // self_count
                final_height = input_img.height
                final_count = self_count
            else:
                # Don't split
                final_cols = 1
                final_width = input_img.width
                final_height = input_img.height
                final_count = 1
            # Create output images
            output_imgs:list[img.ImgImage] = []
            for _i in range(final_count):
                # Initialize image
                _output = img.ImgImage(\
                    width = final_width,\
                    height = final_height,\
                    palsize = input_pal,\
                    alpha = input_img.alpha)
                # Set palette
                if _output.haspalette:
                    assert _output.palette is not None
                    for _j in range(len(_output.palette)):
                        _output.palette[_j] = input_img.palette[_j] # type: ignore
                # Set pixels
                _off_x = (_i % final_cols) * final_width
                _off_y = (_i // final_cols) * final_height
                for _y in range(final_height):
                    for _x in range(final_width):
                        _output[_x, _y] = input_img[_off_x + _x, _off_y + _y]
                # Add image
                output_imgs.append(_output)
            # Save output images
            for _i in range(len(output_imgs)):
                _path = f"{output_pre}.{_i:04}{input_ext}"
                cliutil.CLIImgUtil.image_to_file(output_imgs[_i], _path)
        except cliutil.CLICommandError as e:
            print(f"ERROR: {e}", file = sys.stderr)
            return 1
        return 0

    #endregion

sys.exit(cmd_imgnpal().execute(sys.argv))