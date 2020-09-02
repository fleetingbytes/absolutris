#!/usr/bin/env python

import dataclasses
import logging


# Setup logging
logger = logging.getLogger(__name__)


DEFAULT_SOFT_DROP_FACTOR = 1
DEFAULT_HARD_DROP_FACTOR = 2


@dataclasses.dataclass
class Scoring:
    single: int
    double: int
    triple: int
    tetris: int
    def soft_drop(self, rows) -> int:
        return rows * DEFAULT_SOFT_DROP_FACTOR
    def hard_drop(self, rows) -> int:
        return rows * DEFAULT_HARD_DROP_FACTOR


@dataclasses.dataclass
class NES_Scoring(Scoring):
    single: int = dataclasses.field(init=False)
    double: int = dataclasses.field(init=False)
    triple: int = dataclasses.field(init=False)
    tetris: int = dataclasses.field(init=False)
    level: dataclasses.InitVar[int] = 0
    def __post_init__(self, level) -> None:
        self.single = 40 * (level + 1)
        self.double = 100 * (level + 1)
        self.triple = 300 * (level + 1)
        self.tetris = 1200 * (level + 1)


if __name__ == "__main__":
    lev0 = NES_Scoring(level=0)
    lev1 = NES_Scoring(level=1)
    lev2 = NES_Scoring(level=2)
    lev3 = NES_Scoring(level=3)
    lev4 = NES_Scoring(level=4)
    lev5 = NES_Scoring(level=5)
    lev18 = NES_Scoring(level=18)
    lev19 = NES_Scoring(level=19)
