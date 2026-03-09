import tkinter as _tk

from tkinter import\
    ttk as _ttk
from typing import\
    Any as _Any

import src.helper as _helper

class ButtonRow(_ttk.Frame):
    """
    Represents a row of buttons
    """

    #region init

    def __init__(self,\
            master:None|_tk.Misc = None,\
            kwargs:None|dict[str, _Any] = None,\
            buttons:None|list[dict[str, _Any]] = None,\
            pack:None|dict[str, _Any] = None):
        """
        Initializer for ButtonRow

        :param master:
            Master
        :param kwargs:
            Keyword arguments
        :param buttons:
            Keyword arguments for each button to add
        :param pack:
            Keyword arguments for packing buttons
        """
        if kwargs is None: kwargs = {}
        if pack is None: pack = {}
        super().__init__(master = master, **kwargs)
        # Buttons
        self.__buttons_list:list[_ttk.Button] = []
        self.__buttons = _helper.LockedList[_ttk.Button](self.__buttons_list)
        if buttons is not None:
            for _kwargs in buttons:
                _button = _ttk.Button(master = self, **_kwargs)
                _button.pack(anchor = 'w', side = 'left', **pack)

    #endregion

    #region properties

    @property
    def buttons(self):
        """
        Buttons
        """
        return self.__buttons

    #endregion