__all__ = [\
    '_View',\
    '_VIEW_TILESRC_WIDTH',\
    '_VIEW_TILESRC_HEIGHT']

import numpy as _np
import tkinter as _tk
import tkinter.ttk as _ttk

from dataclasses import\
    dataclass as _dataclass
from PIL import\
    Image as _Image,\
    ImageTk as _ImageTk

import qdg.helper as _qdg_helper

from .internal_ViewMap import *

_VIEW_TILESRC_WIDTH = 2048
_VIEW_TILESRC_HEIGHT = 2048
_VIEW_TILE_WIDTH = 8
_VIEW_TILE_HEIGHT = 8
_VIEW_TILE_COLS = _VIEW_TILESRC_WIDTH // _VIEW_TILE_WIDTH

class _View(_ttk.Frame):
    """
    Represents a tilemap view
    """

    #region nested

    @_dataclass
    class __TileCacheItem:
        image:_ImageTk.PhotoImage
        refs:int

    #endregion

    #region init

    def __init__(self,\
            tilesrc:_Image.Image,\
            map_width:int = 1,\
            map_height:int = 1,\
            **kwargs):
        """
        Initializer for View

        :param content:Content to edit
        :param tilesrc: Source image representation of tileset
        :param map_width: Tilemap width (in cells)
        :param map_height: Tilemap height (in cells)

        :raise ValueError:
            tilesrc width is less than _VIEW_TILESRC_WIDTH\n
            or\n
            tilesrc height is less than _VIEW_TILESRC_HEIGHT
            or\n
            map_width is less than 1\n
            or\n
            map_height is less than 1
        """
        self.__initializing = True
        # Error check
        if tilesrc.size[0] < _VIEW_TILESRC_WIDTH:
            raise ValueError("Tileset width must be greater than or equal to _VIEW_TILESRC_WIDTH.")
        if tilesrc.size[1] < _VIEW_TILESRC_HEIGHT:
            raise ValueError("Tileset height must be greater than or equal to _VIEW_TILESRC_HEIGHT.")
        if map_width < 1:
            raise ValueError("map_width must be greater than or equal to 1.")
        if map_height < 1:
            raise ValueError("map_height must be greater than or equal to 1.")
        # Initialize
        super().__init__(**kwargs)
        # tilesrc
        self.__tilesrc = tilesrc
        # canvas
        self.__canvas = _tk.Canvas(\
            master = self,\
            borderwidth = 0,\
            highlightthickness = 0,\
            background = 'gray')
        self.__canvas.pack(fill = 'both', expand = True)
        self.__canvas.propagate(False)
        self.__canvas.bind("<Motion>", self.__r_canvas_motion)
        # tilecache
        self.__tilecache:dict[_np.uint16, _View.__TileCacheItem] = {}
        # map
        self._map_defined = False # Accessed by ViewMap
        self.__map = _ViewMap(self, map_width, map_height)
        self._map_defined = True
        # tiles
        self.__tiles:dict[_qdg_helper.IXY, int] = {}
        # cursor
        self.__cursor = _qdg_helper.IXY_ZERO
        self.__cursor_visual = self.__canvas.create_rectangle(\
            -1, -1, _VIEW_TILE_WIDTH, _VIEW_TILE_HEIGHT,\
            outline = "white", width = 1)
        # mouse
        self.__mouse = _qdg_helper.IXY_ZERO
        self.__mouse_changed_h = _qdg_helper.SignalHandler[_View, _qdg_helper.IXY]()
        self.__mouse_changed = _qdg_helper.Signal(self.__mouse_changed_h)
        # Post-init
        self.__refresh_size()
        self.__refresh_tiles()
        # Success!!!
        self.__initializing = False

    #endregion

    #region properties

    @property
    def map(self):
        """ Tilemap """
        return self.__map

    @property
    def cursor(self):
        """
        Cell position of cursor. Cursor is a point of reference
        """
        return self.__cursor
    @cursor.setter
    def cursor(self, value:_qdg_helper.IXY):
        self.__set_cursor(value)

    @property
    def mouse(self):
        """
        Cell position of mouse
        """
        return self.__mouse

    #endregion

    #region signals

    @property
    def mouse_changed(self):
        """ Emitted when the mouse position changes """
        return self.__mouse_changed

    #endregion

    #region receivers

    def __r_canvas_motion(self, event = None):
        if not isinstance(event, _tk.Event): return
        prev = self.__mouse
        self.__mouse = _qdg_helper.IXY(x = event.x // _VIEW_TILE_WIDTH, y = event.y // _VIEW_TILE_WIDTH)
        if self.__mouse != prev: self.__mouse_changed_h.emit(self, self.__mouse)

    #endregion

    #region helper methods 1

    def __tileimg(self, index:int):
        """
        Assume
        - index >= 0 and index < 0x10000
        """
        _xx = (index % _VIEW_TILE_COLS) * _VIEW_TILE_WIDTH
        _yy = (index // _VIEW_TILE_COLS) * _VIEW_TILE_HEIGHT
        _box = (_xx, _yy, _xx + _VIEW_TILE_WIDTH, _yy + _VIEW_TILE_HEIGHT)
        return _ImageTk.PhotoImage(self.__tilesrc.crop(_box))
    
    def __tile_inc(self, x:int, y:int, index:_np.uint16):
        # Increment new
        if not (index in self.__tilecache):
            self.__tilecache[index] = self.__TileCacheItem(self.__tileimg(int(index)), 1)
        else: self.__tilecache[index].refs += 1
        # Create new tile image
        _image = self.__canvas.create_image(\
            x * _VIEW_TILE_WIDTH, y * _VIEW_TILE_HEIGHT,\
            anchor = 'nw',\
            image = self.__tilecache[index].image)
        self.__canvas.tag_lower(_image, self.__cursor_visual)
        self.__tiles[_qdg_helper.IXY(x = x, y = y)] = _image

    def __tile_dec(self, x:int, y:int, index:_np.uint16):
        xy = _qdg_helper.IXY(x = x, y = y)
        # Delete old tile image
        if xy in self.__tiles:
            self.__canvas.delete(self.__tiles[xy])
        # Decrement old reference
        if index in self.__tilecache:
            _item = self.__tilecache[index]
            _item.refs -= 1
            if _item.refs <= 0: del self.__tilecache[index]
    
    def __refresh_size(self):
        self.__canvas.config(\
            width = self.__map.width * _VIEW_TILE_WIDTH,\
            height = self.__map.height * _VIEW_TILE_HEIGHT)

    def __refresh_tiles(self):
        # Clear cache
        self.__tilecache.clear()
        # Delete tile images
        for _tile in self.__tiles.values():
            self.__canvas.delete(_tile)
        self.__tiles.clear()
        # Redraw
        for _y in range(self.__map.height):
            for _x in range(self.__map.width):
                self.__tile_inc(_x, _y, self.__map[_x, _y])
    
    def __set_cursor(self, value:None|_qdg_helper.IXY):
        if value is not None:
            if self.__cursor == value: return
            self.__cursor = value
        # Fix value
        self.__cursor = _qdg_helper.IXY(\
            x = max(0, min(self.__map.width - 1, self.__cursor.x)),\
            y = max(0, min(self.__map.height - 1, self.__cursor.y)))
        # Update visual
        self.__canvas.moveto(self.__cursor_visual,\
            x = self.__cursor.x * _VIEW_TILE_WIDTH - 2,\
            y = self.__cursor.y * _VIEW_TILE_HEIGHT - 2)
        # Fix cursor

    #endregion

    #region helper methods 2
    
    def _raise_if_init(self):
        """ Accessed by _ViewMap """
        if not self.__initializing: raise ValueError("View has already been initialized")

    def _map_tilechanged(self, x:int, y:int, old:_np.uint16, new:_np.uint16):
        """
        Assume
        - x >= 0 and x < self.__map.width
        - y >= 0 and y < self.__map.height
        \n
        Accessed by _ViewMap
        """
        if old == new: return
        self.__tile_dec(x, y, old)
        self.__tile_inc(x, y, new)

    def _map_formatted(self):
        """ Accessed by _ViewMap """
        self.__refresh_size()
        self.__refresh_tiles()
        self.__set_cursor(None)
    
    #endregion