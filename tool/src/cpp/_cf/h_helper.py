all = []

from typing import\
    TypeVar as _TypeVar

T = _TypeVar('T')

def _tryfindtype(items:dict[type, T], t:type):
    if t in items: return True, items[t]
    for parent in t.__bases__:
        found, value = _tryfindtype(items, parent)
        if found: return True, value
    return False, None