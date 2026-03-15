__all__ = ['Window']

import numpy as _np
import tkinter as _tk
import tkinter.ttk as _ttk
import tkinter.messagebox as _tk_messagebox

from PIL import\
    Image as _Image,\
    ImageTk as _ImageTk

from .internal_Foot import *
from .internal_Head import *
from .internal_View import *
import qdg.helper as _qdg_helper
import qdg.tmap.w__common as _tmap_common
import qdg.tmap.w_help as _tmap_help
import qdg.tmap.w_size as _tmap_size
import qdg.tmap.w_tileset as _tmap_tileset

_PAD_X = 2
_PAD_Y = 2
_TILE_W = 8
_TILE_H = 8

class Window(_tk.Tk):
    """
    Represents a main window
    """

    #region init

    def __init__(self,\
            content:_tmap_common.Content,\
            tilesrc:_Image.Image,\
            *args, **kwargs):
        """
        Initializer for Window

        :param content:Content to edit
        :param tilesrc: Source image representation of tileset (must be 2048x2048)

        :raise ValueError:
            tilesrc width is less than 2048\n
            or\n
            tilesrc height is less than 2048
        """
        self.__initializing = True
        # Error check
        if tilesrc.size[0] < _tmap_common.TILESET_WIDTH:
            raise ValueError(f"Tileset width must be greater than or equal to {_tmap_common.TILESET_WIDTH}.")
        if tilesrc.size[1] < _tmap_common.TILESET_HEIGHT:
            raise ValueError(f"Tileset height must be greater than or equal to {_tmap_common.TILESET_HEIGHT}.")
        # Initialize
        super().__init__(*args, **kwargs)
        self.resizable(width = False, height = False)
        self.config(padx = _PAD_X, pady = _PAD_Y)
        self.protocol("WM_DELETE_WINDOW", self.__r_wm_delete_window)
        self.pack_propagate(True)
        # content
        self.__content = content
        # tilesrc
        self.__tilesrc = tilesrc
        # isdirty
        self.__isdirty:bool = False
        # textmode
        self.__textmode:bool = False
        # tile/palette/orientation
        self.__tile:int = 0
        self.__palette:int = 0
        self.__orientation:int = 0
        # container
        self.__container = _ttk.Frame(master = self)
        self.__container.pack()
        # head
        self.__head = _Head(master = self.__container)
        self.__head.pack(fill = 'x', pady = (0, _PAD_X))
        # view
        self.__view = _View(self.__tilesrc, master = self.__container)
        self.__view.mouse_changed.connect(self.__r_view_mouse_changed)
        self.__view.pack(fill = 'both', expand = True)
        # foot
        self.__foot = _Foot(master = self.__container)
        self.__foot.pack(fill = 'x')
        # help
        self.__help = _ttk.Label(\
            master = self.__container,\
            text = "Press F1 for help",\
            font = _qdg_helper.FONT_SMALL)
        self.__help.pack(fill = 'x')
        # Input
        self.bind('<Key>', self.__r_input_any)
        self.bind('<Button-1>', self.__r_input_draw)
        self.bind('<B1-Motion>', self.__r_input_draw)
        self.bind('<Button-3>', self.__r_input_pick)
        self.bind('<B3-Motion>', self.__r_input_pick)
        self.bind("<MouseWheel>", self.__r_input_scroll)
        self.bind("<Button-4>", self.__r_input_scroll_up)
        self.bind("<Button-5>", self.__r_input_scroll_down)
        self.bind('<F1>', self.__r_input_help)
        self.bind('<F2>', self.__r_input_switch)
        self.bind('<F3>', self.__r_input_palette)
        self.bind('<F4>', self.__r_input_orientation)
        self.bind('<F5>', self.__r_input_size)
        self.bind('<F6>', self.__r_input_tileset)
        self.bind('<Control-s>', self.__r_input_save)
        self.bind('<Left>', self.__r_input_left)
        self.bind('<Right>', self.__r_input_right)
        self.bind('<Up>', self.__r_input_up)
        self.bind('<Down>', self.__r_input_down)
        self.bind('<Home>', self.__r_input_home)
        self.bind('<End>', self.__r_input_end)
        self.bind('<BackSpace>', self.__r_input_backspace)
        # Post init
        self.__update_title()
        self.__update_view()
        # Success!!!
        self.__initializing = False

    #endregion

    #region receivers
    
    #region Window

    def __r_wm_delete_window(self):
        self.__quit()

    def __r_view_mouse_changed(self, emitter:_View, value:_qdg_helper.IXY):
        if not self.__textmode: self.__set_cursor(value)

    #endregion

    #region Controls

    def __r_input_any(self, event = None):
        if not isinstance(event, _tk.Event): return 
        # Is this text mode?
        if self.__textmode:
            # Make sure key is a character key
            if len(event.char) != 1: return
            char = ord(event.char)
            if char < 0x20 or char >= 0x7F: return
            # Plot tile
            self.__plot_tile(self.__view.cursor.x, self.__view.cursor.y, char)
            # Increment cursor
            self.__inc_cursor(1)

    def __r_input_draw(self, event = None):
        if not self.__textmode:
            self.__plot_tile(self.__view.cursor.x, self.__view.cursor.y, self.__tile)

    def __r_input_pick(self, event = None):
        if not self.__textmode:
            self.__set_tile(int(self.__content.cells[self.__view.cursor.x, self.__view.cursor.y]))

    def __r_input_scroll(self, event = None):
        if not isinstance(event, _tk.Event): return
        if event.delta > 0: self.__r_input_scroll_up(event = event)
        else: self.__r_input_scroll_down(event = event)

    def __r_input_scroll_up(self, event = None):
        if not isinstance(event, _tk.Event): return
        if not self.__textmode:
            shift = 8 if (event.state == 5) else (4 if (event.state == 4) else 0)
            self.__set_tile(self.__tile - (1 << shift))

    def __r_input_scroll_down(self, event = None):
        if not isinstance(event, _tk.Event): return 
        if not self.__textmode:
            shift = 8 if (event.state == 5) else (4 if (event.state == 4) else 0)
            self.__set_tile(self.__tile + (1 << shift))

    def __r_input_help(self, event = None):
        win = _tmap_help.Window(master = self)
        self.__movedialog(win)
        win.transient(self)
        win.grab_set()
        win.focus_set()
        win.wait_window()

    def __r_input_switch(self, event = None):
        self.__textmode = not self.__textmode
        self.__head.textmode = self.__textmode
        if not self.__textmode: self.__set_cursor(self.__view.mouse)

    def __r_input_palette(self, event = None):
        self.__set_palette(self.__palette + 1)

    def __r_input_orientation(self, event = None):
        self.__set_orientation(self.__orientation + 1)

    def __r_input_size(self, event = None):
        # Open Size window
        win = _tmap_size.Window(master = self, initsize = self.__content.cells.size)
        self.__movedialog(win)
        win.transient(self)
        win.grab_set()
        win.focus_set()
        win.wait_window()
        if win.result != _qdg_helper.WinDialogResult.OK: return
        # Resize
        match win.size:
            case _tmap_common.ContentSize.W256H256:
                _new_width = 32
                _new_height = 32
            case _tmap_common.ContentSize.W512H256:
                _new_width = 64
                _new_height = 32
            case _tmap_common.ContentSize.W256H512:
                _new_width = 32
                _new_height = 64
            case _tmap_common.ContentSize.W512H512:
                _new_width = 64
                _new_height = 64
            case _: # Should never happen
                _new_width = 0
                _new_height = 0
        match win.anchor:
            case _tmap_size.Anchor.TOPLEFT:
                _offset_x = 0
                _offset_y = 0
            case _tmap_size.Anchor.TOP:
                _offset_x = (_new_width - self.__content.cells.width) // 2
                _offset_y = 0
            case _tmap_size.Anchor.TOPRIGHT:
                _offset_x = _new_width - self.__content.cells.width
                _offset_y = 0
            case _tmap_size.Anchor.LEFT:
                _offset_x = 0
                _offset_y = (_new_height - self.__content.cells.height) // 2
            case _tmap_size.Anchor.CENTER:
                _offset_x = (_new_width - self.__content.cells.width) // 2
                _offset_y = (_new_height - self.__content.cells.height) // 2
            case _tmap_size.Anchor.RIGHT:
                _offset_x = _new_width - self.__content.cells.width
                _offset_y = (_new_height - self.__content.cells.height) // 2
            case _tmap_size.Anchor.BOTTOMLEFT:
                _offset_x = 0
                _offset_y = _new_height - self.__content.cells.height
            case _tmap_size.Anchor.BOTTOM:
                _offset_x = (_new_width - self.__content.cells.width) // 2
                _offset_y = _new_height - self.__content.cells.height
            case _tmap_size.Anchor.BOTTOMRIGHT:
                _offset_x = _new_width - self.__content.cells.width
                _offset_y = _new_height - self.__content.cells.height
            case _: # Should never happen
                _offset_x = 0
                _offset_y = 0
        self.__content.cells.resize(size = win.size, offset_x = _offset_x, offset_y = _offset_y)
        self.__update_view()
        # Mark dirty
        self.__set_dirty(True)

    def __r_input_tileset(self, event = None):
        # Open Size window
        win = _tmap_tileset.Window(\
            self.__tilesrc,\
            master = self,\
            init_final = _tmap_common.finaltile_to(self.__tile, self.__palette, self.__orientation))
        self.__movedialog(win)
        win.transient(self)
        win.grab_set()
        win.focus_set()
        win.wait_window()
        if win.result != _qdg_helper.WinDialogResult.OK: return
        # Set tile
        tile, palette, orientation = _tmap_common.finaltile_from(win.final)
        self.__set_tile(tile)
        self.__set_palette(palette)
        self.__set_orientation(orientation)

    def __r_input_save(self, event = None):
        # Save
        if not _qdg_helper.ErrorUtil.wrap(self.__content.save):
            return
        # Clear dirty
        self.__set_dirty(False)

    def __r_input_left(self, event = None):
        # Is this text mode?
        if self.__textmode:
            mod_ctrl = event is not None and (event.state & 0x0004) != 0
            mul = 8 if mod_ctrl else 1
            self.__inc_cursor(-mul)

    def __r_input_right(self, event = None):
        # Is this text mode?
        if self.__textmode:
            mod_ctrl = event is not None and (event.state & 0x0004) != 0
            mul = 8 if mod_ctrl else 1
            self.__inc_cursor(mul)

    def __r_input_up(self, event = None):
        # Is this text mode?
        if self.__textmode:
            mod_ctrl = event is not None and (event.state & 0x0004) != 0
            mul = 8 if mod_ctrl else 1
            self.__inc_cursor(-self.__content.cells.width * mul)

    def __r_input_down(self, event = None):
        # Is this text mode?
        if self.__textmode:
            mod_ctrl = event is not None and (event.state & 0x0004) != 0
            mul = 8 if mod_ctrl else 1
            self.__inc_cursor(self.__content.cells.width * mul)

    def __r_input_home(self, event = None):
        # Is this text mode?
        if self.__textmode:
            mod_ctrl = event is not None and (event.state & 0x0004) != 0
            x = 0
            y = 0 if mod_ctrl else self.__view.cursor.y
            self.__set_cursor(_qdg_helper.IXY(x = x, y = y))

    def __r_input_end(self, event = None):
        # Is this text mode?
        if self.__textmode:
            mod_ctrl = event is not None and (event.state & 0x0004) != 0
            x = self.__content.cells.width - 1
            y = (self.__content.cells.height - 1) if mod_ctrl else self.__view.cursor.y
            self.__set_cursor(_qdg_helper.IXY(x = x, y = y))

    def __r_input_backspace(self, event = None):
        # Is this text mode?
        if self.__textmode:
            self.__inc_cursor(-1)
            self.__plot_tile(self.__view.cursor.x, self.__view.cursor.y, 0x20)

    #endregion

    #endregion

    #region helper methods 1
    
    def __update_title(self):
        self.title(f"{("*" if self.__isdirty else "")} {self.__content.path.name} - tmap")

    def __update_view(self):
        self.__view.map.format(width = self.__content.cells.width, height = self.__content.cells.height)
        for _y in range(self.__content.cells.height):
            for _x in range(self.__content.cells.width):
                self.__view.map[_x, _y] = self.__content.cells[_x, _y]
        self.__foot.mapsize = _qdg_helper.IXY(x = self.__content.cells.width, y = self.__content.cells.height)

    def __quit(self):
        if self.__content is not None and self.__isdirty:
            _warn = _tk_messagebox.askyesnocancel(\
                "Unsaved Changes",\
                f"Save changes to {self.__content.path.name}?")
            if _warn is None: return
            if _warn: _qdg_helper.ErrorUtil.wrap(self.__content.save)
        self.destroy()

    def __set_dirty(self, value:bool):
        if self.__isdirty == value: return
        self.__isdirty = value
        self.__update_title()

    def __set_cursor(self, value:_qdg_helper.IXY):
        if self.__view.cursor == value: return
        self.__view.cursor = value
        self.__foot.cursor = self.__view.cursor

    def __set_tile(self, value:int):
        _WRAP = _tmap_common.TILESET_SUB_COLS * _tmap_common.TILESET_SUB_ROWS
        if self.__tile == value: return
        self.__tile = value % _WRAP
        self.__head.tile = self.__tile

    def __set_palette(self, value:int):
        self.__palette = value & 0b1111
        self.__head.palette = self.__palette
        
    def __set_orientation(self, value:int):
        self.__orientation = value & 0b11
        self.__head.orientation = self.__orientation

    def __inc_cursor(self, inc:int):
        pos = self.__view.cursor.x + self.__view.cursor.y * self.__content.cells.width
        pos = max(0, min(len(self.__content.cells) - 1, pos + inc))
        self.__set_cursor(_qdg_helper.IXY(x = pos % self.__content.cells.width, y = pos // self.__content.cells.width))

    def __plot_tile(self, x:int, y:int, tile:int):
        final = _tmap_common.finaltile_to(tile, self.__palette, self.__orientation)
        # Plot tile
        self.__content.cells[x, y] = final
        self.__view.map[x, y] = final
        # Mark dirty
        self.__set_dirty(True)

    def __movedialog(self, win:_tk.Toplevel):
        x = self.winfo_x() + 30
        y = self.winfo_y() + 30
        win.geometry(f"+{x}+{y}")

    #endregion

    #region helper methods 2

    def _raise_if_init(self):
        """ Accessed by _HEAD """
        if not self.__initializing: raise ValueError("Window has already been initialized")

    #endregion