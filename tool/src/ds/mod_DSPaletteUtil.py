__all__ = [\
    'DSPaletteUtil',]

from .mod_DSColor import\
    DSColor as _DSColor
from .mod_DSColorUtil import\
    DSColorUtil as _DSColorUtil
from .mod_DSPalette import\
    DSPalette as _DSPalette
from ..img.mod_Img import\
    Img as _Img
from ..img.mod_ImgColor import\
    ImgColor as _ImgColor

class DSPaletteUtil:
    """
    Utility for DSPalette
    """

    #region img

    @classmethod
    def from_img(cls, img:_Img):
        """
        Creates a DSPalette from an Img
        
        :param img:
            Input Img
        :return:
            Created DSPalette
        """
        palette = _DSPalette()
        count = min(len(palette), img.width * img.height)
        for _i in range(count):
            palette[_i] = _DSColorUtil.from_imgcolor(img[_i % img.width, _i // img.width])
        return palette

    @classmethod
    def to_img(cls, palette:_DSPalette, cpr:int = 16):
        """
        Creates an Img from a DSPalette
        
        :param palette:
            Input DSPalette
        :param cpr:
            Colors per row (<= 0 means all colors will exist along a single row)
        :return:
            Created Img
        """
        # Size
        img_w = cpr if (cpr > 0) else len(palette)
        img_h = max(1, (len(palette) + img_w - 1) // img_w) # Ensure there is at least one row
        # Create image
        img = _Img(img_w, img_h)
        for _i in range(len(palette)):
            img[_i % img_w, _i // img_w] = _DSColorUtil.to_imgcolor(palette[_i])
        # Return
        return img

    #endregion