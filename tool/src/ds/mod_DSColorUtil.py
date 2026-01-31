__all__ = [\
    'DSColorUtil',]

from .mod_DSColor import\
    DSColor as _DSColor,\
    DSCOLOR_MAX as _DSCOLOR_MAX
from ..img.mod_ImgColor import\
    ImgColor as _ImgColor

class DSColorUtil:
    """
    Utility for DSColor
    """

    #region imgcolor

    @classmethod
    def from_imgcolor(cls, color:_ImgColor):
        """
        Creates a DSColor from an ImgColor
        
        :param color:
            Input ImgColor
        :return:
            Created DSColor
        """
        _CONVERT = float(_DSCOLOR_MAX) / 255.0
        return _DSColor((\
            int(round(float(color.r) * _CONVERT)),\
            int(round(float(color.g) * _CONVERT)),\
            int(round(float(color.b) * _CONVERT)), \
            color.a >= 128, ))

    @classmethod
    def to_imgcolor(cls, color:_DSColor):
        """
        Creates an ImgColor from a DSColor
        
        :param color:
            Input DSColor
        :return:
            Created ImgColor
        """
        _CONVERT =  255.0 / float(_DSCOLOR_MAX)
        return _ImgColor(\
            r = int(round(float(color.r) * _CONVERT)),\
            g = int(round(float(color.g) * _CONVERT)),\
            b = int(round(float(color.b) * _CONVERT)), \
            a = 255 if color.a else 0, )
    
    #endregion