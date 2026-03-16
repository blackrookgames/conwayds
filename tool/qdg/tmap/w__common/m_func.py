__all__ = [\
    'finaltile_to',\
    'finaltile_from',]

import numpy as _np

_TILE_MASK = 0b1111111111
_TILE_SHIFT = 0
_PALETTE_MASK = 0b1111
_PALETTE_SHIFT = 12
_ORIENT_MASK = 0b11
_ORIENT_SHIFT = 10

def finaltile_to(tile:int, palette:int, orientation:int):
    """
    Computes a final tile value

    :param tile: Tile index
    :param palette: Palette index
    :param orientation Orientation
    :return: Computed value
    """
    return _np.uint16(\
        ((tile & _TILE_MASK) << _TILE_SHIFT) |\
        ((palette & _PALETTE_MASK) << _PALETTE_SHIFT) |\
        ((orientation & _ORIENT_MASK) << _ORIENT_SHIFT))

def finaltile_from(value:_np.uint16):
    """
    Extracts a final tile value

    :param finaltile: Final tile value
    :return: Extracted tile index, palette index, and orientation
    """
    v = int(value)
    return\
        (v >> _TILE_SHIFT) & _TILE_MASK,\
        (v >> _PALETTE_SHIFT) & _PALETTE_MASK,\
        (v >> _ORIENT_SHIFT) & _ORIENT_MASK