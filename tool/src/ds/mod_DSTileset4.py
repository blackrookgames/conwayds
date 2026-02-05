__all__ = [\
    'DSTileset4',]

from .mod_DSTile4 import\
    DSTile4 as _DSTile4
from .mod_DSTileset import\
    DSTileset as _DSTileset

class DSTileset4(_DSTileset[_DSTile4]):
    """
    Represents a DS 4bpp tileset
    """

    #region init

    def __init__(self):
        """
        Initializer for DSTileset4
        """
        super().__init__()

    #endregion

    #region helper methods
    
    def _validatetile(self, tile):
        if not isinstance(tile, _DSTile4):
            raise TypeError("Tile type must be DSTile4.")
        return tile

    #endregion