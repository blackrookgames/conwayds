__all__ = [\
    'FilePalette',]

import src.cliutil as _cliutil

from .f_DataPalette import\
    DataPalette as _DataPalette

class FilePalette:
    """
    Represents a palette data from a file
    """

    #region init

    def __init__(self, path:None|str):
        """
        Initializer for FilePalette
        
        :param path:
            Path of input file
        :raise CLICommandError:
            An error occurred
        """
        # path
        self.__path = path
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
        self.__palette = _DataPalette(_src)

    #endregion

    #region properties

    @property
    def path(self):
        """
        File path
        """
        return self.__path

    @property
    def palette(self):
        """
        Palette data
        """
        return self.__palette

    #endregion