__all__ = [\
    'ImgUtil',]

import numpy as _np

from typing import\
    cast as _cast

from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil
from .mod_ImgColor import\
    ImgColor as _ImgColor
from .mod_ImgImage import\
    ImgImage as _ImgImage
from .mod_ImgImagePPixels import\
    ImgImagePPixels as _ImgImagePPixels
from .mod_ImgImageRGBAPixels import\
    ImgImageRGBAPixels as _ImgImageRGBAPixels
from .mod_ImgPalette import\
    ImgPalette as _ImgPalette,\
    IMGPALETTE_MAX as _IMGPALETTE_MAX

class ImgUtil:
    """
    Utility for image-related operations
    """

    #region image

    @classmethod
    def image_copy(cls, srcimg:_ImgImage):
        """
        Creates a copy of an ImgImage
        
        :param srcimg:
            Source ImgImage
        :return:
            Created ImgImage
        """
        if srcimg.haspalette:
            _srcpal = _cast(_ImgPalette, srcimg.palette)
            _srcpix = _cast(_ImgImagePPixels, srcimg.pixels)
            newimg = _ImgImage(\
                width = srcimg.width,\
                height = srcimg.height,\
                palsize = len(_srcpal),\
                alpha = srcimg.alpha)
            _newpal = _cast(_ImgPalette, newimg.palette)
            _newpix = _cast(_ImgImagePPixels, newimg.pixels)
            for _i in range(len(_srcpal)):
                _newpal[_i] = _srcpal[_i]
            for _i in range(len(srcimg)):
                _newpix[_i] = _srcpix[_i]
        else:
            _srcpix = _cast(_ImgImageRGBAPixels, srcimg.pixels)
            newimg = _ImgImage(\
                width = srcimg.width,\
                height = srcimg.height,\
                alpha = srcimg.alpha)
            _newpix = _cast(_ImgImageRGBAPixels, newimg.pixels)
            for _i in range(len(srcimg)):
                _newpix[_i] = _srcpix[_i]
        return newimg

    @classmethod
    def image_pal(cls, srcimg:_ImgImage):
        """
        Creates a paletted version of an ImgImage\n
        if the image is already paletted, then a copy of the ImgImage is created.\n
        NOTE: Some color data will be lost on ImgImages with more than 256 unique colors. 
        
        :param srcimg:
            Source ImgImage
        :return:
            Created ImgImage
        """
        if srcimg.haspalette:
            return cls.image_copy(srcimg)
        # Extract colors
        srcpix = _cast(_ImgImageRGBAPixels, srcimg.pixels)
        colors:dict[_ImgColor, _np.uint8] = {}
        for _color in srcpix:
            if _color in colors:
                continue
            _index = _np.uint8(len(colors))
            colors[_color] = _index
            if len(colors) == _IMGPALETTE_MAX:
                break
        # Create image
        newimg = _ImgImage(\
            width = srcimg.width,\
            height = srcimg.height,\
            palsize = len(colors),\
            alpha = srcimg.alpha)
        # Populate palette
        newpal = _cast(_ImgPalette, newimg.palette)
        for _color, _index in colors.items():
            newpal[_index] = _color
        # Set pixels
        newpix = _cast(_ImgImagePPixels, newimg.pixels)
        for _i in range(len(srcpix)):
            _color = srcpix[_i]
            if _color in colors:
                newpix[_i] = colors[_color]
            else:
                newpix[_i] = 0xFF
        # Success!!!
        return newimg

    @classmethod
    def image_nopal(cls, srcimg:_ImgImage):
        """
        Creates a non-paletted version of an ImgImage\n
        if the image is already non-paletted, then a copy of the ImgImage is created.
        
        :param srcimg:
            Source ImgImage
        :return:
            Created ImgImage
        """
        if not srcimg.haspalette:
            return cls.image_copy(srcimg)
        newimg = _ImgImage(\
            width = srcimg.width,\
            height = srcimg.height,\
            alpha = srcimg.alpha)
        srcpal = _cast(_ImgPalette, srcimg.palette)
        srcpix = _cast(_ImgImagePPixels, srcimg.pixels)
        newpix = _cast(_ImgImageRGBAPixels, newimg.pixels)
        for _i in range(len(srcpix)):
            _index = srcpix[_i]
            if _index < len(srcpal):
                newpix[_i] = srcpal[_index]
            else:
                newpix[_i] = _ImgColor(a = 0)
        return newimg

    #endregion
