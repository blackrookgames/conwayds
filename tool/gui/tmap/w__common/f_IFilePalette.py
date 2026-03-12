__all__ = ['IFilePalette',]

import src.cliutil as _cliutil

from .f_IDataPalette import IDataPalette as _IDataPalette
from .f_IFile import IFile as _IFile

class IFilePalette(_IFile):
    """
    Immutable object representing palette data from a file
    """

    #region init

    def __init__(self, path:None|str):
        """
        Initializer for IFilePalette
        
        :param path:
            Path of input file
        :raise CLICommandError:
            An error occurred
        """
        super().__init__(path)
        # palette
        if path is not None:
            # Load image
            _image = _cliutil.CLIImgUtil.image_from_file(path)
            # Make sure image has palette
            if not _image.haspalette:
                raise _cliutil.CLICommandError("Image does not contain a palette.")
            # Get palette
            assert _image.palette is not None
            _src = _image.palette
        else: _src = None
        self.__palette = _IDataPalette(_src)

    #endregion

    #region properties

    @property
    def palette(self):
        """
        Palette data
        """
        return self.__palette

    #endregion