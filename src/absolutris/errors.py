#!/usr/bin/env python

class Error(Exception):
    """
    Base class for Exceptions in this module.
    """
    def __init__(self, message) -> None:
        self.message = message


class TestError(Error):
    """
    Raised only for test purposes.
    """
    pass


class UnsignedIntegerOverflow(Error):
    """
    Raised when trying to convert an python int to an unsigned integer of a limited bit length and this integer is too big.
    """
    pass


class UnsignedIntegerBitLength(Error):
    """
    Raised when trying to convert an integer to a bitlength < 1.
    """
    pass


class GuiNotImplemented(Error):
    """
    Raised when trying to load a gui which is not instantiated in gui.py.
    """
    pass
