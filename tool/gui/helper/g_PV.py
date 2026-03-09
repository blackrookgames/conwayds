import tkinter as _tk

from tkinter import\
    ttk as _ttk
from typing import\
    Any as _Any,\
    Callable as _Callable,\
    Generic as _Generic,\
    TypeVar as _TypeVar

TValue = _TypeVar('TValue', bound = _tk.Pack)

class PV(_Generic[TValue], _ttk.Frame):
    """
    Represents a pair of prompt/value widgets
    """

    #region nested

    type _Create = _Callable[[_tk.Misc, dict[str, _Any]], TValue]

    #endregion

    #region init

    def __init__(self,\
            create:_Create,\
            master:None|_tk.Misc,\
            kwargs:None|dict[str, _Any],\
            p_kwargs:None|dict[str, _Any],\
            p_pack:None|dict[str, _Any],\
            v_kwargs:None|dict[str, _Any],\
            v_pack:None|dict[str, _Any]):
        """
        Initializer for PV

        :param master:
            Master
        :param kwargs:
            Keyword arguments
        :param p_kwargs:
            Keyword arguments for prompt widget
        :param p_pack:
            Keyword arguments for packing prompt widget
        :param v_kwargs:
            Keyword arguments for value widget
        :param v_pack:
            Keyword arguments for packing value widget
        """
        if kwargs is None: kwargs = {}
        if p_kwargs is None: p_kwargs = {}
        if p_pack is None: p_pack = {}
        if v_kwargs is None: v_kwargs = {}
        if v_pack is None: v_pack = {}
        super().__init__(master = master, **kwargs)
        # Prompt
        self.__prompt = _ttk.Label(master = self, **p_kwargs)
        self.__prompt.pack(anchor = 'w', side = 'left', **p_pack)
        # Value
        self.__value = create(self, v_kwargs)
        self.__value.pack(anchor = 'w', side = 'left', fill = 'x', expand = True, **v_pack)

    #endregion

    #region properties

    @property
    def prompt(self):
        """
        Prompt widget
        """
        return self.__prompt

    @property
    def value(self):
        """
        Value widget
        """
        return self.__value

    #endregion