from __future__ import annotations
from typing import TYPE_CHECKING

all = []

from typing import\
    Callable as _Callable

from ..data.mod_Text import\
    Text as _Text

if TYPE_CHECKING:
    from .mod__Creator import _Creator

#region CmdDef

type _CmdCall = _Callable[[_Creator, list[_Text]], None]

class _CmdDef:
    """
    Represents a command definition
    """

    #region init

    def __init__(self, call:_CmdCall, minargs:None|int = None):
        """
        Constructor for _CmdDef
        
        :param call:
            Callable
        :param minargs:
            If not none, this specifies the of arguments needed before the rest of the command line 
            is interpretted as a single argument.
        """
        self.__call = call
        self.__minargs = minargs

    #endregion

    #region properties

    @property
    def call(self):
        """
        Callable
        """
        return self.__call

    @property
    def minargs(self):
        """
        If not none, this specifies the of arguments needed before the rest of the command line 
        is interpretted as a single argument.
        """
        return self.__minargs

    #endregion

#endregion

#region FuncDef

type _FuncCall = _Callable[[_Creator, list[_Text]], _Text]

class _FuncDef:
    """
    Represents a function definition
    """

    #region init

    def __init__(self, call:_FuncCall):
        """
        Constructor for _FuncDef
        
        :param call:
            Callable
        """
        self.__call = call

    #endregion

    #region properties

    @property
    def call(self):
        """
        Callable
        """
        return self.__call

    #endregion

#endregion