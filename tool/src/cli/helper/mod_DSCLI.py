__all__ = [\
    'DSCLI',]

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
from ..mod_CLIParseUtil import\
    CLIParseUtil as _CLIParseUtil
from .mod_DataCLI import\
    DataCLI as _DataCLI
from .mod_ImgCLI import\
    ImgCLI as _ImgCLI

class DSCLI:
    """
    Utility for Life-related operations
    """

    #region palette bin

    @classmethod
    def palette_load_bin(cls, path:str):
        """
        Attempts to load a DSPalette from a binary file
        
        :param path:
            Path of input file
        :return:
            Loaded DSPalette (or None if an error occurred)
        """
        # Load data buffer
        bin = _DataCLI.buffer_load(path)
        if bin is None: return None
        # Read image
        return _DSSerial.palette_from_bin(bin)

    @classmethod
    def palette_save_bin(cls, palette:_DSPalette, path:str,\
            noalpha:bool = False):
        """
        Attempts to save a DSPalette to a binary file
        
        :param palette:
            DSPalette to save
        :param path:
            Path of output file
        :param noalpha:
            Whether or not to ignore alpha
        :return:
            Whether or not successful
        """
        bin = _DSSerial.palette_to_bin(palette,\
            noalpha = noalpha)
        return _DataCLI.buffer_save(bin, path)

    #endregion

    #region palette cpp

    @classmethod
    def palette_save_cpp(cls, palette:_DSPalette, path_cpp:str,\
            path_hdr:None|str = None,\
            noalpha:bool = False):
        """
        Attempts to save a DSPalette to a C++ source file
        
        :param palette:
            DSPalette to save
        :param path_cpp:
            Path of C++ file
        :param path_hdr:
            Path of C++ header file
        :param noalpha:
            Whether or not to ignore alpha
        :return:
            Whether or not successful
        """
        bin = _DSSerial.palette_to_bin(palette,\
            noalpha = noalpha)
        return _DataCLI.buffer_cpp(bin, path_cpp, path_hdr = path_hdr)

    #endregion

    #region palette img

    @classmethod
    def palette_load_img(cls, path:str):
        """
        Attempts to load a DSPalette from an image file
        
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
    def palette_save_img(cls, palette:_DSPalette, path:str,\
            noalpha:bool = False,\
            cpr:int = 16):
        """
        Attempts to save a DSPalette to an image file
        
        :param palette:
            DSPalette to save
        :param path:
            Path of output file
        :param noalpha:
            Whether or not to ignore alpha
        :param cpr:
            Colors per row (<= 0 means all colors are on a single row)
        :return:
            Whether or not successful
        """
        img = _DSSerial.palette_to_img(palette,\
            noalpha = noalpha,\
            cpr = cpr)
        return _ImgCLI.save(img, path)

    #endregion