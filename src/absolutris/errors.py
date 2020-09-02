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


class PlanNotImplemented(Error):
    """
    Raised when trying to load a game plan which is not instantiated in plans.py.
    """
    pass


class RandomSourceDepleted(Error):
    """
    Raised when a generator is not capable of generating any more random numbers.
    """
    def __init__(self, file_name: str, bits_used: int):
        self.file_name = file_name
        self.bits_used = bits_used
        self.message = f"Used all random numbers in {self.file_name}"


class MissedLevel(Error):
    """
    Raised when it is no longer possible to start a level.
    Used for "secret" levels.
    """
    pass


class EndGame(Error):
    """
    Raised when game must end, e.g. when the random source is depleted.
    """
    pass
