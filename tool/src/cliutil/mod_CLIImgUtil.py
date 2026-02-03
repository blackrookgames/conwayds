__all__ = [\
    'CLIImgUtil',]

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
                if input.mode == 'P':
                    palette = input.getpalette()
                    if palette is not None and len(palette) > 0:
                        palettesize = len(palette) // 3
                    else:
                        palette = None
                        palettesize = 0
                    # Create image
                    image = _ImgImage(width = width, height = height, palettesize = palettesize)
                    # Populate palette
                    if palette is not None:
                        image_palette = _cast(_ImgPalette, image.palette)
                        offset = 0
                        for i in range(_cast(int, palettesize)):
                            image_palette[i] = cls.__palettecolor(palette, offset)
                            offset += 3
                    # Loop thru pixels
                    for y in range(raw_h):
                        for x in range(raw_w):
                            raw_pixel = input.getpixel((x, y))
                            if isinstance(raw_pixel, int):
                                image[x, y] = raw_pixel
                else:
                    # Create image
                    image = _ImgImage(width = width, height = height)
                    # Loop thru pixels
                    for y in range(raw_h):
                        for x in range(raw_w):
                            raw_pixel = input.getpixel((x, y))
                            if isinstance(raw_pixel, tuple):
                                image[x, y] = cls.__tuple2pixel(raw_pixel)
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
        :raise CLICommandError:
            An error occurred
        """
        output = _Image.new('RGBA', (image.width, image.height))
        for y in range(image.height):
            for x in range(image.width):
                color = image.getpixel(x, y)
                if color is None:
                    color = _ImgColor(a = 0)
                output.putpixel((x, y), (color.r, color.g, color.b, color.a))
        try:
            output.save(path)
            return
        except Exception as e:
            error = _CLICommandError(e)
        raise error

    #endregion