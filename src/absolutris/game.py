#!/usr/bin/env python

import pygame
import logging
# Necessary for Typing
from absolutris import config_loader
# Own modules
from absolutris import errors


# setup logging
logger = logging.getLogger(__name__)


class Game:
    """
    Main Game class.
    """
    def __init__(self):
        pass
    def run(self):
        logger.debug("Running game")
        logger.debug("Finished running game")


def run(config: config_loader.Config):
    logger.debug(f"Running GUI")
    game = Game()
    game.run()
    logger.debug(f"Ending GUI")


if __name__ == "__main__":
    logger.debug(f"GUI started")
    logger.debug(f"GUI ended")
