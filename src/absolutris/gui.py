#!/usr/bin/env python

import logging
import pygame


# setup logging
logger = logging.getLogger(__name__)


"""
GUI specification for Absolutris
"""


range_playfield_width(7, 14)


class Gui:
    """
    Base GUI class. Any GUI must define its own class derived from this one.
    """
    def __init_subclass__(cls, /, flags, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        logger.error("Hook for checks is here")
        cls.flags = flags


class Debug(Gui, flags=pygame.NOFRAME):
    def __init__(self, playfield_width):
        self.playfield_width = playfield_width


if __name__ == "__main__":
    d = Debug()
