import asyncio as _asyncio
import tkinter as _tk

from async_tkinter_loop import\
    async_handler as _async_handler
from tkinter import\
    ttk as _ttk
from typing import\
    Any as _Any

from .g_GUITaskState import GUITaskState as _GUITaskState

class GUITask:
    """
    Represents a GUI-related task to be executed asyncronously
    """

    #region init

    def __init__(self):
        """
        Initializer for GUITask
        """
        self.__state = _GUITaskState.INIT
    
    #endregion

    #region properties

    @property
    def state(self):
        """ Task state """
        return self.__state

    #endregion

    #region helper methods

    async def _start(self) -> _GUITaskState:
        """ Called by start() """
        raise NotImplementedError("_start has not yet been implemented.")

    #endregion

    #region methods

    async def start(self):
        """
        Begins executing the task
        """
        if self.__state != _GUITaskState.INIT: return
        self.__state = _GUITaskState.RUNNING
        result = await self._start()
        self.__state = result
        

    #endregion