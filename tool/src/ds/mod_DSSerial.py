__all__ = [\
    'DSSerial',]

import numpy as _np

from typing import\
    Callable as _Callable,\
    cast as _cast

from .mod_DSColor import\
    DSColor as _DSColor
from .mod_DSColorUtil import\
    DSColorUtil as _DSColorUtil
from .mod_DSPalette import\
    DSPalette as _DSPalette
from .mod_DSTile import\
    DSTile as _DSTile,\
    DSTILE_W as _DSTILE_W,\
    DSTILE_H as _DSTILE_H
from .mod_DSTile4 import\
    DSTile4 as _DSTile4
from .mod_DSTile8 import\
    DSTile8 as _DSTile8
from .mod_DSTileset import\
    DSTileset as _DSTileset
from .mod_DSTileset4 import\
    DSTileset4 as _DSTileset4
from .mod_DSTileset8 import\
    DSTileset8 as _DSTileset8
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

    @classmethod
    def palette_from_bin(cls, bin:_DataBuffer):
        """
        Deserializes DSPalette binary data
        
        :param bin:
            Input DataBuffer
        :return:
            Created DSPalette
        """
        palette = _DSPalette()
        count = min(len(palette), len(bin) // 2)
        bin.set_cursor(0)
        for _i in range(count):
            palette[_i] = _DSColor(bin.read_int16_l())
        return palette

    @classmethod
    def palette_to_bin(cls, palette:_DSPalette, noalpha:bool = False):
        """
        Serializes DSPalette binary data
        
        :param palette:
            Input DSPalette
        :param noalpha:
            Whether or not to ignore alpha
        :return:
            Created DataBuffer
        """
        buffer = _DataBuffer(len(palette) * 2)
        getvalue = _DSColor.to15 if noalpha else _DSColor.to16
        for _color in palette:
            buffer.write_uint16_l(int(getvalue(_color)))
        return buffer

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
    def palette_to_img(cls, palette:_DSPalette, noalpha:bool = False, cpr:int = 16):
        """
        Serializes DSPalette data to an Img
        
        :param palette:
            Input DSPalette
        :param noalpha:
            Whether or not to ignore alpha
        :param cpr:
            Colors per row (<= 0 means all colors are on a single row)
        :return:
            Created Img
        """
        # Size
        img_w = cpr if (cpr > 0) else len(palette)
        img_h = max(1, (len(palette) + img_w - 1) // img_w) # Ensure there is at least one row
        # Create image
        img = _Img(img_w, img_h)
        for _i in range(len(palette)):
            _color = _DSColorUtil.to_imgcolor(palette[_i])
            if noalpha: _color = _ImgColor(r = _color.r, g = _color.g, b = _color.b)
            img[_i % img_w, _i // img_w] = _color
        # Return
        return img

    #endregion

    #region tileset bin
    
    @classmethod
    def __tileset_loop_pixels(cls, tileset:_DSTileset):
        for _tile in tileset:
            for _y in range(_DSTILE_H):
                for _x in range(_DSTILE_W):
                    yield int(_tile[_x, _y])
                    
    @classmethod
    def tileset4_from_bin(cls, bin:_DataBuffer) -> _DSTileset4:
        """
        Deserializes DSTilset4 binary data
        
        :param bin:
            Input DataBuffer
        :return:
            Created DSTileset4
        """
        raise NotImplementedError("tileset4_from_bin has not yet been implemeneted.")
    
    @classmethod
    def tileset4_to_bin(cls, tileset:_DSTileset4):
        """
        Serializes DSTileset4 binary data
        
        :param tileset:
            Input DSTileset4
        :return:
            Created DataBuffer
        """
        bin = _DataBuffer(size = (len(tileset) * _DSTILE_W * _DSTILE_H) // 2)
        _STEPS = 2
        _value = 0
        _i = _STEPS
        for _pixel in cls.__tileset_loop_pixels(tileset):
            # Update value
            _value <<= 4
            _value |= _pixel
            # Next
            if _i == 1:
                bin.write_uint8(_value)
                _value = 0
                _i = _STEPS
            else: _i -= 1
        return bin
    
    @classmethod
    def tileset8_from_bin(cls, bin:_DataBuffer) -> _DSTileset8:
        """
        Deserializes DSTilset8 binary data
        
        :param bin:
            Input DataBuffer
        :return:
            Created DSTileset8
        """
        raise NotImplementedError("tileset8_from_bin has not yet been implemeneted.")
    
    @classmethod
    def tileset8_to_bin(cls, tileset:_DSTileset8):
        """
        Serializes DSTileset8 binary data
        
        :param tileset:
            Input DSTileset8
        :return:
            Created DataBuffer
        """
        bin = _DataBuffer(size = len(tileset) * _DSTILE_W * _DSTILE_H)
        for _pixel in cls.__tileset_loop_pixels(tileset):
            bin.write_uint8(_pixel)
        return bin

    #endregion