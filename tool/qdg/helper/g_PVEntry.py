import tkinter as _tk

from tkinter import\
    ttk as _ttk
from typing import\
    Any as _Any

from .g_PV import\
    PV as _PV

class PVEntry(_PV[_ttk.Entry]):
    """
    Represents a prompt/combobox pair
    """

    #region init

    def __init__(self,\
            master:None|_tk.Misc = None,\
            kwargs:None|dict[str, _Any] = None,\
            p_kwargs:None|dict[str, _Any] = None,\
            p_pack:None|dict[str, _Any] = None,\
            v_kwargs:None|dict[str, _Any] = None,\
            v_pack:None|dict[str, _Any] = None):
        """
        Initializer for PVEntry

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
        super().__init__(\
            lambda _master, _kwargs: _ttk.Entry(master = _master, **_kwargs),\
            master, kwargs, p_kwargs, p_pack, v_kwargs, v_pack)

    #endregion