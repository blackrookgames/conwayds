import tkinter as _tk

from typing import\
    Any as _Any

from .g_WinDialogResult import WinDialogResult as _WinDialogResult

class WinDialog(_tk.Toplevel):
    """
    Represents a window for dialog
    """

    #region init

    def __init__(self,\
            initresult = _WinDialogResult.NONE,\
            *args:_Any, **kwargs:_Any):
        """
        Initializer for WinDialog

        :param initresult: Initial result
        """
        super().__init__(*args, **kwargs)
        self.__result = initresult
    
    #endregion

    #region properties

    @property
    def result(self):
        """ Dialog result """
        return self.__result

    #endregion

    #region helper methods

    def _set_result(self, value:_WinDialogResult):
        self.__result = value

    #endregion