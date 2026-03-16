__all__ = ['_ViewRefPnt']

from typing import\
    Callable as _Callable,\
    TYPE_CHECKING as _TYPE_CHECKING

if _TYPE_CHECKING:
    from .internal_View import _View

from .internal_ViewMap import *
import qdg.helper as _qdg_helper

class _ViewRefPnt:
    """
    Represents a point of reference
    """

    #region init

    def __init__(self, view:'_View',\
            x_min:_Callable[['_View'], int],\
            y_min:_Callable[['_View'], int],\
            x_max:_Callable[['_View'], int],\
            y_max:_Callable[['_View'], int],\
            redraw:_Callable[['_ViewRefPnt'], None]):
        """ Initializer for ViewRefPnt """
        view._raise_if_init()
        self.__view = view
        self.__redraw = redraw
        self.__x_min = x_min
        self.__y_min = y_min
        self.__x_max = x_max
        self.__y_max = y_max
        # Set fields
        self.__position = _qdg_helper.IXY_ZERO
        self.__visible = False
        # Post-init
        self.__redraw(self)

    #endregion

    #region properties

    @property
    def position(self):
        """ Cell position of point of reference"""
        return self.__position
    @position.setter
    def position(self, value:_qdg_helper.IXY):
        if self.__position == value: return
        self._update_position(value = value)

    @property
    def visible(self):
        """ Whether or not the reference is visible """
        return self.__visible
    @visible.setter
    def visible(self, value:bool):
        if self.__visible == value: return
        self.__visible = value
        self.__redraw(self)

    #endregion

    #region helper methods

    def _update_position(self, value:None|_qdg_helper.IXY = None):
        """ Also accessed by View """
        # Set position
        if value is not None: self.__position = value
        # Fix position
        self.__position = _qdg_helper.IXY(\
            x = max(self.__x_min(self.__view), min(self.__x_max(self.__view), self.__position.x)),\
            y = max(self.__y_min(self.__view), min(self.__y_max(self.__view), self.__position.y)))
        # Redraw
        self.__redraw(self)
    
    #endregion