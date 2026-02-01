__all__ = [\
    'DSSerial',]

from .mod_DSColor import\
    DSColor as _DSColor
from .mod_DSColorUtil import\
    DSColorUtil as _DSColorUtil
from .mod_DSPalette import\
    DSPalette as _DSPalette
from ..data.mod_DataBuffer import\
    DataBuffer as _DataBuffer
from ..img.mod_Img import\
    Img as _Img
from ..img.mod_ImgColor import\
    ImgColor as _ImgColor

class DSSerial:
    """
    Serialization utility
    """

    #region palette bin

    # @classmethod
    # def palette_from_bin(cls, bin:_DataBuffer):
    #     """
    #     Deserializes DSPalette binary data
    #     
    #     :param data:
    #         Input DataBuffer
    #     :return:
    #         Created DSPalette
    #     """
    #     palette = _DSPalette()
    #     count = min(len(palette), len(bin))
    #     for _i in range(count):
    #         palette[_i] = _DSColor()
    #     return palette

    # @classmethod
    # def palette_to_bin(cls, palette:_DSPalette):
    #     """
    #     Serializes DSPalette binary data
    #     
    #     :param data:
    #         Input DSPalette
    #     :return:
    #         Created DataBuffer
    #     """
    #     # Size
    #     img_w = cpr if (cpr > 0) else len(palette)
    #     img_h = max(1, (len(palette) + img_w - 1) // img_w) # Ensure there is at least one row
    #     # Create image
    #     img = _Img(img_w, img_h)
    #     for _i in range(len(palette)):
    #         img[_i % img_w, _i // img_w] = _DSColorUtil.to_imgcolor(palette[_i])
    #     # Return
    #     return img

    #endregion

    #region palette img

    @classmethod
    def palette_from_img(cls, img:_Img):
        """
        Deserializes DSPalette data from an Img
        
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
    def palette_to_img(cls, palette:_DSPalette, cpr:int = 16):
        """
        Serializes DSPalette data to an Img
        
        :param palette:
            Input DSPalette
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