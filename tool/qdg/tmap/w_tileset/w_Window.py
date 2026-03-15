__all__ = ['Window']

import numpy as _np
import tkinter as _tk
import tkinter.ttk as _ttk
import tkinter.messagebox as _tk_messagebox

from PIL import\
    Image as _Image,\
    ImageTk as _ImageTk

import qdg.helper as _qdg_helper
import qdg.tmap.w__common as _tmap_common
import src.helper as _helper

class Window(_qdg_helper.WinDialog):
    """
    Represents a window for selecting a tile
    """

    #region init

    def __init__(self,\
            tilesrc:_Image.Image,\
            init_final:_np.uint16 = _np.uint16(0),\
            *args, **kwargs):
        """
        Initializer for Window

        :param init_final: Initial "final tile value"
        """
        # Initialize
        super().__init__(*args, **kwargs)
        self._set_result(_qdg_helper.WinDialogResult.CANCEL)
        self.title("Tileset")
        self.resizable(False, False)
        self.config(padx = 2, pady = 2)
        # Final Tile Value
        self.__final = init_final
        # Tileset
        self.__tileset:list[_ImageTk.PhotoImage] = []
        for _i in range(_tmap_common.TILESET_SUBS):
            _x = (_i % _tmap_common.TILESET_SUBS_PERROW) * _tmap_common.TILESET_SUB_WIDTH
            _y = (_i // _tmap_common.TILESET_SUBS_PERROW) * _tmap_common.TILESET_SUB_HEIGHT
            _box = (_x, _y, _x + _tmap_common.TILESET_SUB_WIDTH, _y + _tmap_common.TILESET_SUB_HEIGHT)
            self.__tileset.append(_ImageTk.PhotoImage(tilesrc.crop(_box)))
        # Tile
        self.__widget_tile = _ttk.Label(\
            master = self,\
            width = 12,\
            font = _qdg_helper.FONT_SMALL)
        self.__widget_tile.grid(column = 0, row = 0, sticky = 'w')
        # Palette
        self.__widget_palette = _ttk.Label(\
            master = self,\
            width = 12,\
            font = _qdg_helper.FONT_SMALL)
        self.__widget_palette.grid(column = 1, row = 0, sticky = 'w')
        # Orientation
        self.__widget_orientation = _ttk.Label(\
            master = self,\
            width = 12,\
            font = _qdg_helper.FONT_SMALL)
        self.__widget_orientation.grid(column = 2, row = 0, sticky = 'w')
        # Canvas
        self.__widget_canvas = _tk.Canvas(\
            master = self,\
            borderwidth = 0,\
            highlightthickness = 0,\
            width = 256,\
            height = 256)
        self.__widget_canvas.bind("<Motion>", self.__r_widget_canvas_motion)
        self.__widget_canvas.grid(column = 0, row = 1, columnspan = 3)
        # Canvas Tile
        self.__canvas_tile = self.__widget_canvas.create_rectangle(\
            -1, -1, _tmap_common.TILESET_TILE_WIDTH, _tmap_common.TILESET_TILE_HEIGHT,\
            outline = "white", width = 1)
        # Canvas Tileset
        self.__canvas_tileset_index = -1
        self.__canvas_tileset:None|int = None
        # Input
        self.bind('<Button-1>', self.__r_input_select)
        self.bind('<F3>', self.__r_input_palette)
        self.bind('<F4>', self.__r_input_orientation)
        # Post-init
        self.__refresh_widgets()
    
    #endregion

    #region properties

    @property
    def final(self):
        """ Final tile value """
        return self.__final
        
    #endregion

    #region receivers

    def __r_widget_canvas_motion(self, event = None):
        if not isinstance(event, _tk.Event): return
        tile, palette, orientation = _tmap_common.finaltile_from(self.__final)
        prev = tile
        # Compute tile
        x = max(0, min(_tmap_common.TILESET_SUB_COLS - 1, event.x // _tmap_common.TILESET_TILE_WIDTH))
        y = max(0, min(_tmap_common.TILESET_SUB_ROWS - 1, event.y // _tmap_common.TILESET_TILE_WIDTH))
        tile = x + y * _tmap_common.TILESET_SUB_COLS
        if tile == prev: return
        # Update final
        self.__final = _tmap_common.finaltile_to(tile, palette, orientation)
        self.__refresh_widgets()

    def __r_input_select(self, event = None):
        self._set_result(_qdg_helper.WinDialogResult.OK)
        self.destroy()

    def __r_input_palette(self, event = None):
        self.__inc_palette()

    def __r_input_orientation(self, event = None):
        self.__inc_orientation()

    #endregion

    #region helper

    def __refresh_widgets(self):
        _WRAP = _tmap_common.TILESET_SUB_COLS * _tmap_common.TILESET_SUB_ROWS
        tile, palette, orientation = _tmap_common.finaltile_from(self.__final)
        # Tile
        self.__widget_tile.config(text = f"Tile: 0x{tile:03X}")
        # Palette
        self.__widget_palette.config(text = f"Palette: 0x{palette:01X}")
        # Orientation
        self.__widget_orientation.config(text = f"Orient: {orientation}")
        # Canvas Tile
        tile_x = (tile % _tmap_common.TILESET_SUB_COLS) * _tmap_common.TILESET_TILE_WIDTH - 2
        tile_y = (tile // _tmap_common.TILESET_SUB_COLS) * _tmap_common.TILESET_TILE_HEIGHT - 2
        self.__widget_canvas.moveto(self.__canvas_tile, x = tile_x, y = tile_y)
        # Canvas Tileset
        _subindex = int(self.__final) // _WRAP
        if self.__canvas_tileset_index != _subindex:
            self.__canvas_tileset_index = _subindex
            # Delete old
            if self.__canvas_tileset is not None:
                self.__widget_canvas.delete(self.__canvas_tileset)
            # Create new
            self.__canvas_tileset = self.__widget_canvas.create_image(0, 0,\
                anchor = 'nw', image = self.__tileset[_subindex])
            self.__widget_canvas.tag_lower(self.__canvas_tileset, self.__canvas_tile)
        
    
    def __inc_tile(self, value:int):
        _WRAP = _tmap_common.TILESET_SUB_COLS * _tmap_common.TILESET_SUB_ROWS
        tile, palette, orientation = _tmap_common.finaltile_from(self.__final)
        self.__final = _tmap_common.finaltile_to(_WRAP + tile + value, palette, orientation)
        self.__refresh_widgets()

    def __inc_palette(self):
        tile, palette, orientation = _tmap_common.finaltile_from(self.__final)
        self.__final = _tmap_common.finaltile_to(tile, palette + 1, orientation)
        self.__refresh_widgets()
        
    def __inc_orientation(self):
        tile, palette, orientation = _tmap_common.finaltile_from(self.__final)
        self.__final = _tmap_common.finaltile_to(tile, palette, orientation + 1)
        self.__refresh_widgets()

    #endregion