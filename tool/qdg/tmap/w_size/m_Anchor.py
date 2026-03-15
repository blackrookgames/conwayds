from enum import\
    auto as _auto,\
    Enum as _Enum

class Anchor(_Enum):
    """
    Represents an anchor setting
    """

    TOPLEFT = 0
    """ Top-left """
    
    TOP = _auto()
    """ Top """

    TOPRIGHT = _auto()
    """ Top-right """

    LEFT = _auto()
    """ Left """
    
    CENTER = _auto()
    """ Center """

    RIGHT = _auto()
    """ Right """

    BOTTOMLEFT = _auto()
    """ Bottom-left """
    
    BOTTOM = _auto()
    """ Bottom """

    BOTTOMRIGHT = _auto()
    """ Bottom-right """