__all__ = [\
    'DSCLI',\
    'DSCLIFormat',]

from enum import\
    auto as _auto,\
    Enum as _Enum
from io import\
    StringIO as _StringIO
from sys import\
    stderr as _stderr
from typing import\
    cast as _cast

from ...ds.mod_DSPalette import\
    DSPalette as _DSPalette
from ...ds.mod_DSSerial import\
    DSSerial as _DSSerial
from .mod_ImgCLI import\
    ImgCLI as _ImgCLI

class DSCLIFormat(_Enum):
    """
    Represents a format for storing pattern data
    """

    BIN = _auto()
    """
    Palette data is stored as binary data
    """

    CPP = _auto()
    """
    Palette data is stored as C++ source code\n
    NOTE: This is only valid for output
    """

    IMG = _auto()
    """
    Palette data is stored as an image
    """

class DSCLI:
    """
    Utility for Life-related operations
    """

    #region palette img

    @classmethod
    def palette_load_img(cls, path:str):
        """
        Attempts to load a DSPalette from a file
        
        :param path:
            Path of input file
        :return:
            Loaded DSPalette (or None if an error occurred)
        """
        # Load image
        img = _ImgCLI.load(path)
        if img is None: return None
        # Read image
        return _DSSerial.palette_from_img(img)

    @classmethod
    def palette_save_img(cls, palette:_DSPalette, path:str):
        """
        Attempts to save a DSPalette to a file
        
        :param palette:
            DSPalette to save
        :param path:
            Path of output file
        :return:
            Whether or not successful
        """
        img = _DSSerial.palette_to_img(palette)
        return _ImgCLI.save(img, path)

    #endregion