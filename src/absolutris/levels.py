#!/usr/bin/env python

import logging
# Own modules
from absolutris import next_window


# Setup logging
logger = logging.getLogger(__name__)


class Level:
    """
    Class defining an Absolutris level
    `source` should be an instance of Next_Window
    """
    def __init__(self, next_window: next_window.Next_Window) -> None:
        self.next_window = next_window


if __name__ == "__main__":
    pass
