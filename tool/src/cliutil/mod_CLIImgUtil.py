__all__ = [\
    'CLIImgUtil',]

import numpy as _np

from PIL import\
    Image as _Image
from typing import\
    cast as _cast

from ..img.mod_Img import\
    Img as _Img
from ..img.mod_ImgColor import\
    ImgColor as _ImgColor
from ..img.mod_ImgImage import\
    ImgImage as _ImgImage
from ..img.mod_ImgPalette import\
    ImgPalette as _ImgPalette
from .mod_CLICommandError import\
    CLICommandError as _CLICommandError

class CLIImgUtil:
    """
    CLI-utility for image operations
    """

    #region helper methods

    @classmethod
    def __tuple2pixel(cls, color:tuple[int, ...]):
        r = (0 if len(color) == 0 else color[0])
        g = (0 if len(color) <= 1 else color[1])
        b = (0 if len(color) <= 2 else color[2])
        a = (255 if len(color) <= 3 else color[3])
        return _ImgColor(r = r, g = g, b = b, a = a)
    
    @classmethod
    def __pixel2tuple(cls, color:_ImgColor, noalpha:bool = False):
        if noalpha:
            return (color.r, color.g, color.b)
        return (color.r, color.g, color.b, color.a)

    @classmethod
    def __palettecolor(cls, palette:list[int], start:int):
        return _ImgColor(\
            r = palette[start],\
            g = palette[start + 1],\
            b = palette[start + 2])

    #endregion

    #region checkext

    @classmethod
    def checkext(cls, path:str):
        """
        Check if the path has a valid image file extension

        param path:
            Path
        return:
            Whether or not the path has a valid image file extension
        """
        return path.endswith((".png", ".bmp", ".jpg", ".tga", ".gif"))

    #endregion

    #region img

    @classmethod
    def from_file(cls, path:str):
        """
        Creates an Img by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created Img
        :raise CLICommandError:
            An error occurred
        """
        try: 
            with _Image.open(path) as input:
                raw_w, raw_h = input.size
                img = _Img(max(1, raw_w), max(1, raw_h))
                if input.mode == 'P':
                    # Get palette
                    palette = input.getpalette()
                    if palette is not None and len(palette) == 0: palette = None
                    # Loop thru pixels
                    for y in range(raw_h):
                        for x in range(raw_w):
                            raw_pixel = input.getpixel((x, y))
                            if isinstance(raw_pixel, int):
                                if palette is not None:
                                    img[x, y] = cls.__palettecolor(palette, raw_pixel * 3)
                else:
                    # Loop thru pixels
                    for y in range(raw_h):
                        for x in range(raw_w):
                            raw_pixel = input.getpixel((x, y))
                            if isinstance(raw_pixel, tuple):
                                img[x, y] = cls.__tuple2pixel(raw_pixel)
            return img
        except Exception as e:
            error = _CLICommandError(e)
        raise error

    @classmethod
    def to_file(cls, img:_Img, path:str):
        """
        Saves an Img to a file
        
        :param img:
            Img to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        output = _Image.new('RGBA', (img.width, img.height))
        for y in range(img.height):
            for x in range(img.width):
                color = img[x, y]
                output.putpixel((x, y), (color.r, color.g, color.b, color.a))
        try:
            output.save(path)
            return
        except Exception as e:
            error = _CLICommandError(e)
        raise error

    #endregion

    #region image

    @classmethod
    def image_from_file(cls, path:str):
        """
        Creates an ImgImage by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created ImgImage
        :raise CLICommandError:
            An error occurred
        """
        try:
            with _Image.open(path) as input:
                raw_w, raw_h = input.size
                width = max(1, raw_w)
                height = max(1, raw_h)
                if input.mode == 'P' or input.mode == 'PA':
                    alpha = input.mode == 'PA'
                    # Get palette info
                    inpal = input.getpalette()
                    if inpal is not None:
                        palsize = len(inpal) // (4 if alpha else 3)
                    else:
                        palsize = 0
                    # Create image
                    image = _ImgImage(\
                        width = width,\
                        height = height,\
                        palsize = palsize,\
                        alpha = alpha)
                    # Populate palette
                    if inpal is not None:
                        palette = _cast(_ImgPalette, image.palette)
                        offset = 0
                        for i in range(_cast(int, palsize)):
                            if alpha:
                                palette[i] = _ImgColor(\
                                    r = inpal[offset],\
                                    g = inpal[offset + 1],\
                                    b = inpal[offset + 2],\
                                    a = inpal[offset + 3])
                                offset += 4
                            else:
                                palette[i] = _ImgColor(\
                                    r = inpal[offset],\
                                    g = inpal[offset + 1],\
                                    b = inpal[offset + 2])
                                offset += 3
                    # Loop thru pixels
                    for y in range(raw_h):
                        for x in range(raw_w):
                            raw_pixel = input.getpixel((x, y))
                            if isinstance(raw_pixel, int):
                                image[x, y] = raw_pixel
                elif input.mode == 'RGB' or input.mode == 'RGBA':
                    # Create image
                    image = _ImgImage(\
                        width = width,\
                        height = height,\
                        alpha = input.mode == 'RGBA')
                    # Loop thru pixels
                    for y in range(raw_h):
                        for x in range(raw_w):
                            raw_pixel = input.getpixel((x, y))
                            if isinstance(raw_pixel, tuple):
                                image[x, y] = cls.__tuple2pixel(raw_pixel)
                else:
                    raise _CLICommandError(f"{input.mode} images are not supported.")
            return image
        except Exception as e:
            error = _CLICommandError(e)
        raise error

    @classmethod
    def image_to_file(cls, image:_ImgImage, path:str):
        """
        Saves an ImgImage to a file\n
        NOTE: As of right now, paletted images will be saved as a non-paletted image
        
        :param image:
            ImgImage to save
        :param path:
            Path of output file
        :param noalpha:
            Whether or not to exclude alpha data in output
        :raise CLICommandError:
            An error occurred
        """
        # Create output
        imagesize = (image.width, image.height)
        if image.haspalette:
            _palette = _cast(_ImgPalette, image.palette)
            # Initialize image and palette
            if image.alpha:
                # Create image
                output = _Image.new('PA', imagesize)
                # Create palette
                _outpal:list[int] = []
                for _color in _palette:
                    _outpal.append(_color.r)
                    _outpal.append(_color.g)
                    _outpal.append(_color.b)
                    _outpal.append(_color.a)
                output.putpalette(_outpal, rawmode = 'RGBA')
            else:
                # Create image
                output = _Image.new('P', imagesize)
                # Create palette
                _outpal:list[int] = []
                for _color in _palette:
                    _outpal.append(_color.r)
                    _outpal.append(_color.g)
                    _outpal.append(_color.b)
                output.putpalette(_outpal, rawmode = 'RGB')
            # Set pixels
            for _y in range(image.height):
                for _x in range(image.width):
                    _raw = _cast(_np.uint8, image[_x, _y])
                    output.putpixel((_x, _y), int(_raw))
        else:
            output = _Image.new(\
                'RGBA' if image.alpha else 'RGB',\
                imagesize)
            for _y in range(image.height):
                for _x in range(image.width):
                    _raw = _cast(_ImgColor, image[_x, _y])
                    if image.alpha:
                        _color = (_raw.r, _raw.g, _raw.b, _raw.a)
                    else:
                        _color = (_raw.r, _raw.g, _raw.b)
                    output.putpixel((_x, _y), _color)
        # Save output
        try:
            output.save(path)
            return
        except Exception as e:
            error = _CLICommandError(e)
        raise error

    #endregion