import numpy as _np

TILESET_TILE_COUNT = 0x10000
TILESET_TILE_WIDTH = 8
TILESET_TILE_HEIGHT = 8
TILESET_COLS = 256
TILESET_ROWS = 256
TILESET_WIDTH = TILESET_TILE_WIDTH * TILESET_COLS
TILESET_HEIGHT = TILESET_TILE_HEIGHT * TILESET_ROWS
TILESET_SUBS_PERROW = 8
TILESET_SUBS_PERCOL = 8
TILESET_SUBS = TILESET_SUBS_PERROW * TILESET_SUBS_PERCOL
TILESET_SUB_COLS = TILESET_COLS // TILESET_SUBS_PERROW
TILESET_SUB_ROWS = TILESET_ROWS // TILESET_SUBS_PERCOL
TILESET_SUB_WIDTH = TILESET_WIDTH // TILESET_SUBS_PERROW
TILESET_SUB_HEIGHT = TILESET_HEIGHT // TILESET_SUBS_PERCOL

class Tileset:
    """ Tileset info """

    #region offset

    @classmethod
    def offset(cls, finaltile:_np.uint16):
        """
        Computes the offset of the specified final tile value

        :param finaltile: Final tile value
        :return: Computed offset
        """
        sub = int(finaltile % 1024)
        squ = int(finaltile // 1024)
        x = (squ % TILESET_SUBS_PERROW) * TILESET_SUB_WIDTH + (sub % TILESET_SUB_COLS) * TILESET_TILE_WIDTH
        y = (squ // TILESET_SUBS_PERROW) * TILESET_SUB_HEIGHT + (sub // TILESET_SUB_COLS) * TILESET_TILE_HEIGHT
        return x, y

    #endregion