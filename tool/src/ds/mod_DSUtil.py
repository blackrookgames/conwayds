__all__ = [\
    'DSUtil',]

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
from ..img.mod_ImgColor import\
    ImgColor as _ImgColor
from ..img.mod_ImgImage import\
    ImgImage as _ImgImage
from ..img.mod_ImgImagePPixels import\
    ImgImagePPixels as _ImgImagePPixels
from ..img.mod_ImgPalette import\
    ImgPalette as _ImgPalette

class DSUtil:
    """
    Utility for DS-related operations
    """

    __MASK_4 = _np.uint8(0xF)
    __MASK_8 = _np.uint8(0xFF)

    #region palette pal

    @classmethod
    def palette_get_pal(cls, imgpal:_ImgPalette):
        """
        Creates a DSPalette using data from an ImgPalette
        
        :param imgpal:
            Input ImgPalette
        """
        dspal = _DSPalette()
        for _i in range(len(imgpal)):
            dspal[_i] = _DSColorUtil.from_imgcolor(imgpal[_i])
        return dspal
    
    @classmethod
    def palette_set_pal(cls, imgpal:_ImgPalette, dspal:_DSPalette):
        """
        Outputs DSPalette colors onto an ImgPalette
        
        :param imgpal:
            Output ImgPalette
        :param dspal:
            Input DSPalette
        """
        imgpal.format(len(dspal))
        for _i in range(len(dspal)):
            imgpal[_i] = _DSColorUtil.to_imgcolor(dspal[_i])

    #endregion

    #region tileset img
    
    @classmethod
    def __tileset_load_img(cls, img:_ImgImage, tileset:_DSTileset, createtile:_Callable[[], _DSTile], mask:_np.uint8):
        if not img.haspalette:
            raise ValueError("img must be paletted.")
        # Rows and columns
        cols = img.width // _DSTILE_W
        rows = img.height // _DSTILE_H
        # Add tiles
        pixels = _cast(_ImgImagePPixels, img.pixels)
        for _i in range(cols * rows):
            _tile = createtile()
            _y0 = (_i // cols) * _DSTILE_H
            _x0 = (_i % cols) * _DSTILE_W
            for _y in range(_DSTILE_H):
                for _x in range(_DSTILE_W):
                    _tile[_x, _y] = pixels[_x0 + _x, _y0 + _y] & mask
            tileset.add(_tile)
    
    @classmethod
    def __tileset_set_img(cls, img:_ImgImage, tileset:_DSTileset, tpr:int):
        if not img.haspalette:
            raise ValueError("img must be paletted.")
        # Rows and columns
        cols = tpr if (tpr > 0) else len(tileset)
        rows = (len(tileset) + cols - 1) // cols
        # Setup image
        img.resize(cols * _DSTILE_W, rows * _DSTILE_H)
        # Add tiles
        pixels = _cast(_ImgImagePPixels, img.pixels)
        for _i in range(len(tileset)):
            _tile = tileset[_i]
            _x0 = (_i % cols) * _DSTILE_W
            _y0 = (_i // cols) * _DSTILE_H
            for _y in range(_DSTILE_H):
                for _x in range(_DSTILE_W):
                    pixels[_x0 + _x, _y0 + _y] = _tile[_x, _y]
        # Clear unused area
        _mod = len(tileset) % cols
        if _mod != 0:
            _x0 = img.width - (cols - _mod) * _DSTILE_W
            _y0 = img.height - _DSTILE_H
            for _y in range(_y0, img.height):
                for _x in range(_x0, img.width):
                    pixels[_x, _y] = 0
                    
    @classmethod
    def tileset4_get_img(cls, img:_ImgImage):
        """
        Creates a DSTileset4 using data from an ImgImage
        
        :param img:
            Input ImgImage (must be paletted)
        :return:
            Created DSTileset4
        :raise ValueError:
            img is not paletted
        """
        tileset = _DSTileset4()
        cls.__tileset_load_img(img, tileset, lambda : _DSTile4(), cls.__MASK_4)
        return tileset
    
    @classmethod
    def tileset4_set_img(cls, img:_ImgImage, tileset:_DSTileset4, tpr:int = 16):
        """
        Outputs DSTileset4 pixels onto an ImgImage
        
        :param img:
            Output ImgImage (must be paletted)
        :param tileset:
            Input DSTileset4
        :param tpr:
            Tiles per row (<= 0 means all tiles are on a single row)
        :raise ValueError:
            img is not paletted
        """
        return cls.__tileset_set_img(img, tileset, tpr)
    
    @classmethod
    def tileset8_get_img(cls, img:_ImgImage):
        """
        Creates a DSTileset8 using data from an ImgImage
        
        :param img:
            Input ImgImage (must be paletted)
        :return:
            Created DSTileset8
        :raise ValueError:
            img is not paletted
        """
        tileset = _DSTileset8()
        cls.__tileset_load_img(img, tileset, lambda : _DSTile8(), cls.__MASK_8)
        return tileset
    
    @classmethod
    def tileset8_set_img(cls, img:_ImgImage, tileset:_DSTileset8, tpr:int = 16):
        """
        Outputs DSTileset8 pixels onto an ImgImage
        
        :param img:
            Output ImgImage (must be paletted)
        :param tileset:
            Input DSTileset8
        :param tpr:
            Tiles per row (<= 0 means all tiles are on a single row)
        :raise ValueError:
            img is not paletted
        """
        return cls.__tileset_set_img(img, tileset, tpr)

    #endregion