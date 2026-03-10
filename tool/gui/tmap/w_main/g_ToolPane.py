import tkinter as _tk

from tkinter import\
    ttk as _ttk
from typing import\
    Any as _Any

class ToolPane(_ttk.Frame):
    """
    Represents a tool pane
    """

    #region init

    def __init__(self,\
            master:None|_tk.Misc,\
            **kwargs:_Any):
        """
        Initializer for ToolPane
        """
        super().__init__(master = master, **kwargs)
        self.pack_propagate(False)
        # Draw
        self.__widget_draw = _ttk.Button(\
            master = self,\
            command = self.__r_widget_draw,\
            text = "Draw")
        self.__widget_draw.configure(\
            state = _tk.DISABLED)
        self.__widget_draw.pack(fill = 'x')
        # Fill
        self.__widget_fill = _ttk.Button(\
            master = self,\
            command = self.__r_widget_fill,\
            text = "Fill")
        self.__widget_fill.configure(\
            state = _tk.DISABLED)
        self.__widget_fill.pack(fill = 'x')
        # Text
        self.__widget_text = _ttk.Button(\
            master = self,\
            command = self.__r_widget_text,\
            text = "Text")
        self.__widget_text.configure(\
            state = _tk.DISABLED)
        self.__widget_text.pack(fill = 'x')
        # Clear
        self.__widget_clear = _ttk.Button(\
            master = self,\
            command = self.__r_widget_clear,\
            text = "Clear")
        self.__widget_clear.configure(\
            state = _tk.DISABLED)
        self.__widget_clear.pack(fill = 'x')
    
    #endregion

    #region receivers

    def __r_widget_draw(self):
        print("Draw")
        
    def __r_widget_fill(self):
        print("Fill")
        
    def __r_widget_text(self):
        print("Text")
        
    def __r_widget_clear(self):
        print("Clear")

    #endregion