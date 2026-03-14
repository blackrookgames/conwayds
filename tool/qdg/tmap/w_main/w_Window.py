import tkinter as _tk
import tkinter.messagebox as _tk_messagebox

from PIL import\
    Image as _Image,\
    ImageTk as _ImageTk

from .internal_View import *
import qdg.helper as _qdg_helper
import qdg.tmap.w__common as _tmap_common
import qdg.tmap.w_help as _tmap_help

PAD_X = 4
PAD_Y = 4
TILE_W = 8
TILE_H = 8

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
        # Error check
        if tilesrc.size[0] < _VIEW_TILESRC_WIDTH:
            raise ValueError(f"Tileset width must be greater than or equal to {_VIEW_TILESRC_WIDTH}.")
        if tilesrc.size[1] < _VIEW_TILESRC_HEIGHT:
            raise ValueError(f"Tileset height must be greater than or equal to {_VIEW_TILESRC_HEIGHT}.")
        # Initialize
        super().__init__(*args, **kwargs)
        self.resizable(width = False, height = False)
        self.config(padx = PAD_X, pady = PAD_Y)
        self.protocol("WM_DELETE_WINDOW", self.__r_wm_delete_window)
        # content
        self.__content = content
        # isdirty
        self.__isdirty:bool = False
        # view
        self.__view = _View(tilesrc,\
            map_width = self.__content.cells.width,\
            map_height = self.__content.cells.height,\
            master = self)
        self.__view.pack(fill = 'both', expand = True)
        # Input
        self.bind('<F1>', self.__r_input_help)
        self.bind('<Control-s>', self.__r_input_save)
        self.bind('<Left>', self.__r_input_left)
        self.bind('<Right>', self.__r_input_right)
        self.bind('<Up>', self.__r_input_up)
        self.bind('<Down>', self.__r_input_down)
        # Post init
        self.__update_title()
        self.__update_size()

    #endregion

    #region receivers
    
    #region Window

    def __r_wm_delete_window(self): self.__quit()

    #endregion

    #region Controls

    def __r_input_help(self, event = None):
        win = _tmap_help.Window(master = self)
        win.transient(self)
        win.grab_set()
        win.wait_window()

    def __r_input_save(self, event = None):
        # Save
        if not _qdg_helper.ErrorUtil.wrap(self.__content.save):
            return
        # Clear dirty
        self.__isdirty = False
        # Update title
        self.__update_title()

    def __r_input_left(self, event = None):
        pass

    def __r_input_right(self, event = None):
        pass

    def __r_input_up(self, event = None):
        pass

    def __r_input_down(self, event = None):
        pass

    #endregion

    #endregion

    #region helper methods
    
    def __update_title(self):
        self.title(f"{("*" if self.__isdirty else "")} {self.__content.path.name} - tmap")

    def __update_size(self):
        w = self.__content.cells.width * TILE_W + PAD_X * 2
        h = self.__content.cells.height * TILE_H + PAD_Y * 2
        self.geometry(f"{w}x{h}")

    def __quit(self):
        if self.__content is not None and self.__isdirty:
            _warn = _tk_messagebox.askyesnocancel(\
                "Unsaved Changes",\
                f"Save changes to {self.__content.path.name}?")
            if _warn is None: return
            if _warn:
                # TODO: Save
                pass
        self.destroy()

    #endregion