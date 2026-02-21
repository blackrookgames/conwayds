__all__ = [\
    'LifeUtil',]

from .mod_LifePattern import\
    LifePattern as _LifePattern
from ..img.mod_ImgColor import\
    ImgColor as _ImgColor
from ..img.mod_ImgImage import\
    ImgImage as _ImgImage
from ..img.mod_ImgImageRGBAPixels import\
    ImgImageRGBAPixels as _ImgImageRGBAPixels

class LifeUtil:
    """
    Utility for life-related operations
    """

    __COLOR_LIVE = _ImgColor(r = 255, g = 255, b = 255)
    __COLOR_DEAD = _ImgColor()

    #region pattern img
    
    @classmethod
    def pattern_get_img(cls, img:_ImgImage):
        """
        Creates a LifePattern using data from an ImgImage
        
        :param img:
            Input ImgImage
        :return:
            Created LifePattern
        """
        pattern = _LifePattern(width = img.width, height = img.height)
        for _y in range(img.height):
            for _x in range(img.width):
                _pixel = img.getpixel(_x, _y)
                _alive = False if (_pixel is None)\
                    else (_pixel.r >= 128 and _pixel.g >= 128 and _pixel.b >= 128)
                pattern[_x, _y] = _alive
        return pattern
    
    @classmethod
    def pattern_set_img(cls, img:_ImgImage, pattern:_LifePattern):
        """
        Outputs LifePattern pixels onto an ImgImage
        
        :param img:
            Output ImgImage
        :param bitmap:
            Input LifePattern
        """
        img.format(width = pattern.width, height = pattern.height)
        assert isinstance(img.pixels, _ImgImageRGBAPixels)
        for _y in range(pattern.height):
            for _x in range(pattern.width):
                img.pixels[_x, _y] = cls.__COLOR_LIVE if pattern[_x, _y] else cls.__COLOR_DEAD
    
    #endregion