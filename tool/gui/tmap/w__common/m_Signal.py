__all__ = ['Signal']

from typing import \
    Generic as _Generic,\
    TypeVar as _TypeVar

from .m_SignalHandler import SignalHandler as _SignalHandler
from .m_SignalReceiver import SignalReceiver as _SignalReceiver

TEmitter = _TypeVar('TEmitter')
TArgs = _TypeVar('TArgs')

class Signal(_Generic[TEmitter, TArgs]):
    """
    Represents a signal
    """

    #region init

    def __init__(self, handler:_SignalHandler[TEmitter, TArgs]):
        """
        Initializer for Signal

        :param handler:
            Signal handler
        """
        self.__handler = handler

    #endregion

    #region methods

    def connect(self, receiver:_SignalReceiver[TEmitter, TArgs]):
        """
        Connects a receiver to the signal

        :param receiver:
            Receiver to connect
        """
        self.__handler._connect(receiver)

    def disconnect(self, receiver:_SignalReceiver[TEmitter, TArgs]):
        """
        Disconnects a receiver from the signal

        :param receiver:
            Receiver to disconnect
        """
        self.__handler._disconnect(receiver)

    #endregion