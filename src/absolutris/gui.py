#!/usr/bin/env python

import pygame
import logging
from absolutris import config_loader

# setup logging
logger = logging.getLogger(__name__)


def run(config: config_loader.Config):
    logger.debug(f"Running GUI")


if __name__ == "__main__":
    logger.debug(f"GUI started")
