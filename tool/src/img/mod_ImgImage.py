__all__ = [\
    'ImgImage',]

import numpy as _np

from typing import\
    cast as _cast

from .mod_ImgColor import\
    ImgColor as _ImgColor
from .mod_ImgPalette import\
    ImgPalette as _ImgPalette

class ImgImage:
    """
    Represents an image
    """

    #region init

    def __init__(self,\
            width:int = 1,\
            height:int = 1,\
            palettesize:None|int = None):
        """
        Initializer for ImgImage
        
        :param width:
            Image width
        :param height:
            Image height
        :param palettesize:
            Number of colors in palette (use None for no palette)
        :raise ValueError:
            width is less than or equal to zero\n
            or\n
            height is less than or equal to zero
            or\n
            palettesize is less than zero
        """
        try:
            self.format(\
                width = width,\
                height = height,\
                palettesize = palettesize)
            return
        except ValueError as _e:
            e = _e
        raise e

    #endregion

    #region operators

    def __len__(self):
        return len(self.__pixels)
    
    def __getitem__(self, key):
        try:
            index = self.__index(key)
            return _cast(_ImgColor|int, self.__pixels[index])
        except ValueError as _e:
            e = _e
        except TypeError as _e:
            e = _e
        raise e
    
    def __setitem__(self, key, value):
        try:
            index = self.__index(key)
            # Check type
            if self.__haspalette:
                if not isinstance(value, int):
                    raise TypeError("For an image with a palette, the value type must be int.")
            else:
                if not isinstance(value, _ImgColor):
                    raise TypeError("For an image without a palette, the value type must be ImgColor.")
            # Set
            self.__pixels[index] = value
            # Success!!!
            return
        except ValueError as _e:
            e = _e
        except TypeError as _e:
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
    def haspalette(self):
        """
        Whether or not the image has a palette
        """
        return self.__haspalette
    
    @property
    def palette(self):
        """
        Palette
        """
        return self.__palette

    #endregion

    #region helper methods

    def __xy(self,\
            x:int,\
            y:int):
        if x < 0 or x >= self.__width:
            raise ValueError("x is out of range.")
        if y < 0 or y >= self.__height:
            raise ValueError("y is out of range.")
        return x + y * self.__width

    def __index(self, key):
        BADTUPLE = "Tuple must contain exactly 2 integers."
        # Is this a tuple?
        if isinstance(key, tuple):
            if not len(key) == 2:
                raise ValueError(BADTUPLE)
            x, y = key
            if not (isinstance(x, int) and isinstance(y, int)):
                raise ValueError(BADTUPLE)
            return self.__xy(x, y)
        # Is this an integer?
        if isinstance(key, int):
            if key < 0 or key >= len(self.__pixels):
                raise ValueError("Index is out of range.")
            return key
        # Raise exception
        raise TypeError(f"{type(key).__name__} is not a supported key type.")

    def __setsize(self,\
            width:int,\
            height:int):
        if width <= 0:
            raise ValueError("width must be greater than zero.")
        if height <= 0:
            raise ValueError("height must be greater than zero.")
        # width
        self.__width = width
        # height
        self.__height = height
        # pixels
        if self.__haspalette:
            _value = 0
        else:
            _value = _ImgColor()
        self.__pixels = _np.full(self.__width * self.__height, _value, dtype = object)

    #endregion

    #region methods

    def format(self,\
            width:int = 1,\
            height:int = 1,\
            palettesize:None|int = None):
        """
        Formats the ImgImage\n
        WARNING: This erases all data in the image
        
        :param width:
            Image width
        :param height:
            Image height
        :param palettesize:
            Number of colors in palette (use None for no palette)
        :raise ValueError:
            width is less than or equal to zero\n
            or\n
            height is less than or equal to zero
            or\n
            palettesize is less than zero
        """
        try:
            # palette
            if palettesize is not None:
                self.__haspalette = True
                self.__palette = _ImgPalette(palettesize)
            else:
                self.__haspalette = False
                self.__palette = None
            # pixels
            self.__setsize(width, height)
            # Success!!!
            return
        except ValueError as _e:
            e = _e
        raise e

    def resize(self,\
            width:int,\
            height:int,\
            preserve:bool = False):
        """
        Resizes the image
        
        :param width:
            Image width
        :param height:
            Image height
        :param preserve:
            Whether or not to preserve existing pixel data
        :raise ValueError:
            width is less than or equal to zero\n
            or\n
            height is less than or equal to zero
        """
        prev_width = self.__width
        prev_height = self.__height
        prev_pixels = self.__pixels
        # Set size
        ex = None
        try: self.__setsize(width, height)
        except ValueError as _ex: ex = _ex
        if ex is not None: raise ex
        # Preserve (if requested)
        if preserve:
            min_width = min(prev_width, self.__width)
            min_height = min(prev_height, self.__height)
            curr = 0
            prev = 0
            for y in range(min_height):
                for x in range(min_width):
                    self.__pixels[curr + x] = prev_pixels[prev + x]
                curr += self.__width
                prev += prev_width

    def getpixel(self,\
            x:int,\
            y:int):
        """
        Gets the color of the pixel at the specified position
        
        :param x:
            X-coordinate
        :param y:
            Y-coordinate
        :return:
            The color of the pixel (or None if image has a palette and the pixel refers to an out-of-range index)
        :raise ValueError:
            x is out of range\n
            or\n
            y is out of range
        """
        try:
            pixel = self.__pixels[self.__xy(x, y)]
            if self.__palette is not None:
                pixel = _cast(int, pixel)
                if pixel > len(self.__palette):
                    return None
                return self.__palette[pixel]
            return _cast(_ImgColor, pixel)
        except ValueError as _e:
            e = _e
        raise e

    #endregion