from typing import Callable as _Callable
from .c__HCmdLoad import _HCmdLoad
from .c_load_imgimage import _create as _create_imgimage
# Sub-commands
__DICT:dict[str, _Callable[[], _HCmdLoad]] = {
    'imgimage': _create_imgimage,
}
