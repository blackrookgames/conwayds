__all__ = [\
    'DSTile8',]

import numpy as _np
from .mod_DSTile import\
    DSTile as _DSTile

class DSTile8(_DSTile):
    """
    Represents a DS 8bpp tile
    """

    #region init

    def __init__(self):
        """
        Initializer for DSTile8
        """
        super().__init__()

    #endregion