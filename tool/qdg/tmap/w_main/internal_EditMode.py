__all__ = ['_EditMode']

from enum import \
    auto as _auto,\
    Enum as _Enum

class _EditMode(_Enum):
    """
    Represents an edit mode
    """

    DRAW = 0
    """ Draw mode """

    TEXT = _auto()
    """ Text mode """

    SELECT = _auto()
    """ Select mode """