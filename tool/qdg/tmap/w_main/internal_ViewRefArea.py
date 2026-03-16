__all__ = ['_ViewRefArea']

from typing import\
    Callable as _Callable,\
    TYPE_CHECKING as _TYPE_CHECKING

if _TYPE_CHECKING:
    from .internal_View import _View

from .internal_ViewMap import *
import qdg.helper as _qdg_helper

class _ViewRefArea:
    """
    Represents an area of reference
    """

    #region init

    def __init__(self, view:'_View',\
            x_min:_Callable[['_View'], int],\
            y_min:_Callable[['_View'], int],\
            x_max:_Callable[['_View'], int],\
            y_max:_Callable[['_View'], int],\
            redraw:_Callable[['_ViewRefArea'], None]):
        """ Initializer for ViewRefArea """
        view._raise_if_init()
        self.__view = view
        self.__redraw = redraw
        self.__x_min = x_min
        self.__y_min = y_min
        self.__x_max = x_max
        self.__y_max = y_max
        # Set fields
        self.__pnt0 = _qdg_helper.IXY_ZERO
        self.__pnt1 = _qdg_helper.IXY_ZERO
        self.__visible = False
        # Post-init
        self.__redraw(self)

    #endregion

    #region properties

    @property
    def pnt0(self):
        """ Point of reference 0 """
        return self.__pnt0
    @pnt0.setter
    def pnt0(self, value:_qdg_helper.IXY):
        if self.__pnt0 == value: return
        self.__pnt0 = self.__clamp_point(value)
        self.__redraw(self)

    @property
    def pnt1(self):
        """ Point of reference 1 """
        return self.__pnt1
    @pnt1.setter
    def pnt1(self, value:_qdg_helper.IXY):
        if self.__pnt1 == value: return
        self.__pnt1 = self.__clamp_point(value)
        self.__redraw(self)

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

    def __clamp_point(self, value:_qdg_helper.IXY):
        return _qdg_helper.IXY(\
            x = max(self.__x_min(self.__view), min(self.__x_max(self.__view), value.x)),\
            y = max(self.__y_min(self.__view), min(self.__y_max(self.__view), value.y)))

    def _update_pnts(self):
        """ Also accessed by View """
        self.__pnt0 = self.__clamp_point(self.__pnt0)
        self.__pnt1 = self.__clamp_point(self.__pnt1)
        self.__redraw(self)
    
    #endregion