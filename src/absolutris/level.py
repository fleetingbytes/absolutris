#!/usr/bin/env python

import dataclasses
import logging
# Typing
from typing import Callable
# Own modules
from absolutris import next_window
from absolutris import scoring
from absolutris import statistics


# Setup logging
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Level:
    """
    `message` is a short string which the GUI may display when the level is played
    `next_window` is the generator from which the tetrominoes are spawned.
                  It includes the random source, and optional packer.
    `gravity` defines the number of game_ticks between forced row drops
    `scoring` contains information how to score which event occurring in this level
    `condition` is a function which decides whether this level may start.
                It must raise `errors.MissedLevel` if the condition for starting
                this can no longer be reached.
    """
    message: str
    gravity: int
    scoring: scoring.Scoring
    condition: Callable[[statistics.Statistics], bool]


if __name__ == "__main__":
    pass
