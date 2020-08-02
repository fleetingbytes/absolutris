#!/usr/bin/env python

import logging

# setup logging
logger = logging.getLogger(__name__)


class Playfield:
    def __init__(self, width, height, level) -> None:
        self.width = width
        self.height = height
        self.level = level


if __name__ == "__main__":
    pass
