__all__ = [\
    'DSTileset8',]

from .mod_DSTile8 import\
    DSTile8 as _DSTile8
from .mod_DSTileset import\
    DSTileset as _DSTileset

class DSTileset8(_DSTileset[_DSTile8]):
    """
    Represents a DS 8bpp tileset
    """

    #region init

    def __init__(self):
        """
        Initializer for DSTileset8
        """
        super().__init__()

    #endregion

    #region helper methods
    
    def _validatetile(self, tile):
        if not isinstance(tile, _DSTile8):
            raise TypeError("Tile type must be DSTile8.")
        return tile

    #endregion