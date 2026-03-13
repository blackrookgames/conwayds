__all__ = ['SignalHandler']

from typing import \
    Generic as _Generic,\
    TypeVar as _TypeVar

from .m_SignalReceiver import SignalReceiver as _SignalReceiver

TEmitter = _TypeVar('TEmitter')
TArgs = _TypeVar('TArgs')

class SignalHandler(_Generic[TEmitter, TArgs]):
    """
    Represents a signal handler
    """

    #region init

    def __init__(self):
        """
        Initializer for SignalHandler
        """
        self.__receivers:set[_SignalReceiver[TEmitter, TArgs]] = set()

    #endregion

    #region helper methods

    def _connect(self, receiver:_SignalReceiver[TEmitter, TArgs]):
        """
        Also accessed by Signal
        """
        if not (receiver in self.__receivers): self.__receivers.add(receiver)

    def _disconnect(self, receiver:_SignalReceiver[TEmitter, TArgs]):
        """
        Also accessed by Signal
        """
        if receiver in self.__receivers: self.__receivers.remove(receiver)

    #endregion

    #region methods

    def emit(self, emitter:TEmitter, args:TArgs):
        """
        Emits the signal

        :param emitter:
            Object that's emitting the signal
        :param args:
            Signal arguments
        """
        for _receiver in self.__receivers: _receiver(emitter, args)

    #endregion