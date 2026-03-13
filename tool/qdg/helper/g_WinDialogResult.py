from enum import\
    auto as _auto,\
    Enum as _Enum

class WinDialogResult(_Enum):
    """
    Represents a dialog result
    """

    NONE = _auto()
    """ No result given """

    YES = _auto()
    """ User answered Yes """

    NO = _auto()
    """ User answered No """

    OK = _auto()
    """ User confirmed """

    CANCEL = _auto()
    """ User cancelled """