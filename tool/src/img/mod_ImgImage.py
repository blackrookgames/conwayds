__all__ = [\
    'ImgImage',]

import numpy as _np

from typing import\
    cast as _cast

from .mod_ImgImagePPixels import\
    ImgImagePPixels as _ImgImagePPixels
from .mod_ImgImageRGBAPixels import\
    ImgImageRGBAPixels as _ImgImageRGBAPixels
from .mod_ImgPalette import\
    ImgPalette as _ImgPalette

class ImgImage:
    """
    Represents an image
    """

    #region init

    def __init__(self, width:int = 1, height:int = 1, palsize:int = -1, alpha:bool = True):
        """
        Initializer for ImgImage

        :param width:
            Image width
        :param height:
            Image height
        :param palsize:
            Palette size (<0 means no palette)
        :param alpha:
            Alpha flag. This value has no direct effect on the type of colors allowed. 
            However, this must be True in order for images to be saved with alpha.
        :raise ValueError:
            width is less than or equal to 0\n
            or\n
            height is less than or equal to 0\n
            or\n
            palette is greater than 256
        """
        try:
            self.format(width = width, height = height, palsize = palsize, alpha = alpha)
            return
        except ValueError as _e:
            e = _e
        raise e

    #endregion

    #region operators

    def __len__(self):
        return len(self.__pixels)
    
    def __iter__(self):
        for _pixel in self.__pixels:
            yield _pixel
    
    def __getitem__(self, key):
        try:
            return self.__pixels[key]
        except TypeError as _e:
            e = _e
        except ValueError as _e:
            e = _e
        raise e
    
    def __setitem__(self, key, value):
        try:
            self.__pixels[key] = value
            return
        except TypeError as _e:
            e = _e
        except ValueError as _e:
            e = _e
        raise e
    
    #endregion

    #region properties

    @property
    def width(self):
        """
        Image width
        """
        return self.__width

    @property
    def height(self):
        """
        Image height
        """
        return self.__height
    
    @property
    def pixels(self):
        """
        Pixel data
        """
        return self.__pixels
    
    @property
    def palette(self):
        """
        Color palette
        """
        return self.__palette
    
    @property
    def haspalette(self):
        """
        Whether or not the image has a color palette
        """
        return self.__haspalette

    @property
    def alpha(self):
        """
        Alpha flag. This value has no direct effect on the type of colors allowed. 
        However, this must be True in order for images to be saved with alpha.
        """
        return self.__alpha
    @alpha.setter
    def alpha(self, value:bool):
        self.__alpha = value

    #endregion

    #region helper methods
    
    def __chkpal(self, palsize:int):
        if palsize > 256:
            raise ValueError("palsize must be less than or equal to 256.")

    def __chksize(self, width:int, height:int):
        if width <= 0:
            raise ValueError("width must be greater than zero.")
        if height <= 0:
            raise ValueError("height must be greater than zero.")

    def __setpal(self, palsize:int):
        """
        Assume:
        - palsize <= 256
        """
        if palsize < 0:
            self.__palette = None
            self.__haspalette = False
        else:
            self.__palette = _ImgPalette(size = palsize)
            self.__haspalette = True

    def __setsize(self, width:int, height:int):
        """
        Assume:
        - width > 0
        - height > 0
        """
        # width
        self.__width = width
        # height
        self.__height = height
        # pixels
        if self.__haspalette:
            self.__pixels = _ImgImagePPixels(self.__width, self.__height)
        else:
            self.__pixels = _ImgImageRGBAPixels(self.__width, self.__height)
    
    #endregion

    #region methods

    def format(self, width:int = 1, height:int = 1, palsize:int = -1, alpha:bool = True):
        """
        Formats the image\n
        NOTE: All existing data will be lost

        :param width:
            Image width
        :param height:
            Image height
        :param palsize:
            Palette size (<0 means no palette)
        :param alpha:
            Alpha flag. This value has no direct effect on the type of colors allowed. 
            However, this must be True in order for images to be saved with alpha.
        :raise ValueError:
            width is less than or equal to 0\n
            or\n
            height is less than or equal to 0\n
            or\n
            palette is greater than 256
        """
        try:
            # Validate
            self.__chkpal(palsize)
            self.__chksize(width, height)
            # Format
            self.__setpal(palsize)
            self.__setsize(width, height)
            self.__alpha = alpha
            # Success!!!
            return
        except ValueError as _e:
            e = _e
        raise e
    
    def resize(self, width:int, height:int):
        """
        Resizes the image
        
        :param width:
            Image width
        :param height:
            Image height
        :raise ValueError:
            width is less than or equal to 0\n
            or\n
            height is less than or equal to 0
        """
        try:
            prev_width = self.__width
            prev_height = self.__height
            prev_pixels = self.__pixels
            # Set new size
            self.__chksize(width, height)
            self.__setsize(width, height)
            # Set pixels
            _min_w = min(prev_width, self.__width)
            _min_h = min(prev_height, self.__height)
            for _y in range(_min_h):
                _iindex = _y * prev_width
                _oindex = _y * self.__width
                for _x in range(_min_w):
                    self.__pixels[_oindex] = prev_pixels[_iindex]
                    _iindex += 1
                    _oindex += 1
            # Success!!!
            return
        except ValueError as _e:
            e = _e
        raise e

    def getpixel(self, x:int, y:int):
        """
        Gets the color of the pixel at the specified position
        
        :param x:
            X-coordinate
        :param y:
            Y-coordinate
        :return:
            Color of pixel (or None if image is paletted and pixel value is out of range)
        :raise ValueError:
            x is out of range\n
            or\n
            y is out of range
        """
        try:
            if self.__haspalette:
                pixels = _cast(_ImgImagePPixels, self.__pixels)
                palette = _cast(_ImgPalette, self.__palette)
                index = pixels[x, y]
                if index >= len(palette):
                    return None
                return palette[index]
            else:
                pixels = _cast(_ImgImageRGBAPixels, self.__pixels)
                return pixels[x, y]
        except IndexError:
            if x < 0 or x >= self.__width:
                e = ValueError("x is out of range.")
            elif y < 0 or y >= self.__height:
                e = ValueError("y is out of range.")
            else: raise
        raise e
        
    #endregion