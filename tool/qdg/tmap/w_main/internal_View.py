__all__ = ['_View']

import numpy as _np
import tkinter as _tk
import tkinter.ttk as _ttk

from dataclasses import\
    dataclass as _dataclass
from PIL import\
    Image as _Image,\
    ImageTk as _ImageTk

import qdg.helper as _qdg_helper
import qdg.tmap.w__common as _tmap_common

from .internal_ViewMap import *
from .internal_ViewRefArea import *
from .internal_ViewRefPnt import *

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
            tilesrc width is less than _tmap_common.TILESET_WIDTH\n
            or\n
            tilesrc height is less than _tmap_common.TILESET_HEIGHT
            or\n
            map_width is less than 1\n
            or\n
            map_height is less than 1
        """
        self.__initializing = True
        # Error check
        if tilesrc.size[0] < _tmap_common.TILESET_WIDTH:
            raise ValueError("Tileset width must be greater than or equal to _tmap_common.TILESET_WIDTH.")
        if tilesrc.size[1] < _tmap_common.TILESET_HEIGHT:
            raise ValueError("Tileset height must be greater than or equal to _tmap_common.TILESET_HEIGHT.")
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
        # grid
        self.__grid:list[int] = []
        for _x in range(0, 512, _tmap_common.TILESET_TILE_WIDTH):
            self.__grid.append(self.__canvas.create_line(\
                _x, 0, _x, 512, fill = "gray"))
        for _y in range(0, 512, _tmap_common.TILESET_TILE_HEIGHT):
            self.__grid.append(self.__canvas.create_line(\
                0, _y, 512, _y, fill = "gray"))
        self.__showgrid = True
        # ref_a
        self.__ref_a_visual = self.__canvas.create_rectangle(\
            -1, -1, _tmap_common.TILESET_TILE_WIDTH, _tmap_common.TILESET_TILE_HEIGHT,\
            outline = "white", width = 1)
        self.__ref_a = _ViewRefPnt(self,\
            lambda view: 0, lambda view: 0, lambda view: view.__map.width - 1, lambda view: view.__map.height - 1,\
            self.__redraw_ref_a)
        self.__ref_a.visible = True
        # ref_b
        self.__ref_b_visual = self.__canvas.create_rectangle(\
            0, 0, 3, 3,\
            outline = "white", width = 1)
        self.__ref_b = _ViewRefPnt(self,\
            lambda view: 0, lambda view: 0, lambda view: view.__map.width, lambda view: view.__map.height,\
            self.__redraw_ref_b)
        # ref_c
        self.__ref_c_visual = self.__canvas.create_rectangle(\
            0, 0, 3, 3,\
            outline = "white", width = 1)
        self.__ref_c = _ViewRefArea(self,\
            lambda view: 0, lambda view: 0, lambda view: view.__map.width, lambda view: view.__map.height,\
            self.__redraw_ref_c)
        # mouse_cell
        self.__mouse_cell = _qdg_helper.IXY_ZERO
        self.__mouse_cell_changed_h = _qdg_helper.SignalHandler[_View, _qdg_helper.IXY]()
        self.__mouse_cell_changed = _qdg_helper.Signal(self.__mouse_cell_changed_h)
        # mouse_snap
        self.__mouse_snap = _qdg_helper.IXY_ZERO
        self.__mouse_snap_changed_h = _qdg_helper.SignalHandler[_View, _qdg_helper.IXY]()
        self.__mouse_snap_changed = _qdg_helper.Signal(self.__mouse_snap_changed_h)
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
    def showgrid(self):
        """ Whether or not to display the grid"""
        return self.__showgrid
    @showgrid.setter
    def showgrid(self, value:bool):
        if self.__showgrid == value: return
        # Set value
        self.__showgrid = value
        # Update
        state = 'normal' if self.__showgrid else 'hidden'
        for _line in self.__grid:
            self.__canvas.itemconfigure(_line, state = state)

    @property
    def ref_a(self):
        """
        Reference A
        """
        return self.__ref_a

    @property
    def ref_b(self):
        """
        Reference B
        """
        return self.__ref_b

    @property
    def ref_c(self):
        """
        Reference C
        """
        return self.__ref_c

    @property
    def mouse_snap(self):
        """
        Snap position of mouse
        """
        return self.__mouse_snap
    
    @property
    def mouse_cell(self):
        """
        Cell position of mouse
        """
        return self.__mouse_cell

    #endregion

    #region signals

    @property
    def mouse_cell_changed(self):
        """ Emitted when the cell position of the mouse changes """
        return self.__mouse_cell_changed

    @property
    def mouse_snap_changed(self):
        """ Emitted when the snap position of the mouse changes """
        return self.__mouse_snap_changed

    #endregion

    #region receivers

    def __r_canvas_motion(self, event = None):
        if not isinstance(event, _tk.Event): return
        # Update cell position
        prev = self.__mouse_cell
        self.__mouse_cell = _qdg_helper.IXY(\
            x = event.x // _tmap_common.TILESET_TILE_WIDTH,\
            y = event.y // _tmap_common.TILESET_TILE_WIDTH)
        if self.__mouse_cell != prev: self.__mouse_cell_changed_h.emit(self, self.__mouse_cell)
        # Update snap position
        prev = self.__mouse_snap
        self.__mouse_snap = _qdg_helper.IXY(\
            x = round(event.x / _tmap_common.TILESET_TILE_WIDTH),\
            y = round(event.y / _tmap_common.TILESET_TILE_WIDTH))
        if self.__mouse_snap != prev: self.__mouse_snap_changed_h.emit(self, self.__mouse_snap)

    #endregion

    #region helper methods 1

    def __tileimg(self, index:_np.uint16):
        """
        Assume
        - index >= 0 and index < 0x10000
        """
        _xx, _yy = _tmap_common.Tileset.offset(index)
        _box = (_xx, _yy, _xx + _tmap_common.TILESET_TILE_WIDTH, _yy + _tmap_common.TILESET_TILE_HEIGHT)
        return _ImageTk.PhotoImage(self.__tilesrc.crop(_box))
    
    def __tile_inc(self, x:int, y:int, index:_np.uint16):
        # Increment new
        if not (index in self.__tilecache):
            self.__tilecache[index] = self.__TileCacheItem(self.__tileimg(index), 1)
        else: self.__tilecache[index].refs += 1
        # Create new tile image
        _image = self.__canvas.create_image(\
            x * _tmap_common.TILESET_TILE_WIDTH, y * _tmap_common.TILESET_TILE_HEIGHT,\
            anchor = 'nw',\
            image = self.__tilecache[index].image)
        self.__canvas.tag_lower(_image, self.__grid[0])
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
            width = self.__map.width * _tmap_common.TILESET_TILE_WIDTH,\
            height = self.__map.height * _tmap_common.TILESET_TILE_HEIGHT)

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
    
    def __redraw_ref_a(self, ref:_ViewRefPnt):
        if ref.visible:
            x = ref.position.x * _tmap_common.TILESET_TILE_WIDTH - 2
            y = ref.position.y * _tmap_common.TILESET_TILE_HEIGHT - 2
        else:
            x = -_tmap_common.TILESET_TILE_WIDTH * 2
            y = -_tmap_common.TILESET_TILE_WIDTH * 2
        self.__canvas.moveto(self.__ref_a_visual, x, y)

    def __redraw_ref_b(self, ref:_ViewRefPnt):
        if ref.visible:
            x = ref.position.x * _tmap_common.TILESET_TILE_WIDTH - 3
            y = ref.position.y * _tmap_common.TILESET_TILE_HEIGHT - 3
        else:
            x = -_tmap_common.TILESET_TILE_WIDTH
            y = -_tmap_common.TILESET_TILE_HEIGHT
        self.__canvas.moveto(self.__ref_b_visual, x, y)

    def __redraw_ref_c(self, ref:_ViewRefArea):
        if ref.visible:
            x0 = ref.pnt0.x * _tmap_common.TILESET_TILE_WIDTH
            y0 = ref.pnt0.y * _tmap_common.TILESET_TILE_HEIGHT
            x1 = ref.pnt1.x * _tmap_common.TILESET_TILE_WIDTH - 1
            y1 = ref.pnt1.y * _tmap_common.TILESET_TILE_HEIGHT - 1
        else:
            x0 = -2
            y0 = -2
            x1 = -1
            y1 = -1
        self.__canvas.coords(self.__ref_c_visual, x0, y0, x1, y1)

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
        self.__ref_a._update_position()
        self.__ref_b._update_position()
        self.__ref_c._update_pnts()
    
    #endregion