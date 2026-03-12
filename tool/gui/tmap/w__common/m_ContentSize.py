from enum import\
    auto as _auto,\
    Enum as _Enum

class ContentSize(_Enum):
    """
    Represents a tilemap size
    """

    W256H256 = _auto()
    """ 256x256 pixels """

    W512H256 = _auto()
    """ 512x256 pixels """

    W256H512 = _auto()
    """ 256x512 pixels """

    W512H512 = _auto()
    """ 512x512 pixels """