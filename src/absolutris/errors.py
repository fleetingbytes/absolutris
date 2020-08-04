#!/usr/bin/env python

class Error(Exception):
    """
    Base class for Exceptions in this module.
    """
    pass


class TestError(Error):
    """
    Raised only for test purposes.
    """
    def __init__(self, message) -> None:
        self.message = message

