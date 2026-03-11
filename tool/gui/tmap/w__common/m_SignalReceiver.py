__all__ = ['SignalReceiver']

from typing import \
    Callable as _Callable,\
    TypeVar as _TypeVar

TEmitter = _TypeVar('TEmitter')
TArgs = _TypeVar('TArgs')

type SignalReceiver[TEmitter, TArgs] = _Callable[[TEmitter, TArgs], None]