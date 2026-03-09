import tkinter as _tk
import tkinter.messagebox as _tk_messagebox

from async_tkinter_loop import\
    async_handler as _async_handler
from tkinter import\
    ttk as _ttk

from .w_WinNew import\
    WinNew as _WinNew
from .w_WinSize import\
    WinSize as _WinSize
from .w_WinTileset import\
    WinTileset as _WinTileset
from .w_WinTranslate import\
    WinTranslate as _WinTranslate

class WinMain(_tk.Tk):
    """
    Represents a main window
    """

    #region init

    def __init__(self, *args, **kwargs):
        """
        Initializer for WinMain
        """
        super().__init__(*args, **kwargs)
        # Window Properties
        self.title("tmap")
        self.geometry("800x600")
        self.minsize(width = 650, height = 350)
        #region style
        self.__style = _ttk.Style()
        self.__style.configure('My.TFrame', background='#808080')
        #endregion
        #region Menu
        self.__widget_m = _tk.Menu(self)
        self.config(menu = self.__widget_m)
        # File
        self.__widget_mf = _tk.Menu(self.__widget_m, tearoff = 0)
        self.__widget_mf.add_command(label = "New", command = self.__r_widget_mf_new)
        self.__widget_mf.add_command(label = "Open", command = self.__r_widget_mf_open)
        self.__widget_mf.add_command(label = "Save", command = self.__r_widget_mf_save)
        self.__widget_mf.add_command(label = "Save As", command = self.__r_widget_mf_saveas)
        self.__widget_mf.add_command(label = "Exit", command = self.__r_widget_mf_exit)
        self.__widget_m.add_cascade(label = "File", menu = self.__widget_mf)
        # Map
        self.__widget_mm = _tk.Menu(self.__widget_m, tearoff = 0)
        self.__widget_mm.add_command(label = "Tileset", command = self.__r_widget_mm_tileset)
        self.__widget_mm.add_command(label = "Size", command = self.__r_widget_mm_size)
        self.__widget_m.add_cascade(label = "Map", menu = self.__widget_mm)
        # Transform
        self.__widget_mt = _tk.Menu(self.__widget_m, tearoff = 0)
        self.__widget_mt.add_command(label = "Translate", command = self.__r_widget_mt_translate)
        self.__widget_m.add_cascade(label = "Modify", menu = self.__widget_mt)
        #endregion
        #region Main Frame
        self.__widget_f = _ttk.Frame(self, padding = 5)
        self.__widget_f.columnconfigure(1, weight = 1)
        self.__widget_f.rowconfigure(0, weight = 1)
        self.__widget_f.pack(fill = 'both', expand = True)
        #region Tool Pane
        self.__widget_ft = _ttk.Frame(\
            self.__widget_f,\
            width = 60,\
            padding = (0, 0, 5, 0))
        self.__widget_ft.pack_propagate(False)
        self.__widget_ft.grid(column = 0, row = 0, sticky = 'ns')
        # Draw
        self.__widget_ft_draw = _ttk.Button(\
            master = self.__widget_ft,\
            command = self.__r_widget_ft_draw,\
            text = "Draw")
        self.__widget_ft_draw.pack(fill = 'x')
        # Fill
        self.__widget_ft_fill = _ttk.Button(\
            master = self.__widget_ft,\
            command = self.__r_widget_ft_fill,\
            text = "Fill")
        self.__widget_ft_fill.pack(fill = 'x')
        # Text
        self.__widget_ft_text = _ttk.Button(\
            master = self.__widget_ft,\
            command = self.__r_widget_ft_text,\
            text = "Text")
        self.__widget_ft_text.pack(fill = 'x')
        # Clear
        self.__widget_ft_clear = _ttk.Button(\
            master = self.__widget_ft,\
            command = self.__r_widget_ft_clear,\
            text = "Clear")
        self.__widget_ft_clear.pack(fill = 'x')
        #endregion
        #region Canvas
        self.__widget_fc = _ttk.Frame(\
            self.__widget_f,\
            style = 'My.TFrame')
        self.__widget_fc.pack_propagate(False)
        self.__widget_fc.grid(column = 1, row = 0, sticky = 'nsew')
        # Canvas
        self.__widget_fc_canvas = _tk.Canvas(\
            self.__widget_fc,\
            width = 512,\
            height = 512,\
            bg = 'red',\
            highlightthickness = 0)
        self.__widget_fc_canvas.pack(anchor = 'nw')
        #endregion
        #region Tileset
        self.__widget_fs = _ttk.Frame(\
            self.__widget_f,\
            width = 270,\
            padding = (5, 0, 0, 0))
        self.__widget_fs.columnconfigure(3, weight = 1)
        self.__widget_fs.rowconfigure(1, pad = 10)
        self.__widget_fs.rowconfigure(2, weight = 1)
        self.__widget_fs.grid(column = 2, row = 0, sticky = 'ns')
        # Sub-palette
        self.__widget_fs_sub_var = _tk.StringVar()
        self.__widget_fs_sub = _ttk.Combobox(\
            self.__widget_fs,\
            textvariable = self.__widget_fs_sub_var,\
            values = [f"Sub-Pallete {_i:01X}" for _i in range(16)],\
            state = 'readonly',\
            width = 12)
        self.__widget_fs_sub.bind("<<ComboboxSelected>>", self.__r_widget_fs_sub_selected)
        self.__widget_fs_sub.set("Sub-Pallete 0")
        self.__widget_fs_sub.grid(column = 0, row = 0)
        # Flip X
        self.__widget_fs_flipx_var = _tk.BooleanVar(value=False)
        self.__widget_fs_flipx = _ttk.Checkbutton(\
            self.__widget_fs,\
            text = "Flip X",\
            variable = self.__widget_fs_flipx_var,\
            command = self.__r_widget_fs_flipx,\
            padding = (5, 0, 0, 0))
        self.__widget_fs_flipx.grid(column = 1, row = 0)
        # Flip Y
        self.__widget_fs_flipy_var = _tk.BooleanVar(value=False)
        self.__widget_fs_flipy = _ttk.Checkbutton(\
            self.__widget_fs,\
            text = "Flip Y",\
            variable = self.__widget_fs_flipy_var,\
            command = self.__r_widget_fs_flipy,\
            padding = (5, 0, 0, 0))
        self.__widget_fs_flipy.grid(column = 2, row = 0)
        # Tiles
        self.__widget_fs_tiles = _tk.Canvas(\
            self.__widget_fs,\
            width = 256,\
            height = 256,\
            bg = 'blue',\
            highlightthickness = 0)
        self.__widget_fs_tiles.config()
        self.__widget_fs_tiles.grid(column = 0, row = 1, columnspan = 4)
        #endregion
        #endregion
        #region Status
        self.__widget_s = _ttk.Frame(self, height = 10)
        self.__widget_s.pack(fill = 'x', anchor = 's')
        # Position
        self.__widget_sp = _ttk.Label(self.__widget_s, text = "X, Y", width = 10)
        self.__widget_sp.grid(column = 0, row = 0)
        # Size
        self.__widget_ss = _ttk.Label(self.__widget_s, text = "W, H", width = 10)
        self.__widget_ss.grid(column = 1, row = 0)
        #endregion

    #endregion

    #region receivers

    #region Menu

    def __r_widget_mf_new(self):
        dialog = _WinNew(self)
        dialog.transient(self)
        dialog.grab_set()
        dialog.wait_window()

    def __r_widget_mf_open(self):
        print("Open")

    def __r_widget_mf_save(self):
        print("Save")

    def __r_widget_mf_saveas(self):
        print("Save As")

    def __r_widget_mf_exit(self):
        print("Exit")

    def __r_widget_mm_tileset(self):
        dialog = _WinTileset(self)
        dialog.transient(self)
        dialog.grab_set()
        dialog.wait_window()

    def __r_widget_mm_size(self):
        dialog = _WinSize(self)
        dialog.transient(self)
        dialog.grab_set()
        dialog.wait_window()

    def __r_widget_mt_translate(self):
        dialog = _WinTranslate(self)
        dialog.transient(self)
        dialog.grab_set()
        dialog.wait_window()

    #endregion

    #region Tools

    def __r_widget_ft_draw(self):
        print("Draw")
        
    def __r_widget_ft_fill(self):
        print("Fill")
        
    def __r_widget_ft_text(self):
        print("Text")
        
    def __r_widget_ft_clear(self):
        print("Clear")

    #endregion

    #region Tileset

    def __r_widget_fs_sub_selected(self, event):
        selected_item = self.__widget_fs_sub.get()
        print(f"Selected: {selected_item}")

    def __r_widget_fs_flipx(self):
        print(self.__widget_fs_flipx_var.get())

    def __r_widget_fs_flipy(self):
        print(self.__widget_fs_flipy_var.get())

    #endregion

    #endregion