from enum import\
    auto as _auto,\
    Enum as _Enum

class GUITaskState(_Enum):
    """
    Represents the state of a GUI-related task
    """

    INIT = _auto()
    """ Task has been initialized but has not been executed """

    RUNNING = _auto()
    """ Task is currently executing """

    FINISH = _auto()
    """ Task completed successfully """

    ERROR = _auto()
    """ An error occurred while executing the task """

    CANCEL = _auto()
    """ Task was cancelled """