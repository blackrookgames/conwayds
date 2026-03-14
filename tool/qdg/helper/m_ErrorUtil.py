__all__ = ['ErrorUtil']

import tkinter.messagebox as _tk_msg

from typing import\
    Callable as _Callable

import src.cliutil as _cliutil
import src.helper as _helper

class ErrorUtil:
    """ Utility for error-related operations """
    
    #region wrap

    @classmethod
    def wrap(cls, func:_Callable, result:None|_helper.Ptr = None,  *args, **kwargs):
        """
        Calls the function, but if CLICommandError is raised, it is caught and displayed as an error message

        :param func: Function to call
        :param result: Where to store return value of function
        :return: True if no errors occurred; otherwise False
        """
        try:
            retvalue = func(*args, **kwargs)
            if result is not None: result.value = retvalue
            return True
        except _cliutil.CLICommandError as _e:
            _tk_msg.showerror(\
                title = "Error",\
                message = str(_e),\
                icon = 'error')
            return False

    #endregion