import tkinter as _tk
import tkinter.messagebox as _tk_messagebox

from PIL import\
    Image as _Image,\
    ImageTk as _ImageTk

from .internal_View import *
import qdg.tmap.w__common as _tmap_common

_PAD_X = 4
_PAD_Y = 4

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
        self.geometry(f"{(256 + _PAD_X * 2)}x{(256 + _PAD_Y * 2)}")
        self.resizable(width = False, height = False)
        self.config(padx = _PAD_X, pady = _PAD_Y)
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
        # Post init
        self.__update_title()

    #endregion

    #region receivers
    
    #region window

    def __r_wm_delete_window(self): self.__quit()

    #endregion

    #region Menu

    #endregion

    #endregion

    #region helper methods
    
    def __update_title(self):
        self.title(f"{("*" if self.__isdirty else "")} {self.__content.path.name} - tmap")

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