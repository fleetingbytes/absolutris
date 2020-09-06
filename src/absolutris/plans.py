#!/usr/bin/env python

from __future__ import annotations
import dataclasses
import logging
# Typing
from absolutris import level
from absolutris import scoring
from absolutris import next_window
from absolutris.generators import randomorg


# Setup logging
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Plan:
    """
    Game plan. Contains the sequence of levels which can be played in a game.
    """
    name: str
    version: str
    levels: tuple[level.Level]
    next_window: next_window.Next_Window


default = Plan(
    name = "default"
    version "0.0.1"
    levels=(
        level.Level(
            message="Level 0",
            gravity=100,
            scoring=scoring.NES_Scoring(level=0),
            condition=lambda stat: stat.lines == 0,
            ),
        level.Level(
            message="Level 1",
            gravity=50,
            scoring=scoring.NES_Scoring(level=1),
            condition=lambda stat: stat.lines == 3,
            ),
        ),
    next_window=next_window.Next_Window(source=randomorg.source(), length=1)
    )


if __name__ == "__main__":
    pass
