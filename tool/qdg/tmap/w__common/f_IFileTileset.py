__all__ = ['IFileTileset',]

import src.cliutil as _cliutil
import src.img as _img

from .f_IDataPalette import IDataPalette as _IDataPalette
from .f_IDataTileset import IDataTileset as _IDataTileset
from .f_IFile import IFile as _IFile

class IFileTileset(_IFile):
    """
    Immutable object representing tileset data from a file
    """

    #region init

    def __init__(self, path:None|str):
        """
        Initializer for IFileTileset
        
        :param path:
            Path of input file
        :raise CLICommandError:
            An error occurred
        """
        super().__init__(path)
        # tileset/palette
        if path is not None:
            # Load image
            _image = _cliutil.CLIImgUtil.image_from_file(path)
            # Make sure image has palette
            if not _image.haspalette:
                raise _cliutil.CLICommandError("Image does not contain a palette.")
            # Get tileset/palette
            assert isinstance(_image.pixels, _img.ImgImagePPixels)
            assert _image.palette is not None
            _src_pixels = _image.pixels
            _src_palette = _image.palette
        else:
            _src_pixels = None
            _src_palette = None
        self.__tileset = _IDataTileset(_src_pixels)
        self.__palette = _IDataPalette(_src_palette)

    #endregion

    #region properties

    @property
    def tileset(self):
        """
        Tileset data
        """
        return self.__tileset

    @property
    def palette(self):
        """
        Palette data
        """
        return self.__palette

    #endregion