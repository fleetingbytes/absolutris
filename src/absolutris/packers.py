#!/usr/bin/env python

"""
Packers for Absolutris

Packers pull random tetrominoes (represented as base-7 integers) from a random source and manipulate them.
For example they create virual bags of tetrominoes which contain each type of tetromino, ensuring that the
draughts between two types of tetrominoes are not too long.
"""

import logging
import collections
from typing import Generator
from absolutris import errors


#setup logging
logger = logging.getLogger(__name__)


DEFAULT_BAG_SIZE = 7


class Packer:
    def __init__(self, source: Generator[int, None, None], bag_size=DEFAULT_BAG_SIZE) -> None:
        self.bag = collections.deque(tuple(None for _ in range(bag_size)), maxlen=bag_size)
        self.source = source
        self.fill_bag()
    def fill_bag(self) -> None:
        """
        Fills the bag with unique tetromino types.
        """
        logger.debug("Refilling bag")
        warn = False
        while (len(self.bag) < self.bag.maxlen) or (None in self.bag):
            try:
                tetromino = next(self.source)
                if tetromino not in self.bag:
                    self.bag.append(tetromino)
            except StopIteration:
                while None in self.bag:
                    self.bag.remove(None)
                warn = True
                break
        if not warn:
            logger.debug(f"Bag refilled: {self.bag = }")
        else:
            logger.warning(f"Bag not quite refilled: {self.bag = }")
    def bag_gen(self) -> Generator[int, None, None]:
        while True:
            if not self.bag:
                logger.debug(f"{self.bag = }, need to refill")
                self.fill_bag()
                if len(self.bag) == 0:
                    return None
            else:
                try:
                    yield self.bag.popleft()
                except IndexError:
                    raise errors.EndGame("Packer wants to end game, you should investigate how we got here.")


if __name__ == "__main__":
    pass
