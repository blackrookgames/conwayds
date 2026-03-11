__all__ = ['FramePath']

import tkinter as _tk

from collections.abc import\
    Iterable as _Iterable
from idlelib.tooltip import\
    Hovertip
from pathlib import\
    Path as _Path
from tkinter import\
    filedialog as _filedialog,\
    ttk as _ttk
from typing import\
    Any as _Any

from .m_Signal import Signal as _Signal
from .m_SignalHandler import SignalHandler as _SignalHandler

class FramePath(_ttk.Frame):
    """
    Represents a frame for configuring a path
    """

    #region nested

    type FileTypes = _Iterable[tuple[str, str | list[str] | tuple[str, ...]]]

    #endregion

    #region init

    def __init__(self,\
            master:None|_tk.Misc = None,\
            **kwargs:_Any):
        """
        Initializer for FramePath
        """
        super().__init__(master = master, **kwargs)
        # Fields
        self.__enabled = True
        self.__abspath:None|_Path = None
        self.__path:None|str = None
        self.__isrel:bool = False
        self.__dialog_title:None|str = None
        self.__dialog_filetypes:None|FramePath.FileTypes = None
        self.__dialog_defaultextension:None|str = None
        # Signals
        self.__path_changed_h = _SignalHandler[FramePath, None|str]()
        self.__path_changed = _Signal(self.__path_changed_h)
        self.__isrel_changed_h = _SignalHandler[FramePath, bool]()
        self.__isrel_changed = _Signal(self.__isrel_changed_h)
        self.__enabled_changed_h = _SignalHandler[FramePath, bool]()
        self.__enabled_changed = _Signal(self.__enabled_changed_h)
        # Browse
        self.__widget_browse = _ttk.Button(\
            master = self,\
            command = self.__r_widget_browse,\
            text = "Browse")
        self.__widget_browse.pack(anchor = 'e', side = 'right')
        # Relative
        self.__widget_rel_var = _tk.BooleanVar(value = self.__isrel)
        self.__widget_rel = _ttk.Checkbutton(\
            master = self,\
            variable = self.__widget_rel_var,\
            command = self.__r_widget_rel,\
            text = "Rel")
        self.__widget_rel.configure(\
            state = _tk.DISABLED)
        self.__widget_rel.pack(anchor = 'e', side = 'right')
        # Display
        self.__widget_display = _ttk.Label(\
            master = self)
        self.__widget_display_tip = Hovertip(self.__widget_display, "")
        self.__widget_display.pack(anchor = 'e', side = 'right', fill = 'x', expand = True)
    
    #endregion

    #region properties

    @property
    def enabled(self):
        """ Whether or not the path selector is enabled"""
        return self.__enabled
    @enabled.setter
    def enabled(self, value:bool):
        if self.__enabled == value: return
        self.__enabled = value
        # Update GUI
        guistate = _tk.NORMAL if self.__enabled else _tk.DISABLED
        self.__widget_display.configure(state = guistate)
        self.__widget_browse.configure(state = guistate)
        self.__update_widget_isrel_state()
        # Emit signal
        self.__enabled_changed_h.emit(self, self.__enabled)

    @property
    def path(self):
        """ Path """
        return self.__path
    @path.setter
    def path(self, value:None|str|_Path):
        if value is not None:
            abspath = (value if isinstance(value, _Path) else _Path(value)).resolve()
            if self.__abspath == abspath: return
            # Set path
            self.__abspath = abspath
            self.__update_path()
            # Emit signal
            self.__path_changed_h.emit(self, self.__path)
        elif self.__path is not None:
            # Set path
            self.__abspath = None
            self.__update_path()
            # Emit signal
            self.__path_changed_h.emit(self, self.__path)

    @property
    def isrel(self):
        """ Whether or not the is relative """
        return self.__isrel
    @isrel.setter
    def isrel(self, value:bool):
        if self.__isrel == value: return
        # Set isrel
        self.__isrel = value
        self.__update_path()
        # Update GUI
        self.__widget_rel_var.set(self.__isrel)
        # Emit signal
        self.__isrel_changed_h.emit(self, self.__isrel)
    
    @property
    def dialog_title(self):
        """ Title of file dialog """
        return self.__dialog_title
    @dialog_title.setter
    def dialog_title(self, value:None|str):
        self.__dialog_title = value
    
    @property
    def dialog_defaultextension(self):
        """ Default extension to use for file dialog """
        return self.__dialog_defaultextension
    @dialog_defaultextension.setter
    def dialog_defaultextension(self, value:None|str):
        self.__dialog_defaultextension = value
    
    @property
    def dialog_filetypes(self):
        """ File type options provided by file dialog """
        return self.__dialog_filetypes
    @dialog_filetypes.setter
    def dialog_filetypes(self, value:None|FileTypes):
        self.__dialog_filetypes = value

    #endregion

    #region signals

    @property
    def path_changed(self):
        """
        Emitted when the path is changed\n
        NOTE: This is not emitted when the path is changed from absolute to relative (or vice versa). 
        For that use isrel_changed
        """
        return self.__path_changed

    @property
    def isrel_changed(self):
        """
        Emitted when the path is changed from absolute to relative (or vice versa).
        """
        return self.__isrel_changed

    @property
    def enabled_changed(self):
        """
        Emitted when the path selector is enabled or disabled
        """
        return self.__enabled_changed

    #endregion

    #region receivers

    def __r_widget_rel(self):
        self.isrel = self.__widget_rel_var.get() # Use the property; NOT the variable

    def __r_widget_browse(self):
        def _dirandfile():
            nonlocal self
            if self.__abspath is not None:
                try: return str(self.__abspath.parent), self.__abspath.name
                except: pass
            return str(_Path.cwd()), ""
        # Open file dialog
        kwargs:dict[str, _Any] = {}
        if self.__dialog_title is not None:
            kwargs['title'] = self.__dialog_title
        if self.__dialog_filetypes is not None:
            kwargs['filetypes'] = self.__dialog_filetypes
        if self.__dialog_defaultextension is not None:
            kwargs['defaultextension'] = self.__dialog_defaultextension
        initialdir, initialfile = _dirandfile()
        file_path = _filedialog.askopenfilename(\
            initialdir = initialdir,\
            initialfile = initialfile,\
            **kwargs)
        # Update path
        if file_path: self.path = file_path # Use the property; NOT the variable

    #endregion

    #region helper methods

    def __update_path(self):
        # Update value
        if self.__abspath is not None:
            if self.__isrel:
                try: path = self.__abspath.relative_to(_Path.cwd(), walk_up = True)
                except: path = self.__abspath
            else: path = self.__abspath
            self.__path = str(path)
        else: self.__path = None
        # Update display
        displaytext = "" if (self.__path is None) else self.__path
        self.__widget_display.configure(text = displaytext)
        self.__widget_display_tip.text = displaytext
        # Update relative checkbox
        self.__update_widget_isrel_state()
    
    def __update_widget_isrel_state(self):
        if self.__enabled:
            if self.__path is not None: self.__widget_rel.configure(state = _tk.NORMAL)
            else: self.__widget_rel.configure(state = _tk.DISABLED)
        else: self.__widget_rel.configure(state = _tk.DISABLED)

    #endregion